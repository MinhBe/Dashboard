#!/usr/bin/env python3
"""
Batch transcribe YouTube channel with auto-resource detection,
benchmarking, and parallel pipeline optimization.

Pipeline: parallel download+denoise -> N transcribe workers -> format
Supports quality modes: fast | normal | max
Supports quantity modes: solo (1 worker) | multi (N auto-detected workers)
"""

import argparse
import json
import os
import subprocess
import sys
import shutil
import time
import threading
import queue
import re
from pathlib import Path
from datetime import datetime, date

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.normpath(os.path.join(SCRIPTS_DIR, ".."))
DEFAULT_TEMP = os.path.join(SKILL_DIR, "temp")

# Find models directory (check parent Skill/models/ first)
_candidate_models = [
    os.path.join(os.path.dirname(SKILL_DIR), "models"),
    os.path.join(SKILL_DIR, "models"),
]
MODELS_DIR = None
for d in _candidate_models:
    if os.path.isdir(d) and any("faster-whisper" in item for item in os.listdir(d)):
        MODELS_DIR = d
        break
if not MODELS_DIR:
    MODELS_DIR = _candidate_models[0]


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def run(cmd, capture=False):
    eprint(f"  [{os.path.basename(cmd[0])}] {' '.join(str(a) for a in cmd[1:])}")
    try:
        result = subprocess.run(cmd, capture_output=capture, text=True)
        ok = result.returncode == 0
        return (ok, result.stdout, result.stderr) if capture else (ok, "", "")
    except Exception as e:
        return (False, "", str(e))


