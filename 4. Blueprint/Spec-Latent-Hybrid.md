---
aliases: [Latent-Hybrid Roadmap]
created: 2026-04-29 05:50:00
progress: research
blueprint: [SQLi-GAN]
tags: [spec, latent-space, hybrid-gan, feature-matching, vae]
category: [blueprint]
---

# Technical Roadmap: SQLi-GAN (Latent / Hybrid Approach)

Bản lộ trình này tập trung vào việc học một biểu diễn ngữ nghĩa (Semantic Representation) của SQL Injection trong không gian ẩn, kết hợp sức mạnh của Variational Autoencoders (VAE) và GAN để tạo ra các payload có tính sáng tạo cao.

## 🟩 Giai đoạn 1: Thiết lập Dữ liệu & Semantic Mapping
- [ ] **Large-scale Data Collection:** Thu thập tập dữ liệu lớn (>200k mẫu) để mô hình học được cấu trúc phân tầng của ngôn ngữ SQL.
- [ ] **Attribute Labeling:** Gán nhãn các thuộc tính tấn công (ví dụ: `is_union`, `is_blind`, `has_sleep`) để hỗ trợ việc điều hướng trong không gian ẩn (Controlled Generation).
- [ ] **Latent Dimension Selection:** Xác định kích thước vector ẩn $z$ (thường từ 256-512) để đủ sức chứa các biến thể ngữ nghĩa phức tạp.

## 🟨 Giai đoạn 2: Tiền xử lý & Feature Engineering
- [ ] **Advanced Tokenization:** Sử dụng Byte-Pair Encoding (BPE) hoặc SQL-specific Tokenization để xử lý các từ vựng mở rộng.
- [ ] **Normalization:** Chuyển đổi dữ liệu về dạng chuẩn nhưng giữ lại các đặc trưng ngữ nghĩa quan trọng (không chỉ là anonymization đơn thuần).
- [ ] **Feature Extraction:** Sử dụng các bộ trích xuất đặc trưng (như BERT-based encoder) để tạo ra các vector khởi tạo cho không gian latent.

## 🟧 Giai đoạn 3: Kiến trúc Mô hình (Hybrid VAE-GAN)
- [ ] **Encoder ($E$):** Nén các câu SQL thực tế thành các phân phối trong không gian ẩn $z \sim q(z|x)$.
- [ ] **Generator/Decoder ($G$):** Giải mã vector ẩn $z$ ngược lại thành chuỗi token SQL.
- [ ] **Discriminator ($D$):** 
    - Thực hiện **Feature Matching**: So sánh các đặc trưng lớp ẩn của payload thật và payload sinh ra (thay vì chỉ so sánh output cuối cùng).
- [ ] **Hybrid Loss:** Kết hợp Reconstruction Loss (VAE), KL-Divergence, và Adversarial Loss (GAN).

## 🟥 Giai đoạn 4: Huấn luyện & Khám phá Không gian ẩn
- [ ] **Joint Training:** Huấn luyện đồng thời Autoencoder và GAN để đảm bảo không gian latent vừa mượt mà (smooth) vừa có tính phân biệt (discriminative).
- [ ] **Latent Space Regularization:** Sử dụng các kỹ thuật như *Label Conditioned Latent* để có thể sinh payload theo yêu cầu (ví dụ: "Sinh cho tôi một câu Union-based").
- [ ] **Warm-up Phase:** Huấn luyện VAE trước để ổn định không gian ẩn trước khi đưa Discriminator vào cuộc.

## 🟦 Giai đoạn 5: Đánh giá & Khả năng Nội suy
- [ ] **Latent Interpolation (Latent Walk):** Kiểm tra xem khi thay đổi dần vector $z$, câu lệnh SQL có biến đổi logic một cách tuần tự hay không (ví dụ: tăng dần độ phức tạp của câu lệnh).
- [ ] **Reconstruction Accuracy:** Đo khả năng mô hình tái tạo lại đúng các mẫu dữ liệu gốc từ không gian ẩn.
- [ ] **Semantic Diversity:** Sử dụng các phương pháp đo khoảng cách vector (Cosine Similarity) để đảm bảo các payload sinh ra bao phủ toàn bộ không gian tấn công.

## 🟪 Giai đoạn 6: Triển khai & Ứng dụng Sáng tạo
- [ ] **Semantic Search Interface:** Cho phép người dùng tìm kiếm hoặc sinh ra các biến thể của một payload có sẵn thông qua việc điều chỉnh vector ẩn.
- [ ] **High-Fidelity Payload API:** Cung cấp các payload có cấu trúc phức tạp và tinh vi, khó bị phát hiện bởi các hệ thống bảo mật dựa trên signature truyền thống.
