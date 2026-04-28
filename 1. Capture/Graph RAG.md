---
aliases: []
created: 2026-04-22 19:47:06
progress: raw
blueprint: []
impact: 
urgency: 
tags: []
category: []
---
RAG bình thường:
Query → tìm document giống → trả về
Dựa trên 
- semantic similarity (embedding)
- keyword (BM25)
- không hiểu mối quan hệ giữa các thông tin 

Graph RAG
dùng “knowledge graph” để tìm và suy luận theo mối quan hệ

Ví dụ
[Nguyễn Văn A] ──làm việc tại──> [Công ty X]
[Nguyễn Văn A] ──quản lý──> [Dự án Y]
[Dự án Y] ──sử dụng──> [Công nghệ Z]

không còn là text rời rạc  
mà là **mạng lưới quan hệ**
có thể **traverse (đi theo graph)**
hiểu quan hệ nhiều bước