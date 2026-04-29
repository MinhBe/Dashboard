---
aliases: [Transformer Architecture, Self-Attention Theory]
created: 2026-04-29 02:00:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [foundation, generative-ai, transformer, architecture]
category: [theory]
---
# Foundation: Transformers - Kiến trúc Dựa trên Sự chú ý

## 1. Triết lý Thiết kế (Design Philosophy)
Kiến trúc Transformer, được giới thiệu trong bài báo *"Attention Is All You Need"*, đánh dấu bước ngoặt từ việc xử lý dữ liệu tuần tự (Sequential) sang xử lý song song hoàn toàn (Parallel). 

Triết lý cốt lõi là **Cơ chế Chú ý (Attention Mechanism)**: Cho phép mô hình tính toán mức độ ảnh hưởng của mọi phần tử trong một chuỗi lên một phần tử cụ thể, bất kể khoảng cách vật lý giữa chúng. Điều này giải quyết triệt để vấn đề "nút thắt cổ chai" thông tin và sự suy giảm gradient trong các mô hình cũ như RNN hay LSTM.

## 2. Các Trụ cột Kiến trúc (Architectural Pillars)

### 2.1. Scaled Dot-Product Attention
Đây là cơ chế tính toán trọng số quan trọng nhất. Nó sử dụng ba ma trận: **Query (Q)**, **Key (K)**, và **Value (V)**.
- Quy trình: Lấy tích vô hướng của Q và K, chuẩn hóa bằng căn bậc hai của kích thước vector ($\sqrt{d_k}$), đi qua hàm Softmax để lấy trọng số xác suất, sau đó nhân với V.
- Ý nghĩa: Xác định xem một "truy vấn" (Query) khớp với "khóa" (Key) nào nhất để trích xuất "giá trị" (Value) tương ứng.

### 2.2. Multi-Head Attention
Thay vì thực hiện một phép tính Attention duy nhất, mô hình chia nhỏ các vector thành nhiều phần (Heads) và thực hiện tính toán song song. 
- Mỗi "đầu" sẽ học các cách biểu diễn quan hệ khác nhau trong dữ liệu (ví dụ: một đầu học về cú pháp, một đầu học về ngữ nghĩa).

### 2.3. Positional Encoding
Vì không có cấu trúc lặp (recurrent), mô hình không biết thứ tự của các phần tử. 
- Giải pháp: Sử dụng các hàm sóng Sin và Cosin với tần số khác nhau để mã hóa vị trí vào không gian vector. Điều này tạo ra một "bản đồ vị trí" giúp mô hình phân biệt được sự khác biệt giữa các phần tử ở các khoảng cách khác nhau.

## 3. Giải mã Toán học (Mathematical Foundations)

| Thành phần | Công thức | Diễn giải Bản chất |
| --- | --- | --- |
| **Attention Score** | $\text{Softmax}(\frac{QK^T}{\sqrt{d_k}})V$ | Ma trận trọng số xác định mức độ tập trung vào từng phần tử. |
| **Layer Norm** | $\text{LN}(x + \text{Sublayer}(x))$ | Cơ chế ổn định hóa, giúp dòng thông tin không bị biến dạng khi đi qua nhiều lớp. |
| **Feed-Forward** | $\text{max}(0, xW_1 + b_1)W_2 + b_2$ | Chuyển đổi phi tuyến tính, giúp mô hình học được các hàm phức tạp hơn sau khi đã thu thập thông tin từ Attention. |

## 4. Ưu điểm và Hạn chế Cố hữu

### 4.1. Ưu điểm
- **Tính song song cực cao:** Tối ưu hóa tối đa khả năng tính toán của GPU.
- **Tầm nhìn toàn cục (Global Receptive Field):** Hiểu được mối quan hệ giữa các phần tử ở cách xa nhau hàng nghìn bước.

### 4.2. Hạn chế
- **Chi phí tính toán bậc hai ($O(n^2)$):** Độ phức tạp tăng theo bình phương độ dài chuỗi, khiến việc xử lý các chuỗi cực dài trở nên đắt đỏ.
- **Thiếu định hướng vị trí tự nhiên:** Phụ thuộc hoàn toàn vào chất lượng của Positional Encoding.

## 5. Các Biến thể và Mở rộng
- **Encoder-only (BERT):** Tập trung vào việc hiểu ngữ cảnh từ cả hai phía.
- **Decoder-only (GPT):** Tập trung vào việc dự đoán phần tử tiếp theo trong chuỗi.
- **Encoder-Decoder (T5, BART):** Kết hợp cả hai để thực hiện các nhiệm vụ chuyển đổi phức tạp.
