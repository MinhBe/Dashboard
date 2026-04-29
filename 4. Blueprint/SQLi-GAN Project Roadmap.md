---
aliases: [SQLi-GAN Roadmap, Project Plan]
created: 2026-04-29 04:30:00
progress: raw
blueprint: [SQLi-GAN]
tags: [roadmap, sql-injection, gan, project-management]
category: [blueprint]
---
# Roadmap: Phát triển Mô hình GAN tạo sinh SQL Injection (Technical Deep Dive)

Lộ trình này được thiết kế dựa trên quy trình AI Lifecycle tiêu chuẩn, tối ưu cho bài toán dữ liệu rời rạc (Text).

## 🟩 Giai đoạn 1: Xác định Bài toán & Dữ liệu (Problem & Data)
*Mục tiêu: Xây dựng nền tảng xác suất $P_{data}$ để mô hình học tập.*

- [ ] **Define Latent Space Prior ($p_z$):** 
    - Lựa chọn phân phối Uniform $[-1, 1]$ hoặc Gaussian $\mathcal{N}(0, 1)$.
    - *Lưu ý:* Gaussian thường giúp Latent Space mượt mà hơn cho việc nội suy.
- [ ] **Data Sourcing (Malicious vs Benign):**
    - Thu thập ít nhất 50k mẫu SQLi (GitHub, Seclists) và 50k mẫu SQL sạch (Log ứng dụng).
    - *Lý do:* Discriminator cần biết "thế nào là SQL sạch" để không bị đánh lừa bởi những chuỗi ký tự vô nghĩa nhưng có từ khóa `SELECT`.
- [ ] **Xây dựng Domain Vocabulary ($V$):**
    - Trích xuất toàn bộ từ khóa SQL, ký tự đặc biệt, và các mẫu bypass phổ biến.
    - Tính toán **Entropy** của tập dữ liệu để đánh giá độ đa dạng ban đầu.

## 🟨 Giai đoạn 2: Tiền xử lý & Khám phá (Preprocessing & EDA)
*Mục tiêu: Chuyển đổi dữ liệu từ dạng người đọc sang dạng Tensor mà không làm mất tính Linear Independence của các đặc trưng.*

- [ ] **SQL-Aware Tokenization (Regex-based):**
    - KHÔNG dùng khoảng trắng đơn thuần. Phải tách được các token nhạy cảm: `'`, `--`, `/*`, `UNION`, `SELECT`.
- [ ] **De-lexicalization (Anonymization):**
    - Thay thế tên bảng cụ thể bằng `<TABLE>`, số bằng `<NUM>`, chuỗi bằng `<STR>`.
    - *Toán học:* Giảm phương sai (Variance) không cần thiết, ép mô hình tập trung vào cấu trúc logic (Manifold) của cuộc tấn công.
- [ ] **Padding & Truncation Semantics:**
    - Quyết định độ dài chuỗi tối đa ($L$). Sử dụng `<PAD>` và `<EOS>`.
- [ ] **EDA - Phân tích đặc trưng:**
    - Vẽ biểu đồ phân phối độ dài chuỗi.
    - Tính toán Cosine Similarity giữa các cụm tấn công để phát hiện các "modes" chính trong dữ liệu.

## 🟧 Giai đoạn 3: Thiết kế Kiến trúc (Modeling)
*Mục tiêu: Giải quyết bài toán "Saddle Point" trong không gian rời rạc.*

- [ ] **Generator ($G$):** 
    - Sử dụng **LSTM** hoặc **GRU** (để tránh Vanishing Gradient) hoặc **Transformer Decoder** (nếu dữ liệu cực dài).
- [ ] **Discriminator ($D$):** 
    - Sử dụng **1D-CNN** với nhiều kích thước filter để bắt các "n-grams" (các cụm từ khóa tấn công đứng cạnh nhau).
- [ ] **Discrete Handling (Chọn 1 trong 2):**
    - [ ] **Gumbel-Softmax:** Sử dụng kỹ thuật Reparameterization để tính đạo hàm qua bước sampling.
    - [ ] **SeqGAN (RL):** Coi $G$ là một Policy $\pi$, sử dụng **Policy Gradient** để cập nhật dựa trên phần thưởng từ $D$.
- [ ] **Loss Function & Regularization:**
    - Triển khai **WGAN-GP (Gradient Penalty)** để đảm bảo tính **Lipschitz Continuity** cho $D$, ngăn chặn Exploding Gradients.

## 🟥 Giai đoạn 4: Huấn luyện & Tối ưu (Training & Tuning)
*Mục tiêu: Đạt được cân bằng Nash (Nash Equilibrium) mà không bị Mode Collapse.*

- [ ] **Pre-training (MLE Phase):**
    - Huấn luyện $G$ như một Language Model thông thường với Cross-Entropy loss. 
    - *Mục tiêu:* Để $G$ biết viết đúng cú pháp SQL trước khi học cách "lừa" $D$.
- [ ] **Adversarial Training Loop:**
    - Thiết lập tỉ lệ huấn luyện $D:G$ (thường là $5:1$).
    - Theo dõi **Gradient Norm** để phát hiện sớm sự mất ổn định.
- [ ] **Temperature Decay ($\tau$):** 
    - Nếu dùng Gumbel-Softmax, lập lịch giảm $\tau$ từ $1.0$ xuống $0.1$ để hội tụ về phân phối Categorical.
- [ ] **Monitor Mode Collapse:** 
    - Kiểm tra phương sai (Variance) của các batch sinh ra. Nếu $G$ chỉ sinh ra 1 mẫu duy nhất -> Tăng Dropout hoặc thêm nhiễu vào Latent Space.

## 🟦 Giai đoạn 5: Đánh giá & Kiểm thử (Evaluation & Validation)
*Mục tiêu: Kiểm chứng tính Fidelity, Diversity và Utility.*

- [ ] **Syntax Validity Rate:** 
    - Sử dụng `sqlparse` để parse thử 1000 mẫu sinh ra. Đạt >80% là thành công.
- [ ] **Self-BLEU Score:** 
    - Đo mức độ lặp lại nội bộ của các mẫu sinh ra. Score thấp = Đa dạng cao.
- [ ] **Red Teaming (Oracle Test):**
    - Chạy các mẫu sinh ra qua **ModSecurity (WAF)**. Tính toán tỉ lệ Bypass thành công.
- [ ] **Latent Space Walk:** 
    - Thay đổi nhẹ vector $z$ để xem các câu SQL biến đổi mượt mà hay nhảy cóc.

## 🟪 Giai đoạn 6: Triển khai & Đóng gói (Deployment)
- [ ] **Model Compression:** Quantization mô hình nếu cần chạy real-time trên Edge.
- [ ] **API Service:** Flask/FastAPI nhận seed và trả về danh sách Payload.

---

## 🔗 Liên kết Kiến thức Toán học (Math Mapping)
- **Jacobian/Hessian:** Dùng để phân tích loss landscape khi mô hình không hội tụ.
- **Lipschitz Continuity:** Thực thi thông qua Gradient Penalty trong WGAN-GP.
- **Expected Value:** Cơ sở của Policy Gradient trong SeqGAN.
- **KL/JS Divergence:** Hiểu bản chất của việc so khớp phân phối $P_G$ và $P_{data}$.
