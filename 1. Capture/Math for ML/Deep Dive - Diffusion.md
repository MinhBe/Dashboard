---
aliases: [Diffusion, Score-based Models]
created: 2026-04-29 00:15:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [deep-dive, generative-ai, diffusion, sql-injection]
category: [research]
---
# Deep Dive: Diffusion Models - Từ Hỗn loạn đến Trật tự

## 1. Bản chất cốt lõi (Core Intuition)
Hãy tưởng tượng bạn có một câu lệnh SQL hoàn chỉnh. Bạn bắt đầu đổ mực lên nó (thêm nhiễu) cho đến khi nó chỉ còn là một vũng mực đen ngòm, không ai đọc được gì nữa. 

**Diffusion Model** làm ngược lại: Nó học cách "lau sạch" vũng mực đó theo từng bước nhỏ để khôi phục lại câu SQL ban đầu.
- Khi đã học được cách lau sạch mực, bạn chỉ cần đưa cho nó một vũng mực ngẫu nhiên (nhiễu), nó sẽ tự động "lau" ra một câu SQL hoàn toàn mới.

**Nỗi đau giải quyết:** GAN rất khó train (dễ sụp đổ/mode collapse). Diffusion ổn định hơn nhiều vì nó không phải "đấu đá" với ai cả, nó chỉ tập trung vào việc học cách khử nhiễu.

## 2. Cách thức vận hành (How it works)
Gồm 2 quá trình:
1.  **Forward Process (Làm bẩn):** Thêm nhiễu Gaussian vào dữ liệu theo từng bước cho đến khi dữ liệu biến mất hoàn toàn.
2.  **Reverse Process (Làm sạch):** Đây là nơi mô hình AI (thường là kiến trúc U-Net hoặc Transformer) thực hiện công việc. Nó nhìn vào dữ liệu đang bị bẩn và đoán xem "nhiễu" đã được thêm vào là gì để trừ đi.

Khi muốn sinh dữ liệu mới: Bạn bắt đầu với 100% nhiễu trắng, cho mô hình chạy qua hàng chục bước khử nhiễu, cuối cùng một câu SQL "xịn" sẽ hiện ra.

## 3. Giải mã công thức (Math Decoded)

| Công thức | Ý nghĩa "tiếng người" | Tại sao quan trọng? |
| --- | --- | --- |
| **Gaussian Noise ($\epsilon$)** | "Bụi bẩn ngẫu nhiên". | Là nguyên liệu đầu vào để mô hình học cách dọn dẹp. |
| **Denoising Step** | "Một lần lau gương". | Mỗi bước mô hình chỉ cần đoán một chút nhiễu, giúp việc học trở nên cực kỳ ổn định. |
| **Score Function** | "La bàn chỉ hướng". | Chỉ cho mô hình biết hướng nào là hướng để trở về vùng dữ liệu "đẹp" (SQL có ý nghĩa). |
| **U-Net / Transformer** | "Bộ não thực hiện". | Kiến trúc chịu trách nhiệm nhìn nhiễu và đoán dữ liệu gốc. |

## 4. Liên hệ bài toán SQL Injection
**Tại sao Diffusion có tiềm năng cho SQLi?**
- **Sự đa dạng (Diversity):** Diffusion cực giỏi trong việc tạo ra các mẫu dữ liệu khác biệt nhau hoàn toàn, không bị lặp lại như GAN.
- **Tính ổn định:** Bạn sẽ không gặp cảnh Generator "chết lâm sàng" như khi dùng GAN cho Text.
- **Khả năng chỉnh sửa:** Bạn có thể đưa một câu SQL bình thường vào, thêm một chút nhiễu, rồi bảo Diffusion "lau sạch nhưng hãy làm nó trông giống SQL Injection". Đây gọi là **Guided Diffusion**.

**Nhược điểm:**
- Chạy rất chậm. Để sinh ra một câu SQL, nó phải chạy qua 50-100 bước tính toán (trong khi GAN chỉ cần 1 bước).
- Áp dụng cho text vẫn đang là một thách thức lớn (cần chuyển text sang không gian liên tục trước).

## 5. Kết nối & Mở rộng (Connections)
- **Mô hình liên quan:** Stable Diffusion (ảnh), Diffusion-LM (text), Discrete Diffusion.
- **Câu hỏi mở:** Có thể dùng Diffusion để "biến đổi" một câu SQL sạch thành một câu SQL Injection mà vẫn giữ nguyên được chức năng của nó không?

## 6. Tài liệu tham khảo
- Paper: "Denoising Diffusion Probabilistic Models" (2020).
- Blog: What are Diffusion Models? (Lilian Weng).
