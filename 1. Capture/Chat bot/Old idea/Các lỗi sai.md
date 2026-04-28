---
aliases: []
created: 2026-04-22 20:10:10
progress: raw
blueprint: []
impact: 
urgency: 
tags: []
category: []
---
Recursive Character Text Splitter KHÔNG split theo markdown mặc định

Supabase node không insert JSONB đúng cách

Vector search fail silent

Chunks không có heading → context lost

Polling loop với sleep cứng -> dùng  exponential backoff (2s, 4s, 8s, ...) + max retries

Không có record manager → re-embed toàn bộ mỗi lần



----
Đề tài:
Phân phối thiết bị IT (Firewall, Switch, Server, Storage, UPS, Camera, Router...) **Bài toán thực tế:** - Mỗi khi có hồ sơ mời thầu (HSMT), nhân viên phải đọc thủ công 2–3 tiếng để hiểu yêu cầu - Việc so sánh thông số giữa các hãng mất 1–2 ngày 

Viết thuyết minh kỹ thuật, BOM, báo giá làm lại từ đầu cho mỗi dự án 

**Mục tiêu tổng quát:** Xây dựng hệ thống AI hỗ trợ toàn bộ quy trình đấu thầu — từ đọc HSMT → chọn thiết bị → viết hồ sơ kỹ thuật → lập BOM báo giá. --- 
## 2. Stack Kỹ thuật
| Thành phần | Vai trò | |---|---| | **n8n** | Orchestration — điều phối toàn bộ workflow | | **Qwen (LLM)** | Classify tài liệu, generate text, phân tích HSMT | | **Supabase (PostgreSQL + pgvector)** | Lưu vector embeddings + metadata | | **Telegram Bot** | Giao diện người dùng cuối | | **Python** | Xử lý file: scan, dedup, extract text, embed | | **Docker** | Chạy toàn bộ stack local (n8n + Supabase PostgreSQL) | | **ngrok** | Expose n8n ra ngoài để Telegram webhook hoạt động |
*

Dự kiến

Thiết kế 1 chuẩn dữ liệu markdown lưu vào vector DB cho RAG
Dùng phương pháp hybird retrieval để tìm kiếm dữ liệu gồm Dense Search, sparse, pattern matching,BM25,triagram  sau đó gộp lại và chấm điểm
Tôi cũng sẽ thêm metadata filtering có thể là time-base, vị trí đặc thù của tài liệu, nguồn, theo loại file, theo dạng ngôn ngữ
Về re-ranking lấy top K lấy top 20-50 kết quả chấm lại kĩ lấy top 5 rồi LLM đọc rồi mới trả lời
Khi xử lý dạng data thì sẽ có thêm thông tin như là khi PDF thì có thểm mô tả , dự kiến Ingestion
Retrieval + Reasoning

về Structured data integration, thì tôi sẽ dự kiến datasheet sẽ là BI

còn RAG sẽ là lấy ngữ cảnh
khi gặp câu hỏi thì sẽ ưu tiên Query SQL rồi mới là RAG search, combine lại mới trả lời dự kiến sử dụng - Text hóa
- SQL query
- Tool/APi calling
  
Tôi cũng muốn Graph RAG


tôi muốn thiết kế hệ thống Evaluation framework đây là phần tối quan trọng đối với tôi
 Dataset test (ground truth)  
bộ câu hỏi + đáp án chuẩn

Metrics (thước đo)

- **Accuracy** → đúng/sai
- **Faithfulness** → có bịa không
- **Context relevance** → lấy đúng tài liệu chưa

tôi cũng mong muốn có thể scale **Orchestrator pattern**  
Điều phối công việc  
Vai trò:

- chia nhỏ job
- phân phối cho worker
- retry nếu fail
- theo dõi trạng thái 

n8n Queue Mode  
Job → Redis Queue → nhiều Worker → xử lý song song

### Thành phần:

- **Queue (Redis)** → chứa job
- **Worker** → xử lý job
- **Main instance** → điều phối
- **Recall@K** → có tìm ra doc đúng không

Evaluation method

- Rule-based
- LLM-as-judge
- Human evaluation