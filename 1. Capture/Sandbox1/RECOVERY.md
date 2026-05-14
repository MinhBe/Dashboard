# Recovery - Audio Transcriber Pipeline

## Trạng thái hiện tại

- **Đã xử lý:** 1 video (`1pyR403UKXs` → `Twitch streamer tự hủy sự nghiệp_Fast.md`)
- **Còn lại:** 369 videos (trong `remaining_videos.json`)
- **Thời gian mỗi video (CPU int8, 6 threads):** ~18 phút / video 57 phút
- **Output folder:** `C:\Projects\Dashboard\1. Capture\Sandbox1`

## Đã fix

1. `C:\Projects\Dashboard\6. Vault\Skill\audio-transcriber\scripts\process_remaining.py`:
   - `OUTPUT_DIR` → `C:\Projects\Dashboard\1. Capture\Sandbox1`
   - Auto-detect CUDA/CPU (không còn hardcode `--device cuda`)
   - Thêm `--max N` để giới hạn số video xử lý

## Tiếp tục xử lý tất cả video còn lại

Mở **PowerShell 7** và chạy:

```powershell
cd C:\Projects\Dashboard\6. Vault\Skill\audio-transcriber
python scripts/process_remaining.py
```

Script sẽ tự động:
- Đọc `remaining_videos.json` → xử lý từng video
- Pipeline: download → denoise → transcribe (CPU int8) → format_fast
- Output: `{title}_Fast.md` vào `Sandbox1`
- Update JSON sau mỗi video (remove đã xử lý)
- Ghi log vào `processed_videos_fast.log` (tránh chạy lại)

## Test với 1 video (để kiểm tra)

```powershell
python scripts/process_remaining.py --max 1
```

## Output format

File `*_Fast.md`:
```
### [FAST] Transcript: {title}
- **Nguồn:** {url}
- **Ngày:** DD/MM/YYYY
- **Ngôn ngữ:** {language}

---

[00:00] {text}
[00:05] {text}
...
```
