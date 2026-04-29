---
aliases: [AI Agents, Agentic Workflow, AI Personas]
created: 2026-04-29 03:15:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [foundation, ai-agents, automation, workflow]
category: [theory]
---
# Foundation: Các Vai trò Agent trong Vòng đời AI

Để vận hành quy trình phát triển AI một cách tự động và hiệu quả, chúng ta có thể chia nhỏ trách nhiệm cho các "Skill Agents" chuyên biệt. Dưới đây là sơ đồ ánh xạ giữa các giai đoạn và các Agent tương ứng.

## 1. Giai đoạn: Xác định Bài toán & Dữ liệu
### **Agent: Data Strategy Scout**
- **Sứ mệnh:** Tìm kiếm nguồn dữ liệu chất lượng cao và xác định tính khả thi của bài toán.
- **Kỹ năng (Skills):**
    - Scraping & Crawling (Thu thập dữ liệu web).
    - Data Compliance (Kiểm tra bản quyền và đạo đức dữ liệu).
    - Domain Research (Tìm kiếm các paper hoặc dataset tương tự).
- **Công cụ:** Web search, API connectors, Database explorers.

## 2. Giai đoạn: Tiền xử lý & EDA
### **Agent: Data Engineering Specialist**
- **Sứ mệnh:** Biến dữ liệu thô thành "vàng" cho mô hình.
- **Kỹ năng (Skills):**
    - Data Cleaning (Xử lý nhiễu, trùng lặp).
    - Feature Engineering (Trích xuất đặc trưng chuyên sâu).
    - Statistical Analysis (Phân tích phân phối, tương quan).
- **Công cụ:** Pandas, NumPy, Scikit-learn, Visualization tools (Matplotlib/Seaborn).

## 3. Giai đoạn: Thiết kế Kiến trúc
### **Agent: AI Architect & Researcher**
- **Sứ mệnh:** Lựa chọn "bộ não" phù hợp nhất cho bài toán.
- **Kỹ năng (Skills):**
    - SOTA Analysis (Cập nhật các kiến trúc mới nhất).
    - Math Modeling (Thiết kế Loss function và Layer cấu trúc).
    - Framework Expertise (Thành thạo PyTorch, TensorFlow, Jax).
- **Công cụ:** Arxiv search, Model Zoo, Mathematical notation editors.

## 4. Giai đoạn: Huấn luyện & Tối ưu hóa
### **Agent: Training Orchestrator**
- **Sứ mệnh:** Quản lý tài nguyên và đảm bảo mô hình hội tụ.
- **Kỹ năng (Skills):**
    - Distributed Training (Huấn luyện song song trên nhiều GPU).
    - Hyperparameter Tuning (Bayesian Optimization, Grid Search).
    - Log Monitoring (Theo dõi Loss/Accuracy theo thời gian thực).
- **Công cụ:** Weights & Biases, TensorBoard, SLURM/Kubernetes.

## 5. Giai đoạn: Đánh giá & Kiểm thử
### **Agent: Validation & Red Teaming Expert**
- **Sứ mệnh:** Tìm ra điểm yếu của mô hình trước khi triển khai.
- **Kỹ năng (Skills):**
    - Adversarial Testing (Tấn công mô hình để kiểm tra độ bền).
    - Metric Analysis (Phân tích chuyên sâu FID, IS, BLEU, ROUGE).
    - Fairness & Bias Audit (Kiểm tra tính thiên kiến của mô hình).
- **Công cụ:** Custom test suites, Red-teaming frameworks.

## 6. Giai đoạn: Triển khai & Giám sát
### **Agent: MLOps Engineer**
- **Sứ mệnh:** Đưa mô hình vào thực tế và duy trì "sức khỏe" của nó.
- **Kỹ năng (Skills):**
    - Model Quantization & Optimization (Nén mô hình để chạy nhanh hơn).
    - CI/CD for ML (Tự động hóa luồng cập nhật mô hình).
    - Drift Detection (Phát hiện sự sụt giảm hiệu năng theo thời gian).
- **Công cụ:** Docker, NVIDIA Triton, Prometheus, Grafana.

---

## Bảng tổng kết Kỹ năng (Agentic Skill Map)

| Giai đoạn | Tên Agent | Kỹ năng trọng tâm |
| --- | --- | --- |
| **Data** | Scout | Thu thập & Chiến lược |
| **EDA** | Engineer | Làm sạch & Thống kê |
| **Modeling** | Architect | Thiết kế & Nghiên cứu |
| **Training** | Orchestrator | Tối ưu & Vận hành |
| **Eval** | Validator | Kiểm thử & Bảo mật |
| **Ops** | MLOps | Triển khai & Giám sát |
