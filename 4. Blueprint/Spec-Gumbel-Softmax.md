---
aliases: [Gumbel-Softmax Roadmap]
created: 2026-04-29 05:30:00
progress: research
blueprint: [SQLi-GAN]
tags: [spec, gumbel-softmax, sql-injection, gan]
category: [blueprint]
---

# Technical Roadmap: SQLi-GAN (Gumbel-Softmax Approach)

Bản lộ trình này tập trung vào việc sử dụng kỹ thuật **Gumbel-Softmax Reparameterization** để cho phép truyền đạo hàm qua các token rời rạc trong quá trình huấn luyện đối kháng.

## 🟩 Giai đoạn 1: Thiết lập Dữ liệu & Không gian xác suất
- [ ] **Data Acquisition:** Thu thập 100k mẫu SQL (50% Malicious, 50% Benign).
- [ ] **Vocabulary Construction:** Xây dựng bộ từ vựng $V$ bao gồm các từ khóa SQL, ký tự đặc biệt và các token trừu tượng (`<TABLE>`, `<NUM>`, `<STR>`).
- [ ] **Prior Distribution ($p_z$):** Thiết lập Latent Space dựa trên phân phối Gaussian $\mathcal{N}(0, 1)$ để tối ưu hóa khả năng nội suy cấu trúc.

## 🟨 Giai đoạn 2: Tiền xử lý & Chuẩn hóa
- [ ] **Regex Tokenization:** Tách các chuỗi SQL thành các token nguyên tử (atomic tokens), đảm bảo các ký tự như `'`, `--`, `#` được xử lý độc lập.
- [ ] **Structural Anonymization:** Thực hiện De-lexicalization để chuyển đổi dữ liệu về dạng cấu trúc thuần túy, giảm nhiễu từ các giá trị cụ thể.
- [ ] **Sequence Standardization:** Thực hiện Padding và Truncation về độ dài cố định $L$, sử dụng các special tokens `<SOS>`, `<EOS>`, `<PAD>`.

## 🟧 Giai đoạn 3: Kiến trúc Mô hình (Core Architecture)
- [ ] **Generator ($G$):** 
    - Sử dụng kiến trúc **Transformer Decoder** với cơ chế Self-Attention.
    - **Gumbel-Softmax Layer:** Tích hợp lớp kích hoạt Gumbel-Softmax ở đầu ra để biến đổi phân phối xác suất rời rạc thành các vector liên tục có khả năng truyền đạo hàm.
- [ ] **Discriminator ($D$):** 
    - Sử dụng **1D-CNN** với nhiều kích thước kernel (2, 3, 4, 5) để trích xuất đặc trưng n-gram của payload.
- [ ] **Loss Function:** Triển khai **WGAN-GP** (Wasserstein GAN với Gradient Penalty) để đảm bảo tính ổn định và tránh biến mất đạo hàm.

## 🟥 Giai đoạn 4: Chiến lược Huấn luyện Đối kháng
- [ ] **Maximum Likelihood Pre-training (MLE):** Huấn luyện $G$ như một mô hình ngôn ngữ thông thường để học cú pháp SQL cơ bản trước khi đối kháng.
- [ ] **Temperature Scheduling ($\tau$):** 
    - Thiết lập lộ trình giảm dần nhiệt độ $\tau$ từ 1.0 xuống 0.1.
    - *Mục tiêu:* Bắt đầu với phân phối mềm (soft) để học và kết thúc với phân phối cứng (hard) gần với thực tế.
- [ ] **Adversarial Loop:** Huấn luyện song song $G$ và $D$ với tỉ lệ cập nhật $5:1$.

## 🟦 Giai đoạn 5: Đánh giá & Hậu xử lý
- [ ] **Re-lexicalization Module:** Xây dựng bộ giải mã để thay thế các token trừu tượng bằng giá trị thực tế từ wordlist mục tiêu.
- [ ] **Fidelity & Diversity Metrics:**
    - **Syntax Validity Rate:** Đo tỉ lệ payload viết đúng cú pháp SQL sau khi qua bộ Parser.
    - **Self-BLEU:** Đánh giá mức độ đa dạng của các mẫu sinh ra.
- [ ] **Distribution Matching:** Sử dụng khoảng cách Jensen-Shannon (JS) để đo độ tương đồng giữa phân phối thực tế và phân phối sinh ra.

## 🟪 Giai đoạn 6: Đóng gói & Triển khai
- [ ] **Inference Engine:** Xây dựng pipeline nhận vector nhiễu $z$, thực hiện feed-forward qua $G$, lấy argmax token và thực hiện re-lexicalize.
- [ ] **API Service:** Cung cấp giao diện RESTful API để tích hợp vào các công cụ bảo mật và kiểm thử xâm nhập.
