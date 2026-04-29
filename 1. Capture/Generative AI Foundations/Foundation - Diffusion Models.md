---
aliases: [Diffusion, Score-based Modeling, DDPM]
created: 2026-04-29 02:45:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [foundation, generative-ai, diffusion, thermodynamics]
category: [theory]
---
# Foundation: Diffusion Models

## 1. Triết lý Thiết kế (Design Philosophy)
Diffusion Models lấy cảm hứng từ **Nhiệt động lực học (Thermodynamics)**, cụ thể là quá trình khuếch tán của các phân tử khí. 

Triết lý cốt lõi là sự phá hủy và tái thiết thông tin:
- Nếu ta dần dần thêm nhiễu vào dữ liệu cho đến khi nó trở thành nhiễu trắng hoàn toàn (Forward process), ta có thể huấn luyện một mạng nơ-ron để học cách đảo ngược quá trình đó (Reverse process). 
- Bằng cách học cách "khử nhiễu", mô hình thực chất đang học được cấu trúc phân phối của dữ liệu gốc.

## 2. Các Trụ cột Kiến trúc (Architectural Pillars)

### 2.1. Forward Diffusion (Hủy hoại)
Đây là một chuỗi các bước thêm nhiễu Gaussian cố định. Không có tham số học tập ở đây. Quá trình này biến đổi dữ liệu từ phân phối phức tạp của thế giới thực về một phân phối chuẩn đơn giản.
- Khái niệm quan trọng: **Markov Chain** - trạng thái tiếp theo chỉ phụ thuộc vào trạng thái ngay trước đó.

### 2.2. Reverse Diffusion (Tái thiết)
Mô hình AI (thường sử dụng kiến trúc U-Net hoặc Transformer) đóng vai trò dự đoán lượng nhiễu đã được thêm vào ở mỗi bước.
- Thay vì dự đoán hình ảnh sạch ngay lập tức, nó dự đoán **Score function** - vector chỉ hướng đi về vùng có mật độ dữ liệu cao hơn.

## 3. Giải mã Toán học (Mathematical Foundations)

| Thành phần | Công thức | Diễn giải Bản chất |
| --- | --- | --- |
| **Diffusion Kernel** | $q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t}x_{t-1}, \beta_t \mathbf{I})$ | Quy luật toán học của việc thêm nhiễu qua từng bước $t$. |
| **Reparameterized Forward** | $x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t}\epsilon$ | Công thức cho phép tính trực tiếp trạng thái tại bất kỳ bước $t$ nào từ dữ liệu gốc $x_0$. |
| **Denoising Score Matching** | $\mathcal{L} = \mathbb{E}_{x_0, \epsilon} [ \| \epsilon - \epsilon_\theta(x_t, t) \|^2 ]$ | Hàm mất mát: AI cố gắng đoán đúng loại nhiễu $\epsilon$ đã được trộn vào dữ liệu. |

## 4. Đặc tính nổi bật

- **Tính ổn định (Stability):** Khác với GAN, Diffusion không có quá trình đối đầu, nên việc huấn luyện rất ổn định và hội tụ tốt hơn.
- **Độ đa dạng mẫu (Sample Diversity):** Khả năng phủ sóng toàn bộ phân phối dữ liệu cực tốt, tránh được hiện tượng Mode Collapse.
- **Khả năng điều khiển:** Thông qua các kỹ thuật như **Guidance**, ta có thể điều khiển quá trình khử nhiễu để sinh ra dữ liệu theo ý muốn mà không cần huấn luyện lại toàn bộ mô hình.

## 5. Hạn chế Cố hữu

- **Tốc độ sinh (Inference Speed):** Do phải chạy qua hàng trăm đến hàng nghìn bước khử nhiễu, Diffusion chậm hơn GAN gấp nhiều lần.
- **Chi phí lưu trữ:** Cần lưu trữ nhiều trạng thái trung gian trong quá trình huấn luyện.

## 6. Các Biến thể và Mở rộng
- **DDIM (Denoising Diffusion Implicit Models):** Cho phép bỏ qua một số bước khử nhiễu để tăng tốc độ sinh dữ liệu mà không làm giảm quá nhiều chất lượng.
- **Latent Diffusion (như Stable Diffusion):** Thực hiện quá trình khuếch tán trong không gian tiềm ẩn (Latent space) thay vì không gian dữ liệu gốc, giúp giảm cực lớn chi phí tính toán.
- **Classifier-free Guidance:** Kỹ thuật điều khiển mô hình sinh dữ liệu theo các gợi ý (prompts) mà không cần một bộ phân loại phụ trợ.
