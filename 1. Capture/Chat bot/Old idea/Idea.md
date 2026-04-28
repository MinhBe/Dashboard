---
aliases: []
created: 2026-04-22 13:48:25
progress: raw
blueprint: []
impact: 
urgency: 
tags: []
category: []
---
# Mục đích
AI-Automation hỗ trợ decision-making trong đấu thầu kỹ thuật

# Bài toán
- **Hiểu HSMT** (requirement extraction)
- **Match thiết bị** (catalog + datasheet)
- **Sinh tài liệu** (thuyết minh kỹ thuật)
- **Tính toán & báo giá** (structured data)

# Kiến trúc
## Telegram Bot UI

## n8n (Orchestrator)

## Processing Layer
- Qwen (LLM reasoning)
- Python workers

## Retrieval Layer
 - BM25 / full-text 
 -  Vector DB (pgvector)
 - Trigram search 
 - Metadata filtering 
 - Re-ranking (top 50 → top 5)

## Structured Data Layer (BI)
- PostgreSQL (datasheet, pricing)
- SQL / API query

## Knowledge Graph
- Device
- Vendor
- Spec
- Compatibility

# Data Design
## Markdown schema cho RAG
Device
Metadata
- vendor
- category
- source
- date
Specs
Use Cases
Notes


## Structured DB (BI layer)
devices (
  id,
  name,
  vendor,
  category,
  throughput,
  price,
  updated_at
)

# Retrieval Strategy
## Hybrid Retrieval
Dense (semantic)     → hiểu nghĩa
BM25                → keyword chính xác
Trigram             → typo / fuzzy
Merge → RRF → Top 50
→ Re-rank → Top 5

# Query Routing (cực quan trọng)
User query  
↓  
Classifier (LLM)  
↓  
IF numeric / pricing:  
→ SQL  
ELSE:  
→ RAG  
ELSE IF complex relation:  
→ Graph  
↓  
Combine → Answer

# Graph RAG
- compatibility:
    - firewall A có dùng với switch B không
- dependency:
    - system cần gì

[Device] ──compatible_with──> [Device]
[Device] ──belongs_to──> [Vendor]
[Device] ──has_spec──> [Spec]

# Orchestrator
n8n (main)
   ↓
Redis Queue
   ↓
Workers (Python)
   - parse PDF
   - OCR
   - embedding
   - dedup

# Scale
- tăng worker = tăng throughput
- retry job nếu fail
- log trạng thái

# Evaluation Framework
## Dataset
### Retrieval test

{  
  "query": "router cho chi nhánh 50 user",  
  "relevant_docs": ["doc_123", "doc_456"]  
}

---

### 🔵 QA test

{  
  "question": "thiết bị nào phù hợp cho 50 user",  
  "answer": "Cisco ISR 4431"  
}

---

### 🟣 SQL test

{  
  "question": "giá router Cisco ISR 4431",  
  "sql": "SELECT price FROM devices WHERE name='ISR 4431'"  
}


## Metrics
### Retrieval

- Recall@K
- Precision@K

---

### Generation

- Accuracy
- Faithfulness
- Context relevance

---

### SQL

- Execution accuracy
- Result correctness


## Evaluation pipeline
Test dataset
   ↓
Run system
   ↓
Collect:
   - retrieved docs
   - final answer
   ↓
Evaluate:
   - rule-based
   - LLM-as-judge
   ↓
Score report

## LLM-as-judge prompt
Câu hỏi: ...
Câu trả lời: ...
Ground truth: ...

Đánh giá:
1. Có đúng không?
2. Có bịa không?
3. Có thiếu không?

