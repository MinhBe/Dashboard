---
aliases: [Diffusion, DDPM, Score-based Generative Modeling]
created: 2026-04-29 01:45:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [deep-dive, generative-ai, diffusion, advanced-math]
category: [research]
---
# Deep Dive: Diffusion Models - Nghệ thuật Khử nhiễu và Sự trỗi dậy của Trật tự

## 1. Bản chất Triết học: Từ Entropy đến Cấu trúc
Diffusion Model không cố gắng bắt chước dữ liệu một cách trực tiếp như GAN. Thay vào đó, nó học quy luật vật lý của sự hủy diệt và tái sinh. 
- **Triết lý:** Mọi dữ liệu có cấu trúc (như một câu lệnh SQL hoàn chỉnh) đều là một trạng thái có **Entropy thấp** (trật tự cao). Khi ta thêm nhiễu, ta đang tăng Entropy cho đến khi trật tự biến mất hoàn toàn. 
- **Công việc của AI:** Học cách đi ngược lại chiều mũi tên của thời gian, từ sự hỗn loạn (Entropy cao) tìm đường quay về trật tự (Entropy thấp).

## 2. Cơ chế Vận hành Chuyên sâu

### 2.1. Forward Diffusion (Quá trình Khuếch tán Thuận)
Đây là một chuỗi Markov (Markov Chain). Tại mỗi bước, ta thêm một chút nhiễu Gaussian $\epsilon$ vào dữ liệu $x_t$. 
- **Đặc điểm:** Quá trình này không có tham số để học. Nó tuân theo một lịch trình (Schedule) cố định. Sau khoảng 1000 bước, bất kỳ câu SQL nào cũng sẽ trở thành nhiễu trắng hoàn toàn.
- **Ý nghĩa:** Nó thiết lập một "con đường" để mô hình biết cách quay về nhà.

### 2.2. Reverse Diffusion (Quá trình Khuếch tán Ngược)
Đây là nơi phép màu xảy ra. AI không cần phải "vẽ" ra cả câu SQL ngay lập tức. Nó chỉ cần thực hiện một nhiệm vụ cực kỳ đơn giản: **Đoán xem bước nhiễu vừa rồi là gì**.
- **Score-based Modeling:** Mô hình học một hàm gọi là "Score Function" - nó giống như một bản đồ địa hình. Tại mỗi điểm trong không gian nhiễu, Score Function chỉ ra hướng nào là hướng có mật độ dữ liệu cao nhất (nơi có khả năng chứa các câu SQL hợp lệ).
- **Lợi thế:** Vì nhiệm vụ là "khử nhiễu" (một bài toán Regression đơn giản), quá trình training cực kỳ ổn định, không bị hiện tượng "đối đầu" gây sụp đổ như GAN.

## 3. Giải mã toán học (Conceptual Math)

| Khái niệm | Diễn giải sâu sắc | Vai trò trong mô hình |
| --- | --- | --- |
| **Langevin Dynamics** | Quá trình di chuyển trong sương mù. | Phương pháp giúp mô hình "dò dẫm" từ vùng nhiễu về vùng dữ liệu sạch dựa trên Score Function. |
| **Variational Bound (VLB)** | Giới hạn dưới của xác suất. | Một công cụ toán học để tối ưu hóa quá trình khử nhiễu, đảm bảo câu SQL sinh ra có xác suất xuất hiện cao nhất trong thực tế. |
| **Signal-to-Noise Ratio (SNR)** | Tỉ lệ tín hiệu trên nhiễu. | Quyết định xem tại bước nào mô hình cần tập trung vào cấu trúc tổng thể (SQL keywords) và bước nào tập trung vào chi tiết (dấu nháy, khoảng cách). |
| **U-Net / Transformer Backbone** | Cỗ máy dự đoán nhiễu. | Cấu trúc mạng nơ-ron có khả năng xử lý dữ liệu ở nhiều cấp độ phân giải/chi tiết khác nhau. |

## 4. Ứng dụng trong SQL Injection Generation
Diffusion đang trở thành ứng cử viên sáng giá cho dữ liệu cấu trúc nhờ các kỹ thuật mới:
1.  **Latent Diffusion cho SQL:** Thay vì khử nhiễu trực tiếp trên chữ cái (rất khó), người ta dùng một Encoder để biến SQL thành các vector số (giống VAE), sau đó khử nhiễu trên các vector đó. Cuối cùng dùng Decoder để biến vector sạch thành câu SQLi.
2.  **Guided Generation (Tạo sinh có hướng dẫn):** Bạn có thể "thì thầm" vào tai mô hình Diffusion trong lúc nó đang khử nhiễu: *"Hãy hướng về phía các câu lệnh có chứa từ khóa UNION"*. Mô hình sẽ bẻ lái quá trình khử nhiễu để kết quả cuối cùng hội tụ về đúng loại tấn công bạn cần.
3.  **Sự đa dạng tuyệt đối:** Diffusion không bị Mode Collapse. Nó có thể sinh ra hàng triệu câu SQLi với cấu trúc khác nhau hoàn toàn, giúp bạn kiểm thử WAF một cách toàn diện hơn bất kỳ phương pháp nào khác.

## 5. Phân tích Chuyên sâu: Thách thức của dữ liệu Rời rạc
Dữ liệu SQL là rời rạc, trong khi Diffusion hoạt động trên số thực.
- **Giải pháp:** **Bit Diffusion** hoặc **Analog Bits**. Chúng ta biểu diễn các ký tự SQL dưới dạng nhị phân (0 và 1), sau đó coi các số 0, 1 đó là số thực và thêm nhiễu vào chúng. Khi khử nhiễu xong, ta chỉ cần làm tròn về 0 hoặc 1 để lấy lại ký tự ban đầu.

## 6. Kết nối & Mở rộng
- **Mô hình liên quan:** Classifier-Free Guidance (giúp điều khiển mô hình mà không cần huấn luyện thêm bộ phân loại).
- **Câu hỏi tư duy:** Nếu ta coi việc "bypass WAF" là một loại trật tự, liệu ta có thể huấn luyện Diffusion để nó coi "nhiễu" là SQL bình thường và "dữ liệu sạch" là SQL Injection không?
