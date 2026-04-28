---
aliases: [Transformer, Attention Mechanism]
created: 2026-04-28 23:30:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [deep-dive, generative-ai, transformer, sql-injection]
category: [research]
---
# Deep Dive: Transformers - Trái tim của SQL và Ngôn ngữ

## 1. Bản chất cốt lõi (Core Intuition)
Hãy tưởng tượng bạn đang đọc một câu lệnh SQL phức tạp. Để hiểu được nó, mắt bạn không đọc từng chữ từ trái sang phải một cách đều đặn. Thay vào đó, khi thấy từ `WHERE`, mắt bạn sẽ tự động "nhảy" đi tìm xem điều kiện đằng sau nó là gì.

**Transformers** sinh ra để làm đúng việc đó: Nó không đọc tuần tự (như con người đọc dòng kẻ), mà nó nhìn **toàn bộ câu lệnh cùng một lúc** và xác định xem những từ nào "có liên quan" chặt chẽ đến nhau.

- **Nỗi đau giải quyết:** Các mô hình cũ (RNN/LSTM) rất mau quên. Nếu câu SQL quá dài, đến cuối câu nó sẽ quên mất đầu câu viết gì. Transformer khắc phục điều này bằng cách giữ liên kết giữa mọi từ trong câu, bất kể khoảng cách.

## 2. Cách thức vận hành (How it works)
Transformer hoạt động dựa trên 2 bộ phận chính:
1.  **Encoder (Người hiểu):** Đọc câu lệnh SQL đầu vào, phân tích cấu trúc, nhận diện đâu là từ khóa (`SELECT`, `UNION`), đâu là dữ liệu.
2.  **Decoder (Người viết):** Dựa trên những gì Encoder hiểu, nó sẽ dự đoán từ tiếp theo cần viết là gì để tạo ra một câu SQL hoàn chỉnh.

Điểm đặc biệt nhất là **Self-Attention**: Mỗi từ trong câu sẽ tự hỏi các từ còn lại: *"Bạn có liên quan gì đến tôi không?"*. 
Ví dụ: Trong câu `SELECT * FROM users WHERE id = '1' OR '1'='1'`, từ `'OR'` sẽ cực kỳ quan trọng vì nó báo hiệu một cấu trúc tấn công.

## 3. Giải mã công thức (Math Decoded)

| Công thức | Ý nghĩa "tiếng người" | Tại sao quan trọng? |
| --- | --- | --- |
| **Attention(Q, K, V)** | Đây là quy trình "Tra cứu thư viện". | Giúp mô hình tập trung nguồn lực vào đúng chỗ. |
| **Query (Q)** | *"Tôi đang tìm kiếm thông tin gì?"* | Đại diện cho từ hiện tại đang xét. |
| **Key (K)** | *"Tôi có những thông tin gì để cung cấp?"* | Giúp xác định mức độ phù hợp giữa từ hiện tại với các từ khác. |
| **Value (V)** | *"Nội dung thực sự của thông tin đó là gì?"* | Là giá trị thực tế sẽ được đưa vào tính toán sau khi đã biết mức độ quan trọng. |
| **Softmax** | *"Trong các mối liên hệ này, cái nào là quan trọng nhất (theo tỉ lệ %)"* | Biến các con số khô khan thành xác suất. Tổng cộng các mối quan tâm luôn bằng 100%. |

## 4. Liên hệ bài toán SQL Injection
**Tại sao bạn cần Transformer cho SQLi?**
- **Hiểu cú pháp:** SQL Injection không phải là những từ ngẫu nhiên, nó là việc vi phạm cú pháp một cách có tính toán (ví dụ: đóng dấu nháy đơn `'` đúng lúc). Transformer cực giỏi trong việc bắt chước các "mẹo" cú pháp này.
- **Context-Aware:** Mô hình sẽ hiểu rằng sau `UNION SELECT`, các cột phải tương ứng với bảng trước đó. Đây là thứ mà các mô hình đơn giản không làm được.

**Nhược điểm:**
- Cần rất nhiều dữ liệu mẫu để mô hình "thấm" được các kiểu tấn công.
- Tốn tài nguyên tính toán (GPU).

## 5. Kết nối & Mở rộng (Connections)
- **Mô hình liên quan:** BERT (để phân loại SQLi), GPT (để tạo sinh SQLi).
- **Câu hỏi mở:** Liệu có thể dùng Transformer làm Generator trong mô hình GAN để tạo ra các câu lệnh SQLi vừa "đúng cú pháp" vừa "bypass được WAF" không?

## 6. Tài liệu tham khảo
- Paper: "Attention Is All You Need" (2017).
- Blog: The Illustrated Transformer (Jay Alammar).
