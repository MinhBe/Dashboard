---
aliases: [Evaluation Metrics, Generative AI Assessment, Quality Control]
created: 2026-04-29 04:15:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [foundation, evaluation, metrics, generative-ai]
category: [theory]
---
# Foundation: Phương pháp Đánh giá Chất lượng Dữ liệu Output

Đánh giá dữ liệu tạo sinh (Generative Output) khó hơn nhiều so với dữ liệu phân loại vì không có một đáp án đúng duy nhất. Chúng ta cần đánh giá dựa trên 3 trụ cột: **Tính trung thực (Fidelity)**, **Tính đa dạng (Diversity)** và **Tính hữu dụng (Utility)**.

## 1. Các Trụ cột Đánh giá

### Trụ cột 1: Tính trung thực (Fidelity / Quality)
Dữ liệu sinh ra có giống thật hay không? Cú pháp có đúng hay không?
- **Statistical Alignment:** Dữ liệu sinh ra phải có cùng phân phối thống kê với dữ liệu thật.
- **Validity:** Dữ liệu có tuân thủ các quy tắc cứng nhắc của miền dữ liệu hay không (ví dụ: Đúng cú pháp SQL).

### Trụ cột 2: Tính đa dạng (Diversity)
Mô hình có sinh ra được nhiều mẫu khác nhau hay chỉ lặp lại một vài mẫu "an toàn"?
- **Entropy:** Đo lường mức độ hỗn loạn/phong phú của tập dữ liệu sinh ra.
- **Mode Coverage:** Kiểm tra xem mô hình có bao phủ được tất cả các kiểu dữ liệu có trong dataset gốc hay không.

### Trụ cột 3: Tính hữu dụng (Utility)
Dữ liệu sinh ra có dùng được cho mục đích tiếp theo hay không? (Ví dụ: Có bypass được WAF hay không?).

## 2. Các Phương pháp Đánh giá Cụ thể

### 2.1. Chỉ số Thống kê (Statistical Metrics)
- **FID (Frechet Inception Distance):** So sánh khoảng cách giữa hai phân phối (Thật vs Giả) trong không gian vector. FID càng thấp, dữ liệu càng giống thật.
- **Precision & Recall cho Generative AI:** 
    - **Precision:** Tỉ lệ dữ liệu giả trông giống thật.
    - **Recall:** Khả năng mô hình bao phủ được toàn bộ sự đa dạng của dữ liệu thật.

### 2.2. Đánh giá dựa trên Mô hình (Model-based Evaluation)
- **Discriminator Loss:** Trong GAN, giá trị mất mát của Discriminator chính là một thước đo. Nếu D không thể phân biệt được, tức là G đã làm rất tốt.
- **LLM-as-a-judge:** Sử dụng một mô hình lớn hơn (như GPT-4) để chấm điểm chất lượng của dữ liệu sinh ra dựa trên các tiêu chí (rubrics) định sẵn.
- **Perplexity (Độ hỗn loạn):** Đo lường mức độ tự tin của một mô hình ngôn ngữ khi đọc dữ liệu sinh ra. Perplexity thấp thường đi kèm với độ trôi chảy cao.

### 2.3. Đánh giá đặc thù theo Miền (Domain-specific Metrics)
- **Syntax Checkers:** Sử dụng các bộ Parser (như `sqlparse`) để đếm tỉ lệ câu lệnh hợp lệ về mặt cú pháp.
- **Semantic Similarity:** So sánh ý nghĩa logic giữa câu gốc và câu sinh ra (thường dùng Cosine Similarity trên các vector embedding).

## 3. Ma trận Đánh giá Tổng hợp

| Phương pháp | Ưu điểm | Nhược điểm |
| --- | --- | --- |
| **Statistical (FID/IS)** | Khách quan, tự động hoàn toàn. | Đôi khi không phản ánh đúng cảm nhận của con người hoặc logic ngữ nghĩa. |
| **Model-based** | Hiểu được ngữ cảnh và logic phức tạp. | Tốn kém tài nguyên, bản thân mô hình giám khảo cũng có thể bị sai. |
| **Human Eval** | Chính xác nhất về mặt cảm nhận. | Chậm, đắt đỏ, không thể thực hiện ở quy mô lớn. |
| **Rule-based (Parser)** | Tuyệt đối chính xác về cú pháp. | Không đánh giá được tính sáng tạo hay mức độ tinh vi. |

## 4. Quy trình Đánh giá Tiêu chuẩn
1.  **Lọc cú pháp:** Loại bỏ ngay các kết quả không hợp lệ về mặt cấu trúc (Rule-based).
2.  **Đo lường phân phối:** So sánh tập dữ liệu sinh ra với dataset gốc (FID/Statistical).
3.  **Kiểm tra tính đa dạng:** Đảm bảo không bị Mode Collapse.
4.  **Thực nghiệm mục tiêu:** Đưa dữ liệu vào môi trường thật (ví dụ: Test tấn công) để đo lường hiệu quả cuối cùng.
