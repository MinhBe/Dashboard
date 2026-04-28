---
aliases: [VAE, Variational Autoencoder]
created: 2026-04-28 23:45:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [deep-dive, generative-ai, vae, sql-injection]
category: [research]
---
# Deep Dive: VAE - Nghệ thuật Nén và Tái tạo

## 1. Bản chất cốt lõi (Core Intuition)
Hãy tưởng tượng bạn có 1000 câu lệnh SQL Injection. Thay vì lưu từng câu một, bạn cố gắng tìm ra "công thức chung" của chúng. 
Ví dụ: Hầu hết đều có dấu `'`, từ khóa `OR`, và phép so sánh `1=1`.

**VAE** giống như một máy nén thông minh:
- Nó nén câu SQL cồng kềnh thành một vài con số (đ tọa độ trong không gian).
- Sau đó, nó thử giải nén những con số đó để xem có ra lại đúng câu SQL ban đầu không.

**Nỗi đau giải quyết:** Nếu bạn chỉ copy-paste SQLi, bạn chỉ có bấy nhiêu đó. VAE giúp bạn tìm ra "khoảng trống" giữa các câu SQLi đã biết để tạo ra những câu mới "tương tự nhưng khác biệt".

## 2. Cách thức vận hành (How it works)
VAE gồm 2 phần đối nghịch nhưng hỗ trợ nhau:
1.  **Encoder (Máy nén):** Biến câu SQL thành một phân phối xác suất (thường là hình chuông - Gaussian) trong một không gian gọi là **Latent Space**.
2.  **Decoder (Máy giải nén):** Lấy một điểm bất kỳ trong không gian đó và biến nó thành một câu SQL hoàn chỉnh.

Điểm khác biệt của VAE so với Autoencoder thường là nó không nén thành 1 điểm cố định, mà nén thành một **vùng**. Điều này giúp không gian tiềm ẩn trở nên liên tục, cho phép bạn "dạo chơi" trong đó để sinh dữ liệu.

## 3. Giải mã công thức (Math Decoded)

| Công thức | Ý nghĩa "tiếng người" | Tại sao quan trọng? |
| --- | --- | --- |
| **Latent Space (z)** | "Căn phòng chứa ý tưởng". | Nơi chứa các đặc trưng cốt lõi của SQLi dưới dạng số. |
| **KL Divergence** | "Hình phạt cho sự bừa bãi". | Ép các điểm dữ liệu phải nằm gọn gàng xung quanh tâm, không được bay lung tung, giúp việc sinh dữ liệu dễ dàng hơn. |
| **Reconstruction Loss** | "Sai số khi vẽ lại". | Đảm bảo rằng sau khi nén và giải nén, câu SQL sinh ra vẫn phải giữ được "linh hồn" của câu gốc. |
| **Reparameterization Trick** | "Mẹo lách luật". | Cho phép máy tính tính toán được gradient (đạo hàm) qua các bước ngẫu nhiên. Nếu không có cái này, mô hình không thể học được. |

## 4. Liên hệ bài toán SQL Injection
**Tại sao bạn cần VAE cho SQLi?**
- **Data Augmentation:** Từ 100 mẫu SQLi thủ công, VAE có thể sinh ra 10,000 mẫu biến thể khác nhau về mặt hình thức nhưng cùng mục đích tấn công.
- **Anomalous Discovery:** Giúp tìm ra các cấu trúc SQLi "lạ" mà WAF chưa được học.
- **Kết hợp với GAN:** Bạn có thể dùng VAE để tạo ra các điểm đầu vào (noise) "chất lượng cao" cho Generator của GAN thay vì dùng noise ngẫu nhiên.

**Nhược điểm:**
- Dữ liệu sinh ra đôi khi bị "mờ" hoặc không chuẩn cú pháp hoàn toàn (vì nó ưu tiên tính liên tục của không gian hơn là tính chính xác tuyệt đối của từng ký tự).

## 5. Kết nối & Mở rộng (Connections)
- **Mô hình liên quan:** Autoencoder (AE), Beta-VAE (kiểm soát độ sáng tạo).
- **Câu hỏi mở:** Làm sao để ép VAE chỉ sinh ra các câu SQL "hợp lệ" về mặt cú pháp (valid SQL syntax)?

## 6. Tài liệu tham khảo
- Paper: "Auto-Encoding Variational Bayes" (2013).
- Blog: Variational Autoencoders Explained (Towards Data Science).
