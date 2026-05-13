---
name: audio-transcriber
description: Chuyên gia chuyển đổi audio và video YouTube thành transcript có nhận diện người nói, tối ưu cho môi trường ồn (quán cà phê) và ưu tiên xử lý LOCAL. Sử dụng skill này khi user gửi link YouTube hoặc file audio. Skill sẽ thực hiện quy trình kiểm tra môi trường, lọc nhiễu, và transcription trước khi hỏi ý kiến user về việc dùng AI để sửa lỗi văn phong.
---

# Audio Transcriber Skill (Local-First Edition)

Skill này tập trung vào việc xử lý âm thanh chất lượng thấp hoàn toàn LOCAL. **QUY TẮC TỐI THƯỢNG: Luôn kiểm tra môi trường trước mỗi lần xử lý, không có ngoại lệ.**

## Quy Trình Bắt Buộc (Mọi lúc, mọi nơi)

### Bước 0: Kiểm tra môi trường (MANDATORY)
Trong **MỌI PHIÊN LÀM VIỆC**, ngay khi nhận được yêu cầu xử lý audio/video, Model PHẢI chạy script kiểm tra:
```powershell
python scripts/check_env.py
```
- **Nếu PASS**: Tiếp tục sang Bước 1.
- **Nếu FAIL**: 
    1. Model PHẢI liệt kê các thành phần thiếu.
    2. **CHỦ ĐỘNG** dùng `ask_user` hỏi: *"Môi trường chưa sẵn sàng. Bạn có muốn tôi tự động chạy scripts/setup.ps1 để cài đặt các thành phần còn thiếu không?"*
    3. Nếu User đồng ý: Chạy lệnh `powershell scripts/setup.ps1` ngay lập tức. Sau đó chạy lại Bước 0 để xác nhận trước khi tiếp tục.

### Bước 1: Thu thập & Tiền xử lý (Denoise & VAD)
Lọc nhiễu quán cà phê và cắt bỏ khoảng lặng để tối ưu cho Whisper.
```powershell
# Nếu là YouTube:
python scripts/download_audio.py "<URL>" -o "<temp>"
# Tiền xử lý (Bắt buộc cho cả file local và YouTube):
python scripts/denoise.py "<input_file>" --output "<temp>/clean.wav"
```

### Bước 2: Transcription & Confidence Tagging
Xử lý chuyển đổi âm thanh thành văn bản thô với Faster-Whisper.
```powershell
python scripts/transcribe.py "<temp>/clean.wav" --output "<temp>/segments.json" --model-dir "models"
```
- **Logic**: Tự động gắn tag `[LOW_CONFIDENCE]` nếu `avg_logprob < -1.0`.

### Bước 3: Diarization (Optional - Chỉ dùng cho Mode Blog/Max)
```powershell
python scripts/diarize.py "<temp>/clean.wav" --output "<temp>/speakers.json"
```

### Bước 4: Formatting (Chọn 1 trong 3 chế độ)

**Mode 1: Fast (Nhanh, có nhãn thời gian)**
```powershell
python scripts/format_fast.py --segments "<temp>/segments.json" --metadata "<temp>/metadata.json" --output-dir "<output>"
```

**Mode 2: Blog (Gộp đoạn văn, loại bỏ thời gian chi tiết)**
```powershell
python scripts/format_blog.py --segments "<temp>/segments.json" --speakers "<temp>/speakers.json" --metadata "<temp>/metadata.json" --output-dir "<output>"
```

**Mode 3: Max (Chi tiết nhất, đầy đủ metadata và diarization)**
```powershell
python scripts/format_max.py --segments "<temp>/segments.json" --speakers "<temp>/speakers.json" --metadata "<temp>/metadata.json" --output-dir "<output>"
```

## Các lệnh thực thi chính

1. **Setup**: `powershell scripts/setup.ps1`
2. **Quy trình Fast (Tốc độ cao nhất)**:
   - Download -> Denoise -> Transcribe -> format_fast.py
3. **Quy trình Blog (Dễ đọc)**:
   - Download -> Denoise -> Transcribe -> Diarize -> format_blog.py
4. **Quy trình Max (Chất lượng tối đa)**:
   - Download -> Denoise -> Transcribe -> Diarize -> format_max.py

## Cấu trúc thư mục

- `models/`: Whisper và VAD models.
- `scripts/`: Chứa các script xử lý (download, denoise, transcribe, diarize, format_*).
- `temp/`: Thư mục tạm thời.

## Lưu ý quan trọng
- **Tính riêng tư**: Mọi bước xử lý âm thanh đều diễn ra Offline. 
- **Hallucination**: Whisper có thể "vẽ" ra lời nói từ tiếng ồn. Luôn chú ý các tag `[LOW_CONFIDENCE]`.
- **Diarization**: Nhận diện người nói trong môi trường ồn có thể không chính xác 100%, cần kiểm tra lại tên "Nhân vật".
