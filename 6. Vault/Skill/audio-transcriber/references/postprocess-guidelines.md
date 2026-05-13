# Post-processing Guidelines

## Nguyên tắc cốt lõi: TÔN TRỌNG HỘI THOẠI GỐC

### 1. KHÔNG thay đổi câu từ gốc

Tuyệt đối không thêm, bớt, sửa từ ngữ trong lời nói của nhân vật. Nội dung phải giống hệt những gì transcript raw trả về.

### 2. Được phép: Làm rõ văn phong (khi cần)

Chỉ áp dụng khi nội dung **tối nghĩa đến mức người đọc không hiểu được** — ví dụ:

| Transcript gốc (tối nghĩa) | Sau khi làm rõ (OK) |
|---|---|
| "ờ thì cái đó... ừ... nó không được" | "Ờ thì cái đó... ừ... nó không được" |
| "bọn mình cần Q3 cái đó trước khi..." | "Bọn mình cần [quý 3] cái đó trước khi..." |

**Giới hạn của việc làm rõ:**
- ✅ Thêm từ nối cho mượt: "thì", "là", "mà" (chỉ khi cần)
- ✅ Viết hoa đầu câu, thêm dấu câu cơ bản
- ✅ Thêm chú thích trong `[ngoặc vuông]` nếu từ viết tắt khó hiểu
- ❌ Không paraphrase lại cả câu
- ❌ Không "diễn giải" theo ý hiểu của bạn
- ❌ Không bỏ qua từ ngữ khó nghe — giữ nguyên, thêm `[không rõ]`

### 3. Quy trình làm rõ

Khi gặp đoạn tối nghĩa, hãy tự hỏi:
1. **Người nói muốn truyền đạt gì?** — Nếu không chắc chắn, KHÔNG sửa
2. **Có thể thêm 1-2 từ để câu rõ nghĩa hơn mà không thay đổi ý?** — Nếu có, thêm
3. **Cần ghi chú giải thích?** — Nếu có, thêm footnote

### 4. Format transcript

```
### Transcript: [Title]
- **Nguồn:** [YouTube URL / File path]
- **Tác giả:** [Channel name]
- **Transcript ngày:** [ngày/tháng/năm]

---

**Nhân vật 1** (00:00 - 01:30)
> Nội dung hội thoại...

**Nhân vật 2** (01:31 - 03:00)
> Nội dung hội thoại...

---
*Ghi chú chỉnh sửa: Câu "[nguyên văn]" đã được làm rõ thành "[văn phòng mới]" — giữ nguyên nội dung, cải thiện văn phong.*
```

### 5. Mọi thay đổi đều phải có lý do

Nếu bạn chỉnh sửa bất kỳ từ nào so với raw transcript, PHẢI ghi chú ở cuối file với lý do. Nếu không có ghi chú, mặc định là không có chỉnh sửa nào.
