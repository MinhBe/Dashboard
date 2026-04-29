---
aliases: [SQLi-GAN Technical Specification, Deep Dive Spec]
created: 2026-04-29 05:20:00
progress: research
blueprint: [SQLi-GAN]
tags: [technical-spec, gan, sql-injection, machine-learning, cybersecurity]
category: [blueprint]
---

# Technical Specification: SQLi-GAN Deep Dive

Tài liệu này chi tiết hóa các bước thực hiện trong Roadmap, tập trung vào các giải pháp kỹ thuật cụ thể để giải quyết bài toán tạo sinh SQL Injection bằng mô hình GAN.

## 🟩 Giai đoạn 1: Xác định Bài toán & Dữ liệu (Problem & Data)

### 1.1. Define Latent Space Prior ($p_z$)
- **Thiết kế:** Sử dụng vector $z \in \mathbb{R}^{128}$ phân phối Gaussian $\mathcal{N}(0, 1)$.
- **Kỹ thuật:** Áp dụng *Spherical Linear Interpolation (Slerp)* khi lấy mẫu để đảm bảo sự chuyển đổi mượt mà giữa các điểm trong không gian mã, giúp sinh ra các biến thể payload có tính kế thừa cấu trúc.

### 1.2. Data Sourcing & Cleaning
- **Xử lý nhiễu:** Loại bỏ các mẫu có độ dài token quá ngắn (< 3) hoặc chỉ chứa các ký tự đơn lẻ không có tính logic tấn công.
- **Cân bằng:** Duy trì tỉ lệ Benign:Malicious là 1:1. Dữ liệu Benign giúp Discriminator học được cấu trúc SQL chuẩn, từ đó ép Generator phải tạo ra các payload "trông giống SQL thật" hơn.
- **Deduplication:** Sử dụng **MinHash LSH** để đảm bảo tập dữ liệu huấn luyện đa dạng về mặt cấu trúc, tránh việc mô hình học thuộc lòng các mẫu lặp lại.

### 1.3. Domain Vocabulary ($V$)
- **Phân loại Vocab:**
    1. **Keywords:** `SELECT`, `UNION`, `WHERE`, `AND`, `OR`.
    2. **Attack Tokens:** `--`, `/*`, `@@version`, `SLEEP()`, `BENCHMARK()`.
    3. **Abstraction Tokens:** `<TABLE>`, `<NUM>`, `<STR>`, `<COL>`.
- **Phân tích:** Tính toán **Information Gain** cho từng token để xác định mức độ quan trọng của chúng trong việc phân biệt payload tấn công và payload sạch.

---

## 🟨 Giai đoạn 2: Tiền xử lý & Khám phá (Preprocessing & EDA)

### 2.1. SQL-Aware Tokenization
- **Phương pháp:** Sử dụng Regular Expressions kết hợp với bộ luật của `sqlparse`. 
- **Đặc điểm:** Tách rời các ký tự đặc biệt đứng sát nhau (ví dụ: `'OR'1'='1'` $\to$ `['OR', "'", '1', "'", '=', "'", '1', "'"]`) để mô hình hiểu được cấu trúc cú pháp thay vì coi đó là một chuỗi đơn lẻ.

### 2.2. De-lexicalization (Anonymization)
- **Cơ chế:**
    - Thay thế hằng số $\to$ `<NUM>`.
    - Thay thế giá trị chuỗi $\to$ `<STR>`.
    - Thay thế tên định danh (bảng, cột) $\to$ `<TABLE>`/`<COL>`.
- **Toán học:** Giúp giảm **Sparse Data Problem**, tập trung vào phân phối xác suất của cấu trúc (structural distribution) thay vì phân phối của các giá trị cụ thể.

### 2.3. EDA & Embedding Analysis
- **Visualization:** Sử dụng **UMAP** để chiếu dữ liệu lên không gian 2D, kiểm tra xem các loại tấn công (Union, Boolean, Time) có tạo thành các cụm (clusters) rõ ràng hay không.

---

## 🟧 Giai đoạn 3: Thiết kế Kiến trúc (Modeling)

### 3.1. Generator ($G$) - Transformer Decoder
- **Cấu trúc:** 4-6 layers, multi-head attention (8 heads).
- **Lý do:** Transformer bắt được các phụ thuộc xa (long-range dependencies) tốt hơn LSTM, đặc biệt quan trọng cho các câu lệnh SQL phức tạp có nhiều cặp ngoặc lồng nhau.

