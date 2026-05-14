---
name: audio-transcriber
description: Chuyên gia chuyển đổi audio/video YouTube thành transcript local, offline. Sử dụng skill này khi user gửi link YouTube, cần tải transcript, hoặc muốn xử lý audio/video thành văn bản. Hỗ trợ 3 quality modes (fast/normal/max) và 2 quantity modes (solo/multi). Toàn bộ pipeline chạy local, không cần internet sau khi setup. Script tự detect hardware và tối ưu worker count.
---

# Audio Transcriber

## Selection

**Quality** (`--mode`): độ chi tiết của transcript
| Mode | Pipeline | Đầu ra | Khi nào dùng |
|------|----------|--------|-------------|
| **fast** | download → denoise → transcribe → format_fast | Timestamp `[mm:ss]`, 1 luồng text | Clip ngắn, 1 speaker, cần nhanh |
| **normal** | + diarize + format_normal | Speaker labels, gộp đoạn văn | Podcast, phỏng vấn, nhiều speaker |
| **max** | + diarize + format_max | Metadata đầy đủ, speaker blocks | Archive, reference, hậu kỳ AI |

**Quantity** (`--quantity`): số video xử lý cùng lúc
| Mode | Worker count | Khi nào dùng |
|------|-------------|-------------|
| **solo** | 1 video tại 1 thời điểm | Mặc định, ổn định nhất |
| **multi** | Auto-detect dựa trên hardware | Tối ưu thời gian, có GPU≥6GB hoặc CPU≥8 cores |

## Workflow (2 bước)

### Bước 0: Kiểm tra môi trường (bắt buộc)
```powershell
python scripts/check_env.py
```
Nếu FAIL → chạy `powershell scripts/setup.ps1` để cài đặt.

### Bước 1: Chạy batch transcribe
```powershell
python scripts/batch_transcribe_channel.py <channel_url> -o <output_dir> --mode <quality> --quantity <quantity>
```

Script tự động: detect resources → benchmark → tối ưu workers → pipeline → log → cleanup.

### Ví dụ
```powershell
# Fast + Solo (mặc định)
python scripts/batch_transcribe_channel.py "https://www.youtube.com/@SiiniClips" -o "C:\path\to\output" --mode fast --quantity solo

# Fast + Multi (auto-detect workers)
python scripts/batch_transcribe_channel.py "https://www.youtube.com/@SiiniClips" -o "C:\path\to\output" --mode fast --quantity multi

# Normal + Multi
python scripts/batch_transcribe_channel.py "https://www.youtube.com/@SiiniClips" -o "C:\path\to\output" --mode normal --quantity multi

# Max + Solo
python scripts/batch_transcribe_channel.py "https://www.youtube.com/@SiiniClips" -o "C:\path\to\output" --mode max --quantity solo
```

### Dry-run (xem cấu hình trước khi chạy)
```powershell
python scripts/batch_transcribe_channel.py "https://www.youtube.com/@SiiniClips" -o "C:\path\to\output" --mode fast --quantity multi --dry-run
```

## Pipeline detail

Mỗi mode tương ứng 1 format script trong `scripts/`:
- **fast** → `format_fast.py` → file `_Fast.md`
- **normal** → `format_normal.py` → file `_Normal.md`
- **max** → `format_max.py` → file `_Max.md`

Mỗi quality mode có processed log riêng (`processed_videos_fast.log`, `processed_videos_normal.log`, `processed_videos_max.log`) để tránh chạy lại.

## References (đọc khi cần chi tiết)

| File | Nội dung |
|------|----------|
| `references/quality-fast.md` | Fast mode output format, caveats |
| `references/quality-normal.md` | Normal mode diarization details |
| `references/quality-max.md` | Max mode full metadata structure |

## Notes

- **Hoàn toàn local/offline**: không gửi data ra ngoài
- **Hallucination**: Whisper có thể "vẽ" lời nói từ nhiễu → để ý tag `[LOW_CONFIDENCE]`
- **Diarization**: nhận diện speaker trong môi trường ồn không chính xác 100%
- **Multi mode + GPU**: nếu VRAM không đủ cho N workers, tự fallback CPU int8
