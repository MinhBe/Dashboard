---
aliases: [RL-SeqGAN Roadmap]
created: 2026-04-29 05:40:00
progress: research
blueprint: [SQLi-GAN]
tags: [spec, reinforcement-learning, seqgan, sql-injection, policy-gradient]
category: [blueprint]
---

# Technical Roadmap: SQLi-GAN (Reinforcement Learning / SeqGAN Approach)

Bản lộ trình này tập trung vào việc mô hình hóa quá trình sinh SQL như một bài toán ra quyết định tuần tự, sử dụng thuật toán **Policy Gradient** để tối ưu hóa khả năng vượt qua các bộ lọc bảo vệ.

## 🟩 Giai đoạn 1: Thiết lập Dữ liệu & Môi trường (Environment)
- [ ] **Data Sourcing:** Thu thập 100k mẫu SQL. Đặc biệt chú trọng vào các mẫu "Bypass thành công" để làm mục tiêu học tập (Expert Trajectories).
- [ ] **Reward Oracle Setup:** Thiết lập các hệ thống đánh giá ngoại vi:
    - SQL Parser (kiểm tra cú pháp).
    - WAF Oracle (ModSecurity/SQLMap) để trả về tín hiệu bypass.
- [ ] **State-Action Space:** Định nghĩa không gian trạng thái (chuỗi token hiện tại) và không gian hành động (chọn token tiếp theo từ từ vựng $V$).

## 🟨 Giai đoạn 2: Tiền xử lý & Trích xuất Đặc trưng
- [ ] **Tokenization & De-lexicalization:** Thực hiện tương tự quy trình chuẩn để giảm không gian hành động, tập trung vào cấu trúc logic tấn công.
- [ ] **Environment Interaction Wrapper:** Xây dựng một lớp trung gian (Wrapper) để Generator có thể "gửi" một payload thử nghiệm, nhận lại phản hồi và cập nhật trạng thái.

## 🟧 Giai đoạn 3: Kiến trúc Mô hình (Agent & Rewarder)
- [ ] **Generator (Policy $\pi$):** 
    - Sử dụng kiến trúc **RNN/LSTM** (truyền thống cho SeqGAN) hoặc **Transformer** để làm Policy mạng thần kinh.
    - Output là một phân phối xác suất trên từ vựng tại mỗi bước thời gian $t$.
- [ ] **Discriminator ($D$):** 
    - Đóng vai trò là hàm phần thưởng (Reward Function). 
    - Sử dụng **CNN** hoặc **Highway Network** để phân biệt payload sinh ra và dữ liệu thật.
- [ ] **Monte Carlo Tree Search (MCTS) / Roll-out:** 
    - Triển khai cơ chế Roll-out để ước lượng giá trị của một sequence chưa hoàn chỉnh, giúp Generator nhận được phần thưởng sớm.

## 🟥 Giai đoạn 5: Chiến lược Huấn luyện (Policy Gradient)
- [ ] **Pre-training (Supervised Phase):** Huấn luyện $G$ bằng Maximum Likelihood Estimation (MLE) để hội tụ nhanh hơn.
- [ ] **Adversarial RL Loop:**
    - Sử dụng thuật toán **REINFORCE** để cập nhật trọng số cho $G$.
    - Cập nhật $D$ định kỳ dựa trên các mẫu "thật" và các mẫu "giả" mà $G$ vừa sinh ra.
- [ ] **Reward Shaping:** Kết hợp phần thưởng từ $D$ với phần thưởng từ Oracle (Cú pháp + Khả năng Bypass).

## 🟦 Giai đoạn 5: Đánh giá & Kiểm thử Hiệu năng
- [ ] **Attack Success Rate (ASR):** Đây là metric quan trọng nhất. Đo tỉ lệ phần trăm payload sinh ra vượt qua được WAF thực tế.
- [ ] **Syntax Integrity:** Đảm bảo >95% payload sinh ra có thể thực thi được trên cơ sở dữ liệu đích.
- [ ] **Reward Convergence:** Theo dõi biểu đồ phần thưởng để đảm bảo Agent đang học cách bypass chứ không chỉ học cách "viết giống SQL".

## 🟪 Giai đoạn 6: Triển khai & Vận hành
- [ ] **Agent Inference:** Generator sinh payload bằng cách lấy mẫu (sampling) từ Policy đã được tối ưu.
- [ ] **Continuous Learning Pipeline:** Hệ thống có khả năng nhận phản hồi từ các cuộc tấn công thực tế để tiếp tục tinh chỉnh Policy (Online Learning).
