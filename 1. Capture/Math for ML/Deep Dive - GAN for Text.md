---
aliases: [TextGAN, SeqGAN, Gumbel-Softmax, RL-GAN]
created: 2026-04-29 01:30:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [deep-dive, generative-ai, gan, reinforcement-learning, sql-injection]
category: [research]
---
# Deep Dive: GAN cho Text - Giải mã Cuộc chiến Rời rạc

## 1. Bản chất của Thất bại: Tại sao GAN truyền thống "sợ" Text?
GAN được thiết kế dựa trên giả định rằng mọi thứ đều là dòng chảy liên tục (như pixel ảnh). 
- **Vấn đề toán học:** Khi Discriminator chê một câu SQL là "fake", nó sẽ gửi một tín hiệu (gradient) bảo Generator: *"Hãy thay đổi giá trị đầu ra của lớp cuối cùng đi một chút"*. 
- **Sự đứt gãy:** Trong ảnh, thay đổi "một chút" có nghĩa là màu sắc đậm lên một tí. Trong text, đầu ra của lớp cuối là xác suất của các từ (ví dụ: `SELECT`: 0.9, `UNION`: 0.1). Nếu bạn thay đổi "một chút", xác suất có thể thành (`SELECT`: 0.89, `UNION`: 0.11). Nhưng khi bạn chọn từ (sampling), nó vẫn sẽ chọn `SELECT`. 
- **Hệ quả:** Generator không thấy sự thay đổi nào ở kết quả cuối cùng, nên nó không biết đường nào mà học. Nó bị kẹt trong một vùng không gian mà mọi hướng đi đều trông giống nhau (Vanishing Gradient).

## 2. Giải pháp 1: Gumbel-Softmax - "Cây cầu" giữa Rời rạc và Liên tục
Gumbel-Softmax không phải là một hàm bình thường, nó là một **phép xấp xỉ**.
- **Cơ chế:** Nó thêm một loại nhiễu đặc biệt (Gumbel noise) vào xác suất của các từ, sau đó dùng một tham số gọi là **Nhiệt độ (Temperature - $\tau$)**.
    - Khi $\tau$ lớn: Các từ có xác suất gần bằng nhau (hỗn loạn).
    - Khi $\tau$ nhỏ: Nó hội tụ về một từ duy nhất (giống hệt chọn từ thật).
- **Ý nghĩa:** Trong quá trình huấn luyện, ta bắt đầu với $\tau$ lớn để Generator có thể "cảm nhận" được gradient từ Discriminator chảy qua tất cả các từ, sau đó giảm dần $\tau$ để mô hình học cách chọn từ chính xác. Đây là cách ta "lừa" toán học để có được đạo hàm trên dữ liệu chữ.

## 3. Giải pháp 2: SeqGAN - Khi GAN trở thành một "Kẻ đánh bạc" có tính toán
Nếu Gumbel-Softmax là "giả vờ liên tục", thì SeqGAN chấp nhận sự rời rạc và giải quyết nó bằng **Reinforcement Learning (Học tăng cường)**.

### 3.1. Bài toán Phần thưởng Trung gian (Intermediate Reward)
Một câu SQL chỉ có ý nghĩa khi nó hoàn tất (ví dụ: có đủ `SELECT` và `FROM`). Nhưng Discriminator chỉ có thể chấm điểm khi câu đã viết xong. Vậy khi Generator mới viết được chữ `SELECT`, làm sao nó biết chữ đó là tốt hay xấu?
- **Giải pháp:** **Monte Carlo Tree Search (MCTS)**. 
- **Cơ chế:** Khi Generator viết đến chữ thứ 3, nó sẽ tự "tưởng tượng" ra hàng trăm cái kết khác nhau cho câu đó (roll-out). Nếu đa số cái kết đó bị Discriminator chấm điểm cao, thì chữ thứ 3 đó được coi là tốt.

### 3.2. Policy Gradient ($\nabla_\theta J(\theta)$)
Thay vì dùng Loss function thông thường, SeqGAN dùng công thức Policy Gradient để cập nhật trọng số. 
- **Ý nghĩa:** Nó không hỏi *"Làm sao để giống dữ liệu thật?"*, mà nó hỏi *"Hành động này mang lại bao nhiêu phần thưởng từ Discriminator?"*. Nếu phần thưởng dương, nó sẽ tăng xác suất thực hiện lại hành động đó trong tương lai.

## 4. Giải mã toán học (Conceptual Math)

| Khái niệm | Diễn giải sâu sắc | Vai trò trong mô hình |
| --- | --- | --- |
| **Differentiable Relaxation** | Làm "mềm" các quyết định cứng nhắc. | Cho phép toán học "nhìn thấy" các lựa chọn thay thế thay vì chỉ nhìn thấy lựa chọn duy nhất. |
| **Expectation ($E$)** | Giá trị kỳ vọng. | Vì chúng ta đang làm việc với xác suất, chúng ta không tối ưu hóa một kết quả, mà tối ưu hóa "trung bình" các kết quả tốt nhất. |
| **Log-Probability ($\log \pi$)** | Độ tin cậy của hành động. | Giúp mô hình nhấn mạnh vào những quyết định mang lại phần thưởng lớn và loại bỏ những quyết định tồi tệ một cách nhanh chóng. |
| **Actor-Critic** | Sự kết hợp giữa "Người thực hiện" và "Người phê bình". | Một cấu trúc nâng cao giúp ổn định quá trình huấn luyện GAN cho text, giảm bớt sự hỗn loạn. |

## 5. Liên hệ bài toán SQL Injection
**Tại sao CWGAN của bạn gặp khó?**
Bạn đang cố gắng bắt một mô hình vốn dành cho số thực xử lý các ký tự SQL. Các ký tự đặc biệt như `'`, `--`, `/*` có ý nghĩa cực lớn trong SQLi nhưng về mặt toán học, chúng chỉ là những con số đứng cạnh nhau.

**Chiến lược nâng cấp cho bạn:**
1.  **Reward Shaping:** Thay vì chỉ để Discriminator chấm điểm 0/1, bạn hãy tích hợp một bộ parser SQL. Nếu câu sinh ra sai cú pháp -> Trừ điểm nặng. Nếu đúng cú pháp nhưng không tấn công được -> Điểm thấp. Nếu bypass được WAF -> Thưởng tối đa.
2.  **Pre-training:** Luôn bắt đầu bằng việc huấn luyện Generator như một mô hình ngôn ngữ thông thường (MLE) để nó học cú pháp SQL trước, sau đó mới đưa vào vòng xoáy GAN để học cách bypass. Đừng để nó "tập bò" và "tập đánh nhau" cùng lúc.

## 6. Kết nối & Mở rộng
- **Mô hình liên quan:** LeakGAN (Generator lấy trộm thông tin từ Discriminator để học tốt hơn).
- **Câu hỏi tư duy:** Làm thế nào để Discriminator không quá mạnh? Nếu Discriminator quá giỏi, nó sẽ "vùi dập" Generator ngay từ đầu và Generator sẽ không bao giờ học được gì (Nash Equilibrium bị phá vỡ).
