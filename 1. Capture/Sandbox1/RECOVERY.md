# Recovery - Audio Transcriber Pipeline

## Trạng thái hiện tại

- **Đã xử lý:** 81 videos (trong `Sandbox1`)
- **Còn lại:** 290 videos (trong `remaining_videos.json`)
- **Device:** CUDA (float16) — ~4-6 phút / video
- **Output folder:** `C:\Users\Admin\Documents\Dashboard\1. Capture\Sandbox1`
- **Processed log:** `C:\Users\Admin\Documents\Dashboard\6. Vault\Skill\audio-transcriber\processed_videos_fast.log` (215 entries)

## Tiếp tục xử lý (Multi Fast)

Mở **PowerShell** và chạy:

```powershell
cd C:\Users\Admin\Documents\Dashboard\6. Vault\Skill\audio-transcriber
python scripts/batch_transcribe_channel.py "https://www.youtube.com/@SiiniClips" -o "C:\Users\Admin\Documents\Dashboard\1. Capture\Sandbox1" --mode fast --quantity multi
```

Pipeline tự động:
- Tải toàn bộ video từ kênh
- Bỏ qua video đã xử lý (trong `processed_videos_fast.log`)
- Multi workers: download + denoise song song, GPU transcribe 1 worker
- Output `{title}_Fast.md` vào Sandbox1
- Ghi log vào `processed_videos_fast.log`

## Chạy Solo (thủ công từng cái)

Dùng `process_remaining.py` nếu muốn chạy tuần tự theo `remaining_videos.json`:

```powershell
python scripts/process_remaining.py --max 1   # test 1 video
python scripts/process_remaining.py            # tất cả tuần tự
```

## Ghi chú

- CUDA crash ở transcribe cleanup đã được fix (validate file thay vì exit code)
- `process_remaining.py` dùng `remaining_videos.json` làm source of truth
- `batch_transcribe_channel.py` dùng `processed_videos_fast.log` làm source of truth
