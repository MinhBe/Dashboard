---
aliases: [Transformer, Attention Mechanism, Self-Attention]
created: 2026-04-29 01:00:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [deep-dive, generative-ai, transformer, architecture]
category: [research]
---
# Deep Dive: Transformers - Kiến trúc Cách mạng hóa Dữ liệu Chuỗi

## 1. Bản chất và Triết lý Thiết kế
Trước khi Transformer ra đời, các mô hình như RNN (Recurrent Neural Networks) hay LSTM xử lý dữ liệu như một đoàn tàu: từng toa một đi qua hầm. Nếu đoàn tàu quá dài, thông tin từ toa đầu tiên sẽ bị mờ nhạt khi đến toa cuối cùng. 

**Transformer** thay đổi hoàn toàn triết lý này bằng cách "đọc toàn bộ trang sách cùng lúc". Nó coi một câu lệnh SQL không phải là một chuỗi ký tự, mà là một **ma trận các mối quan hệ**. Triết lý cốt lõi là: **Mọi phần tử trong chuỗi đều có quyền truy cập trực tiếp vào mọi phần tử khác**, bất kể chúng cách xa nhau bao nhiêu.

## 2. Cấu trúc Vận hành Chi tiết

### 2.1. Positional Encoding (Mã hóa Vị trí)
Vì Transformer không đọc tuần tự, nó sẽ bị "mù" về thứ tự. Nó sẽ thấy `SELECT * FROM users` và `users FROM * SELECT` là giống hệt nhau. 
- **Cơ chế:** Nó cộng thêm một loại "nhạc tính" (sóng Sin và Cosin) vào mỗi vector từ. 
- **Ý nghĩa:** Mỗi vị trí trong câu sẽ có một chữ ký độc nhất. Nhờ đó, mô hình biết được từ `'` nằm ở đầu câu khác hoàn toàn với từ `'` nằm ở cuối câu, dù giá trị định danh của chúng là như nhau.

### 2.2. Multi-Head Attention (Sự chú ý Đa đầu)
Đừng tưởng tượng mô hình chỉ có một "con mắt" chú ý. Nó có 8, 12 hoặc thậm chí 96 "đầu" (heads) chú ý chạy song song.
- **Head 1:** Có thể chỉ tập trung vào cú pháp (sau `SELECT` phải là tên cột).
- **Head 2:** Tập trung vào các dấu hiệu tấn công (tìm các hàm như `SLEEP()`, `BENCHMARK()`).
- **Head 3:** Tập trung vào mối quan hệ giữa các bảng và điều kiện `WHERE`.
- **Kết quả:** Tổng hợp tất cả các góc nhìn này lại, mô hình có một cái nhìn toàn diện và đa chiều về câu lệnh SQL.

### 2.3. Residual Connections & Layer Normalization
Giống như một người vừa học vừa phải kiểm tra lại kiến thức cũ. Sau mỗi lớp Attention, thông tin gốc được cộng ngược lại vào kết quả (Residual). Điều này đảm bảo thông tin không bị mất đi hoặc bị biến dạng quá mức khi đi qua hàng chục lớp sâu.

## 3. Giải mã toán học (Conceptual Math)

| Khái niệm | Diễn giải sâu sắc | Vai trò trong mô hình |
| --- | --- | --- |
| **Dot-Product Attention** | Phép nhân ma trận để đo độ tương đồng giữa các từ. | Giống như việc bạn so sánh từ hiện tại với "từ điển" các từ quan trọng trong câu. |
| **Scaling Factor ($1/\sqrt{d_k}$)** | Bộ giảm áp toán học. | Ngăn các con số vọt lên quá lớn, giúp mô hình ổn định và không bị "sốc" trong quá trình học. |
| **Query (Q)** | Một vector biểu diễn "Yêu cầu" của từ hiện tại. | *"Tôi là từ khóa WHERE, tôi cần tìm các biểu thức logic liên quan đến tôi"*. |
| **Key (K)** | Một vector biểu diễn "Nhãn dán" của các từ khác. | *"Tôi là '1'='1', tôi có nội dung logic để khớp với yêu cầu của bạn"*. |
| **Value (V)** | "Giá trị thực" của thông tin. | Sau khi Q và K khớp nhau, thông tin từ V sẽ được trích xuất để đưa vào lớp tiếp theo. |

## 4. Ứng dụng trong SQL Injection Generation
Transformer là "vũ khí hạng nặng" cho bài toán của bạn vì:
1.  **Cấu trúc phân cấp:** SQL có cấu trúc lồng nhau rất phức tạp (Subqueries). Transformer có khả năng hiểu các mối quan hệ lồng nhau này cực tốt nhờ cơ chế Attention tầm xa.
2.  **Khả năng "Học thuộc lòng" cú pháp:** Nó không chỉ sinh ra text, nó sinh ra mã nguồn. Transformer có thể học được luật chơi của SQL (như việc số lượng cột trong `UNION SELECT` phải khớp) chỉ bằng cách nhìn vào hàng triệu mẫu.
3.  **Tấn công theo ngữ cảnh:** Bạn có thể huấn luyện một Transformer để "dịch" một câu SQL bình thường sang một phiên bản Injection tương ứng mà vẫn giữ được logic của ứng dụng.

## 5. Phân tích Chuyên sâu (Advanced Insight)
Trong các mô hình như GPT (Decoder-only), chúng ta sử dụng **Masked Self-Attention**. 
- **Cơ chế:** Khi mô hình đang viết chữ thứ 5, nó bị "bịt mắt" không cho nhìn thấy chữ thứ 6, 7, 8... 
- **Tại sao quan trọng cho SQLi?** Điều này ép mô hình phải học cách dự đoán logic tiếp theo dựa trên những gì nó đã viết. Nếu nó đã viết `OR`, nó phải học cách viết tiếp một biểu thức luôn đúng (Tautology) để hoàn tất cuộc tấn công.

## 6. Kết nối & Mở rộng
- **Mô hình kế thừa:** T5 (Text-to-Text Transfer Transformer) - có thể dùng để biến đổi mọi bài toán bảo mật thành bài toán "dịch ngôn ngữ".
- **Câu hỏi tư duy:** Làm thế nào để điều chỉnh nhiệt độ (Temperature) của Transformer để nó sinh ra các câu SQLi "điên rồ" hơn (Creative) thay vì chỉ lặp lại các mẫu có sẵn?