### 3.2. Discriminator ($D$) - Multi-Scale 1D-CNN
- **Filters:** Kích thước [2, 3, 4, 5] để bắt các n-grams đặc trưng.
- **Global Max Pooling:** Trích xuất các đặc trưng mạnh nhất từ mỗi filter để đưa vào lớp phân loại cuối cùng.

### 3.3. Discrete Handling: Gumbel-Softmax
- **Tác dụng:** Cho phép tính toán gradient thông qua các bước lấy mẫu rời rạc (sampling) bằng kỹ thuật reparameterization. 
- **Schedules:** Giảm dần tham số nhiệt độ $\tau$ (Temperature) để dần dần chuyển từ phân phối liên tục sang phân phối rời rạc (one-hot).

### 3.4. Loss Function: WGAN-GP
- **Mục tiêu:** Sử dụng khoảng cách Wasserstein để đo lường sự khác biệt giữa hai phân phối. 
- **Gradient Penalty:** Ràng buộc gradient của $D$ để đảm bảo tính **1-Lipschitz continuity**, ngăn chặn tình trạng Discriminator quá mạnh dẫn đến Generator không học được gì.

---

## 🟥 Giai đoạn 4: Huấn luyện & Tối ưu (Training & Tuning)

### 4.1. MLE Pre-training
- Huấn luyện Generator độc lập như một mô hình ngôn ngữ (Language Model) để đảm bảo nó nắm vững cú pháp SQL cơ bản (viết đúng `SELECT`, `FROM`, `WHERE`) trước khi bước vào giai đoạn đối kháng.

### 4.2. Adversarial Training Balance
- **Tỉ lệ $D:G$:** Thường là 5:1. 
- **TTUR:** Thiết lập tốc độ học (learning rate) khác nhau cho $D$ và $G$ để đạt được điểm cân bằng Nash ổn định hơn.

---

## 🟦 Giai đoạn 5: Đánh giá & Kiểm thử (Evaluation & Validation)

### 5.1. Module Re-lexicalization (Hậu xử lý)
- **Logic:** Chèn các giá trị thực từ một wordlist (target-specific) vào các vị trí `<TABLE>`, `<NUM>`, `<STR>`.
- **Validation:** Chạy qua một bộ SQL Parser để loại bỏ các payload sai cú pháp trầm trọng sau khi điền giá trị.

### 5.2. Domain-specific Metrics
1. **ACC (Attack Category Coverage):** Sử dụng classifier để đo xem mô hình có sinh đủ các loại tấn công khác nhau không (tránh Mode Collapse vào mỗi `OR 1=1`).
2. **ASD (AST Structural Diversity):** So sánh cây cú pháp (AST) của các payload sinh ra. ASD cao nghĩa là mô hình tạo ra các logic tấn công mới, không chỉ đổi tên bảng/số.
3. **OBD (Oracle Bypass Diversity):** Đánh giá hiệu quả thực tế bằng cách đếm số lượng Rule ID bị kích hoạt trên ModSecurity. Mục tiêu là kích hoạt càng nhiều Rule ID khác nhau càng tốt (biểu hiện của sự đa dạng trong kỹ thuật bypass).

---

## 🟪 Giai đoạn 6: Triển khai & Đóng gói (Deployment)

### 6.1. API & Integration
- Đóng gói mô hình thành một microservice nhận vector $z$ và trả về danh sách payload đã qua bước Re-lexicalization.
- Tích hợp vào quy trình CI/CD để tự động kiểm thử WAF mỗi khi có thay đổi cấu hình hệ thống.

---

## 🔗 Math Reference Table
| Khái niệm | Ứng dụng trong SQLi-GAN |
| :--- | :--- |
| **JS Divergence** | Đo độ lệch giữa payload sinh ra và payload thật (dễ gây Vanishing Gradient). |
| **Wasserstein Distance** | Cải thiện độ ổn định, cho phép $D$ cung cấp gradient hữu ích ngay cả khi hai phân phối không giao nhau. |
| **Hessian Matrix** | Sử dụng để phân tích độ cong của loss landscape, giúp điều chỉnh learning rate tối ưu. |
| **Entropy** | Theo dõi độ đa dạng của batch sinh ra để phát hiện sớm hiện tượng Mode Collapse. |
