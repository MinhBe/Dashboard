---
aliases: [Architecture Decision, Model Selection Process]
created: 2026-04-29 04:00:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [foundation, architecture, model-selection, deep-learning]
category: [theory]
---
# Foundation: Quy trình Lựa chọn Kiến trúc Mô hình AI

Lựa chọn kiến trúc không phải là một sự lựa chọn ngẫu nhiên mà là một quá trình đánh giá dựa trên sự đánh đổi (trade-offs) giữa hiệu năng, tài nguyên và bản chất của dữ liệu.

## 1. Quy trình Lựa chọn (Decision Framework)

### Bước 1: Xác định Kiểu quan hệ trong Dữ liệu (Data Inductive Bias)
Mỗi kiến trúc được thiết kế để "ưu tiên" một loại quan hệ nhất định:
- **Quan hệ Không gian (Spatial):** Nếu dữ liệu có tính chất cục bộ (các điểm gần nhau có liên quan chặt chẽ) -> Ưu tiên **CNN**.
- **Quan hệ Tuần tự (Sequential):** Nếu thứ tự trước sau là quyết định -> Ưu tiên **RNN/LSTM** hoặc **Transformers**.
- **Quan hệ Toàn cục (Global):** Nếu mọi phần tử đều có thể ảnh hưởng đến nhau bất kể khoảng cách -> Ưu tiên **Transformers**.
- **Quan hệ Đồ thị (Graph):** Nếu dữ liệu là các thực thể và mối liên kết -> Ưu tiên **GNN**.

### Bước 2: Đánh giá Không gian Biểu diễn (Representation Space)
- **Rời rạc (Discrete):** Dữ liệu là các token, ký tự, hoặc nhãn -> Cần kiến trúc xử lý xác suất rời rạc hoặc kỹ thuật Embedding.
- **Liên tục (Continuous):** Dữ liệu là ảnh, âm thanh, tín hiệu số -> Cần kiến trúc xử lý không gian thực.

### Bước 3: Phân tích Ràng buộc Tài nguyên (Constraint Analysis)
- **Tốc độ Huấn luyện:** Transformer cho phép song song hóa (nhanh), RNN phải chạy tuần tự (chậm).
- **Bộ nhớ (Memory):** Transformer có độ phức tạp $O(N^2)$ với độ dài chuỗi $N$. Dữ liệu quá dài cần các biến thể như Longformer hoặc Reformer.
- **Latency (Độ trễ khi thực thi):** Diffusion rất chậm do cần nhiều bước khử nhiễu, GAN/VAE sinh dữ liệu gần như tức thời.

### Bước 4: Khả năng Chuyển đổi (Transferability)
- Kiểm tra xem đã có các mô hình huấn luyện sẵn (Pre-trained models) cho kiến trúc đó hay chưa. Việc bắt đầu từ một "bộ não" đã có kiến thức cơ bản luôn tốt hơn học từ đầu.

## 2. Ma trận Lựa chọn theo Mục tiêu Tạo sinh

| Mục tiêu | Kiến trúc Đề xuất | Lý do |
| --- | --- | --- |
| **Độ đa dạng cao** | Diffusion Models | Tránh được sụp đổ chế độ (Mode Collapse), phủ sóng toàn bộ phân phối dữ liệu. |
| **Độ sắc nét/Sát thực** | GANs | Cơ chế đối đầu ép Generator phải tạo ra các chi tiết cực kỳ giống thật. |
| **Cấu trúc Logic chặt chẽ** | Transformers | Cơ chế Attention hiểu được các ràng buộc ngữ pháp và logic tầm xa. |
| **Tạo biến thể từ mẫu có sẵn** | VAEs | Không gian tiềm ẩn (Latent Space) liên tục cho phép nội suy giữa các mẫu dữ liệu. |

---

## 3. Các bước Thực nghiệm (Prototyping)

1.  **Baseline Selection:** Chọn một kiến trúc đơn giản nhất (ví dụ: MLP hoặc RNN đơn giản) để làm thước đo cơ sở.
2.  **Ablation Study:** Thử nghiệm việc thêm/bớt các thành phần (Layer, Attention heads) để hiểu tác động của chúng lên kết quả.
3.  **Cross-Validation:** Đánh giá độ ổn định của kiến trúc trên các tập dữ liệu con khác nhau.
