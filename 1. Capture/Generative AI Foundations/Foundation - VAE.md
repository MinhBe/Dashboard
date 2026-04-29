---
aliases: [VAE, Variational Autoencoder, Latent Variable Models]
created: 2026-04-29 02:15:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [foundation, generative-ai, vae, probability-theory]
category: [theory]
---
# Foundation: Variational Autoencoders (VAE)

## 1. Triết lý Thiết kế (Design Philosophy)
Khác với các Autoencoder thông thường (vốn chỉ là các hàm nén dữ liệu rời rạc), **VAE** là một mô hình tạo sinh dựa trên xác suất. Nó giả định rằng dữ liệu quan sát được ($x$) được sinh ra từ các biến tiềm ẩn ($z$) không quan sát được. 

Mục tiêu của VAE là học được cấu trúc của không gian tiềm ẩn sao cho nó có tính **liên tục (continuity)** và **đầy đủ (completeness)**, cho phép việc lấy mẫu ngẫu nhiên từ không gian này tạo ra được dữ liệu mới có ý nghĩa.

## 2. Các Trụ cột Kiến trúc (Architectural Pillars)

### 2.1. Phân phối Tiềm ẩn (Latent Distribution)
Thay vì ánh xạ đầu vào $x$ tới một vector $z$ cố định, Encoder của VAE ánh xạ $x$ tới các tham số của một phân phối xác suất (thường là Trung bình $\mu$ và Độ lệch chuẩn $\sigma$ của một phân phối Gaussian). 
- Ý nghĩa: Nó tạo ra một "vùng an toàn" xung quanh mỗi điểm dữ liệu thay vì chỉ một điểm duy nhất.

### 2.2. Reparameterization Trick
Đây là kỹ thuật then chốt để có thể huấn luyện mô hình bằng Gradient Descent. 
- Vấn đề: Việc lấy mẫu $z \sim \mathcal{N}(\mu, \sigma)$ là một quá trình ngẫu nhiên không thể tính đạo hàm.
- Giải pháp: Tách $z$ thành $z = \mu + \sigma \odot \epsilon$, với $\epsilon \sim \mathcal{N}(0, 1)$. Lúc này, sự ngẫu nhiên được đẩy sang biến $\epsilon$ cố định, còn $\mu$ và $\sigma$ trở thành các tham số có thể tính đạo hàm.

## 3. Giải mã Toán học (Mathematical Foundations)

| Thành phần | Công thức | Diễn giải Bản chất |
| --- | --- | --- |
| **Evidence Lower Bound (ELBO)** | $\mathcal{L}(\theta, \phi; x) = \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{KL}(q_\phi(z|x) \| p(z))$ | Mục tiêu tối ưu hóa tổng thể của VAE. |
| **Reconstruction Loss** | $\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]$ | Đo lường khả năng tái tạo dữ liệu gốc từ không gian tiềm ẩn (khía cạnh "Autoencoder"). |
| **KL Divergence** | $D_{KL}(q_\phi(z|x) \| p(z))$ | Ép không gian tiềm ẩn phải tuân theo một khuôn mẫu (Prior), thường là phân phối chuẩn đơn vị (khía cạnh "Variational"). |

## 4. Đặc tính của Không gian Tiềm ẩn (Latent Space)

- **Tính liên tục:** Hai điểm gần nhau trong không gian tiềm ẩn sẽ tạo ra hai kết quả đầu ra tương tự nhau.
- **Tính đầy đủ:** Bất kỳ điểm nào được lấy mẫu từ không gian tiềm ẩn cũng sẽ tạo ra một kết quả đầu ra hợp lý (nếu mô hình được huấn luyện tốt).

## 5. Hạn chế Cố hữu

- **Hiện tượng "Blurry":** Do sử dụng Reconstruction Loss dựa trên khoảng cách (như MSE), kết quả đầu ra của VAE thường bị mờ, thiếu sắc nét so với GAN.
- **Posterior Collapse:** Khi Decoder quá mạnh, nó có thể phớt lờ hoàn toàn thông tin từ biến tiềm ẩn $z$, khiến mô hình mất đi tính liên kết giữa đầu vào và đầu ra.

## 6. Các Biến thể và Mở rộng
- **Beta-VAE:** Điều chỉnh trọng số của KL Divergence để tách biệt các đặc trưng (Disentanglement).
- **CVAE (Conditional VAE):** Thêm thông tin điều kiện để kiểm soát loại dữ liệu được sinh ra.
- **VQ-VAE (Vector Quantized VAE):** Sử dụng không gian tiềm ẩn rời rạc, cực kỳ hiệu quả cho việc nén ảnh và âm thanh.