def load_config():
    config_path = os.path.join(SCRIPTS_DIR, "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_resources():
    cpu_count = os.cpu_count() or 4
    ram_total_gb = 16.0
    ram_avail_gb = 8.0
    try:
        import psutil
        mem = psutil.virtual_memory()
        ram_total_gb = mem.total / 1024**3
        ram_avail_gb = mem.available / 1024**3
    except ImportError:
        eprint("  [!] psutil not available, using default RAM estimates")

    has_cuda = False
    gpu_name = ""
    vram_gb = 0
    try:
        import torch
        if torch.cuda.is_available():
            has_cuda = True
            gpu_name = torch.cuda.get_device_name(0)
            vram_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
    except Exception:
        pass

    return {
        "cpu_logical_cores": cpu_count,
        "ram_total_gb": round(ram_total_gb, 1),
        "ram_avail_gb": round(ram_avail_gb, 1),
        "has_cuda": has_cuda,
        "gpu_name": gpu_name,
        "vram_gb": round(vram_gb, 1),
    }


def run_benchmark(bench_video_id, config, device, compute_type, beam_size):
    bench_dir = os.path.join(DEFAULT_TEMP, f"__bench_{bench_video_id}")
    if os.path.exists(bench_dir):
        shutil.rmtree(bench_dir)
    os.makedirs(bench_dir, exist_ok=True)

    eprint("\n  ── BENCHMARK ──")
    eprint(f"  Sample: video {bench_video_id}, first 60s")

    url = f"https://www.youtube.com/watch?v={bench_video_id}"
    output_template = os.path.join(bench_dir, "%(id)s.%(ext)s")
    dl_cmd = [
        sys.executable, "-m", "yt_dlp",
        "-x", "--audio-format", "wav", "--audio-quality", "0",
        "--postprocessor-args", "ffmpeg:-ac 1 -ar 16000",
        "--cookies-from-browser", "chrome",
        "--js-runtimes", "node",
        "--download-sections", "*0-60",
        "-o", output_template, url,
    ]

    t0 = time.time()
    ok, _, _ = run(dl_cmd)
    if not ok:
        eprint("  [!] Benchmark download failed")
        shutil.rmtree(bench_dir, ignore_errors=True)
        return None
    dl_time = time.time() - t0

    audio_path = None
    for f in os.listdir(bench_dir):
        if f.endswith(".wav"):
            audio_path = os.path.join(bench_dir, f)
            break
    if not audio_path:
        shutil.rmtree(bench_dir, ignore_errors=True)
        return None

    std_audio = os.path.join(bench_dir, "audio.wav")
    if os.path.exists(std_audio):
        os.remove(std_audio)
    os.rename(audio_path, std_audio)

    try:
        import soundfile as sf
        data, sr = sf.read(std_audio)
        audio_dur = len(data) / sr
    except Exception:
        audio_dur = 60.0

    eprint(f"  Audio: {audio_dur:.0f}s, download: {dl_time:.1f}s")

    clean_wav = os.path.join(bench_dir, "clean.wav")
    t0 = time.time()
    ok, _, _ = run([
        sys.executable, os.path.join(SCRIPTS_DIR, "denoise.py"),
        std_audio, "-o", clean_wav, "--vad-threshold", "0.4",
    ])
    denoise_time = time.time() - t0
    if not ok or not os.path.exists(clean_wav):
        eprint("  [!] Benchmark denoise failed")
        shutil.rmtree(bench_dir, ignore_errors=True)
        return None

    segments_json = os.path.join(bench_dir, "segments.json")
    t0 = time.time()
    ok, _, _ = run([
        sys.executable, os.path.join(SCRIPTS_DIR, "transcribe.py"),
        clean_wav, "-o", segments_json,
        "--model-dir", MODELS_DIR,
        "--device", device, "--compute-type", compute_type,
        "--beam-size", str(beam_size),
    ])
    transcribe_time = time.time() - t0

    denoise_ratio = denoise_time / audio_dur
    transcribe_ratio = transcribe_time / audio_dur
    speed_ratio = denoise_ratio / transcribe_ratio if transcribe_ratio > 0 else 1.0

    eprint(f"  Denoise:    {denoise_time:.1f}s ({denoise_ratio:.2f}x)")
    eprint(f"  Transcribe: {transcribe_time:.1f}s ({transcribe_ratio:.2f}x)")
    eprint(f"  Ratio (denoise/transcribe): {speed_ratio:.1f}")

    result = {
        "device": device,
        "compute_type": compute_type,
        "beam_size": beam_size,
        "audio_duration": round(audio_dur, 1),
        "denoise_seconds": round(denoise_time, 2),
        "transcribe_seconds": round(transcribe_time, 2),
        "denoise_sps": round(denoise_ratio, 4),
        "transcribe_sps": round(transcribe_ratio, 4),
        "speed_ratio": round(speed_ratio, 2),
        "benchmark_date": str(date.today()),
    }
    bench_log = os.path.join(DEFAULT_TEMP, "benchmark_result.json")
    with open(bench_log, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    eprint(f"  Benchmark saved to {bench_log}")

    shutil.rmtree(bench_dir, ignore_errors=True)
    return result


def load_cached_benchmark():
    bench_log = os.path.join(DEFAULT_TEMP, "benchmark_result.json")
    if os.path.exists(bench_log):
        with open(bench_log, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def calc_workers(resources, config, benchmark):
    cpu_target = config.get("cpu_target", 0.70)
    gpu_target = config.get("gpu_target", 0.85)
    min_vram = config.get("min_vram_gb", 4.0)
    max_cpu_workers = config.get("max_cpu_workers", 10)
    beam_size = config.get("beam_size", 3)

    cpu_cores = resources["cpu_logical_cores"]
    ram_avail = resources["ram_avail_gb"]
    has_cuda = resources["has_cuda"]
    vram = resources["vram_gb"]

    use_cuda = has_cuda and vram >= min_vram
    device = "cuda" if use_cuda else "cpu"
    compute_type = "float16" if use_cuda else "int8"

    gpu_workers = 1 if use_cuda else 0

    max_by_cpu = max(1, round(cpu_cores * cpu_target / 3))
    max_by_cpu = min(max_by_cpu, max_cpu_workers)
    max_by_ram = max(1, round(ram_avail / 1.2))
    cpu_ceiling = min(max_by_cpu, max_by_ram)

    if use_cuda and benchmark and benchmark.get("speed_ratio"):
        sr = benchmark["speed_ratio"]
        if sr < 0.8:
            ideal = min(3, cpu_ceiling)
        elif sr < 1.5:
            ideal = min(2, cpu_ceiling)
        else:
            ideal = max(1, min(cpu_ceiling, round(sr * 1.3)))
        denoise_workers = min(ideal, cpu_ceiling)
        eprint(f"  [tune] speed_ratio={sr:.1f}, ideal_workers={ideal}, ceiling={cpu_ceiling}")
    else:
        denoise_workers = cpu_ceiling

    if not use_cuda:
        denoise_workers = min(cpu_ceiling, 3)

    return {
        "device": device,
        "compute_type": compute_type,
        "beam_size": beam_size,
        "denoise_workers": denoise_workers,
        "gpu_workers": gpu_workers,
    }


def calc_transcribe_workers(quantity, resources, device, config):
    if quantity == "solo":
        return {
            "transcribe_workers": 1,
            "transcribe_note": "solo (1 worker)",
        }

    has_cuda = resources["has_cuda"]
    vram = resources["vram_gb"]
    cpu_cores = resources["cpu_logical_cores"]
    ram_avail = resources["ram_avail_gb"]

    max_workers = config.get("max_transcribe_workers", 4)
    gpu_vram_per_worker = config.get("gpu_vram_per_worker", 2.5)
    cpu_cores_per_worker = config.get("cpu_cores_per_worker", 4)
    cpu_ram_per_worker = config.get("cpu_ram_per_worker_gb", 3.0)

    if device == "cuda":
        usable_vram = vram - 1.0
        workers = max(1, int(usable_vram / gpu_vram_per_worker))
        workers = min(workers, max_workers)
        note = f"GPU {vram}GB VRAM -> {workers} worker(s)"
    else:
        workers = max(1, min(
            max_workers,
            int(cpu_cores / cpu_cores_per_worker),
            int(ram_avail / cpu_ram_per_worker),
        ))
        note = f"CPU {cpu_cores} cores / {ram_avail}GB RAM -> {workers} worker(s)"

    return {
        "transcribe_workers": workers,
        "transcribe_note": note,
    }


def print_config_report(resources, config, workers, quantity_info):
    cpu_target = config.get("cpu_target", 0.70) * 100
    gpu_target = config.get("gpu_target", 0.85) * 100

    eprint("\n" + "=" * 55)
    eprint("  SYSTEM & RESOURCE OPTIMIZATION REPORT")
    eprint("=" * 55)
    eprint(f"  CPU        : {resources['cpu_logical_cores']} logical cores")
    eprint(f"  RAM        : {resources['ram_avail_gb']} GB available / {resources['ram_total_gb']} GB total")
    eprint(f"  GPU        : {resources['gpu_name'] or 'N/A'} ({resources['vram_gb']} GB)")
    eprint("─" * 55)
    eprint(f"  Thresholds    : CPU ~{cpu_target:.0f}% | GPU ~{gpu_target:.0f}%")
    eprint(f"  Device        : {workers['device'].upper()}")
    eprint(f"  Compute type  : {workers['compute_type']}")
    eprint(f"  Beam size     : {workers['beam_size']}")
    eprint(f"  Denoise pool  : {workers['denoise_workers']} workers")
    eprint(f"  Transcriber   : {quantity_info['transcribe_workers']} worker(s) ({quantity_info['transcribe_note']})")
    est_cpu_util = min(100, round(workers['denoise_workers'] * 3 / resources['cpu_logical_cores'] * 100))
    est_gpu_util = 85 if workers['gpu_workers'] > 0 else 0
    eprint(f"  Est. CPU util : ~{est_cpu_util}% (target {cpu_target:.0f}%)")
    eprint(f"  Est. GPU util : ~{est_gpu_util}% (target {gpu_target:.0f}%)")
    eprint("=" * 55 + "\n")


def get_video_ids(channel_url):
    cmd = ["yt-dlp", "--get-id", "--flat-playlist", "--cookies-from-browser", "chrome", "--js-runtimes", "node", channel_url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        eprint(f"  [!] Failed to get video IDs: {result.stderr[:200]}")
        return []
    return [v.strip() for v in result.stdout.strip().split("\n") if v.strip()]


def get_shortest_video_id(video_ids, min_duration=30):
    durations = []
    for vid in video_ids[:10]:
        cmd = [
            "yt-dlp", "--dump-json", "--no-download",
            "--cookies-from-browser", "chrome",
            "--js-runtimes", "node",
            f"https://www.youtube.com/watch?v={vid}",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout.strip().split("\n")[0])
                dur = data.get("duration", 0)
                if dur and dur >= min_duration:
                    durations.append((vid, dur))
            except Exception:
                pass
        else:
            eprint(f"  [!] Failed to get duration for {vid}")

    durations.sort(key=lambda x: x[1])
    if durations:
        eprint(f"  Shortest video for benchmark: {durations[0][0]} ({durations[0][1]}s)")
        return durations[0][0]
    return video_ids[0] if video_ids else None


def format_duration(seconds):
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    else:
        return f"{int(seconds // 3600)}h {int((seconds % 3600) // 60)}m"


def main():
    parser = argparse.ArgumentParser(
        description="Batch transcribe YouTube channel (auto-resource pipeline)")
    parser.add_argument("channel_url", help="YouTube channel URL")
    parser.add_argument("--output-dir", "-o", required=True,
                        help="Output directory for .md files")
    parser.add_argument("--mode", choices=["fast", "normal", "max"],
                        default="fast", help="Quality mode (default: fast)")
    parser.add_argument("--quantity", choices=["solo", "multi"],
                        default="solo", help="Quantity mode: solo=1 video, multi=auto-detected workers (default: solo)")
    parser.add_argument("--cpu-target", type=float, default=None,
                        help="CPU utilization target 0.0-1.0 (overrides config.json)")
    parser.add_argument("--gpu-target", type=float, default=None,
                        help="GPU utilization target 0.0-1.0 (overrides config.json)")
    parser.add_argument("--no-benchmark", action="store_true",
                        help="Skip benchmark, use heuristic defaults")
    parser.add_argument("--dry-run", action="store_true",
                        help="Detect resources, print config, and exit")
    parser.add_argument("--force", action="store_true",
                        help="Reprocess all videos, ignoring processed log")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(DEFAULT_TEMP, exist_ok=True)

    base_config = load_config()
    config = {
        **base_config,
        "beam_size": base_config.get("whisper", {}).get("beam_size", 3),
    }
    rcfg = base_config.get("resource", {})
    if args.cpu_target is not None:
        rcfg["cpu_target"] = args.cpu_target
    if args.gpu_target is not None:
        rcfg["gpu_target"] = args.gpu_target
    config["cpu_target"] = rcfg.get("cpu_target", 0.70)
    config["gpu_target"] = rcfg.get("gpu_target", 0.85)
    config["min_vram_gb"] = rcfg.get("min_vram_gb", 4.0)
    config["max_cpu_workers"] = rcfg.get("max_cpu_workers", 10)
    config["enable_benchmark"] = rcfg.get("enable_benchmark", True)

    eprint("\n[1/5] Detecting system resources...")
    resources = detect_resources()

    eprint("[2/5] Fetching channel video list...")
    all_ids = get_video_ids(args.channel_url)
    if not all_ids:
        eprint("  [!] No videos found!")
        sys.exit(1)
    eprint(f"  Found {len(all_ids)} videos on channel")

    log_path = os.path.join(SKILL_DIR, f"processed_videos_{args.mode}.log")
    processed_ids = set()
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            processed_ids = set(line.strip() for line in f if line.strip())
    if args.force:
        processed_ids = set()
        eprint("  --force: ignoring processed log")

    pending = [v for v in all_ids if v not in processed_ids]
    eprint(f"  Already processed: {len(processed_ids)}, pending: {len(pending)}")

    if not pending:
        eprint("\n  All videos already processed!")
        return

    benchmark = None
    if args.dry_run or args.no_benchmark or not resources["has_cuda"]:
        workers = calc_workers(resources, config, benchmark)
        quantity_info = calc_transcribe_workers(args.quantity, resources, workers["device"], config)
        print_config_report(resources, config, workers, quantity_info)
        if args.dry_run:
            eprint("Dry-run complete. Exiting. (Run without --dry-run to benchmark and execute)")
            return
    else:
        eprint("[3/5] Running benchmark...")
        cached = load_cached_benchmark()
        if cached and cached.get("device") == "cuda":
            eprint("  Using cached benchmark from previous run")
            benchmark = cached
        else:
            bench_vid = get_shortest_video_id(pending)
            if bench_vid:
                benchmark = run_benchmark(
                    bench_vid, config,
                    device="cuda",
                    compute_type="float16",
                    beam_size=config["beam_size"],
                )
            else:
                eprint("  Could not find suitable video for benchmark")
        if benchmark is None:
            eprint("  No benchmark data, using heuristic defaults")

        eprint("[4/5] Optimizing workers with benchmark data...")
        workers = calc_workers(resources, config, benchmark)
        quantity_info = calc_transcribe_workers(args.quantity, resources, workers["device"], config)
        print_config_report(resources, config, workers, quantity_info)

    transcribe_workers = quantity_info["transcribe_workers"]

    eprint("[5/5] Starting pipeline...")
    eprint(f"  Output dir: {args.output_dir}")
    eprint(f"  Quality    : {args.mode}")
    eprint(f"  Quantity   : {args.quantity} ({transcribe_workers} worker(s))")
    eprint(f"  Workers    : {workers['denoise_workers']} denoise, "
           f"{transcribe_workers} transcribe")

    if args.mode in ("normal", "max"):
        eprint(f"  [!] Mode '{args.mode}' uses diarization (slower per video)")

    SENTINEL = ("__SENTINEL__", None)
    dl_queue = queue.Queue()
    tr_queue = queue.Queue()
    pipeline_done = threading.Event()
    tr_workers_done = threading.Event()
    stats = {"downloaded": 0, "denoised": 0, "transcribed": 0, "formatted": 0, "failed": 0, "total": len(pending)}
    stats_lock = threading.Lock()
    tr_finished_count = [0]

    def download_producer():
        for vid in pending:
            vid_dir = os.path.join(DEFAULT_TEMP, f"pipe_{vid}")
            if os.path.exists(vid_dir):
                shutil.rmtree(vid_dir, ignore_errors=True)
            os.makedirs(vid_dir, exist_ok=True)

            url = f"https://www.youtube.com/watch?v={vid}"
            ok, _, _ = run([
                sys.executable, os.path.join(SCRIPTS_DIR, "download_audio.py"),
                url, "-o", vid_dir,
            ])
            if ok:
                dl_queue.put((vid, vid_dir))
                with stats_lock:
                    stats["downloaded"] += 1
            else:
                with stats_lock:
                    stats["failed"] += 1
                eprint(f"  [!] Download failed for {vid}")

        for _ in range(workers["denoise_workers"]):
            dl_queue.put(SENTINEL)

    def denoise_consumer():
        while True:
            item = dl_queue.get()
            if item is SENTINEL:
                tr_queue.put(SENTINEL)
                dl_queue.task_done()
                return
            vid, vid_dir = item

            clean_wav = os.path.join(vid_dir, "clean.wav")
            audio_wav = os.path.join(vid_dir, "audio.wav")
            ok, _, _ = run([
                sys.executable, os.path.join(SCRIPTS_DIR, "denoise.py"),
                audio_wav, "-o", clean_wav, "--vad-threshold", "0.4",
            ])
            if ok:
                tr_queue.put((vid, vid_dir))
                with stats_lock:
                    stats["denoised"] += 1
            else:
                with stats_lock:
                    stats["failed"] += 1
                eprint(f"  [!] Denoise failed for {vid}")
            dl_queue.task_done()

    def format_segment(segments_json, metadata_json, speakers_json, vid_dir):
        if args.mode == "fast":
            return run([
                sys.executable, os.path.join(SCRIPTS_DIR, "format_fast.py"),
                "-s", segments_json, "-m", metadata_json,
                "-o", args.output_dir,
            ])
        elif args.mode == "normal":
            if speakers_json and os.path.exists(speakers_json):
                return run([
                    sys.executable, os.path.join(SCRIPTS_DIR, "format_normal.py"),
                    "-s", segments_json, "-m", metadata_json,
                    "-sp", speakers_json, "-o", args.output_dir,
                ])
            else:
                return run([
                    sys.executable, os.path.join(SCRIPTS_DIR, "format_normal.py"),
                    "-s", segments_json, "-m", metadata_json,
                    "-o", args.output_dir,
                ])
        elif args.mode == "max":
            if speakers_json and os.path.exists(speakers_json):
                return run([
                    sys.executable, os.path.join(SCRIPTS_DIR, "format_max.py"),
                    "-s", segments_json, "-m", metadata_json,
                    "-sp", speakers_json, "-o", args.output_dir,
                ])
            else:
                eprint("  [!] Max mode requires diarization, skipping")
                return (False, "", "")

    def transcribe_consumer(worker_id):
        while True:
            item = tr_queue.get()
            if item is SENTINEL:
                tr_queue.task_done()
                with stats_lock:
                    tr_finished_count[0] += 1
                    if tr_finished_count[0] >= transcribe_workers:
                        tr_workers_done.set()
                return
            vid, vid_dir = item

            clean_wav = os.path.join(vid_dir, "clean.wav")
            segments_json = os.path.join(vid_dir, "segments.json")
            metadata_json = os.path.join(vid_dir, "metadata.json")
            speakers_json = os.path.join(vid_dir, "speakers.json")

            ok, _, _ = run([
                sys.executable, os.path.join(SCRIPTS_DIR, "transcribe.py"),
                clean_wav, "-o", segments_json,
                "--model-dir", MODELS_DIR,
                "--device", workers["device"],
                "--compute-type", workers["compute_type"],
                "--beam-size", str(workers["beam_size"]),
            ])
            if not ok:
                with stats_lock:
                    stats["failed"] += 1
                tr_queue.task_done()
                eprint(f"  [!] Transcribe failed for {vid}")
                continue

            with stats_lock:
                stats["transcribed"] += 1

            if args.mode in ("normal", "max"):
                ok_diar, _, _ = run([
                    sys.executable, os.path.join(SCRIPTS_DIR, "diarize.py"),
                    clean_wav, "-o", speakers_json,
                ])
                if not ok_diar:
                    eprint(f"  [!] Diarization failed for {vid}, continuing without speakers")
                    if os.path.exists(speakers_json):
                        os.remove(speakers_json)

            ok_fmt, _, _ = format_segment(segments_json, metadata_json, speakers_json, vid_dir)
            if ok_fmt:
                with stats_lock:
                    stats["formatted"] += 1
                with open(log_path, "a") as f:
                    f.write(f"{vid}\n")
            else:
                eprint(f"  [!] Format failed for {vid}")

            shutil.rmtree(vid_dir, ignore_errors=True)
            tr_queue.task_done()

    def progress_monitor():
        total = len(pending)
        while not tr_workers_done.is_set():
            tr_workers_done.wait(15)
            if tr_workers_done.is_set():
                break
            with stats_lock:
                done = stats["formatted"]
                failed = stats["failed"]
                dled = stats["downloaded"]
                deno = stats["denoised"]
                trsc = stats["transcribed"]
            remaining = total - done - failed
            eta_str = ""
            if done > 0:
                elapsed = time.time() - start_time
                rate = done / max(elapsed, 1)
                eta = remaining / max(rate, 0.001)
                eta_str = f", ETA: {format_duration(eta)}"
            eprint(f"  [{done}/{total}] dl={dled} dn={deno} tr={trsc} ✔={done} ✘={failed}{eta_str}")

    start_time = time.time()

    dl_thread = threading.Thread(target=download_producer)
    dl_thread.start()

    denoise_threads = []
    for _ in range(workers["denoise_workers"]):
        t = threading.Thread(target=denoise_consumer, daemon=True)
        t.start()
        denoise_threads.append(t)

    tr_threads = []
    for i in range(transcribe_workers):
        t = threading.Thread(target=transcribe_consumer, args=(i,), daemon=True)
        t.start()
        tr_threads.append(t)

    pg_thread = threading.Thread(target=progress_monitor, daemon=True)
    pg_thread.start()

    dl_thread.join()
    eprint("  Downloads done. Waiting for denoise+transcribe pipeline...")

    tr_workers_done.wait()
    eprint("  Pipeline complete.")

    elapsed = time.time() - start_time
    eprint(f"\n{'=' * 55}")
    eprint(f"  BATCH COMPLETE")
    eprint(f"{'=' * 55}")
    with stats_lock:
        eprint(f"  Processed : {stats['formatted']}/{len(pending)}")
        eprint(f"  Failed    : {stats['failed']}")
        eprint(f"  Time      : {format_duration(elapsed)}")
    eprint(f"{'=' * 55}\n")


if __name__ == "__main__":
    main()
