---
aliases: []
created: 2026-04-22 19:41:16
progress: raw
blueprint: []
impact: 
urgency: 
tags: []
category: []
---
đưa dữ liệu có cấu trúc (database, bảng, số liệu) vào hệ AI / RAG để dùng chung với text


Có thể dùng hệ chuẩn như hệ BI Business Intelligence


Nhưng
RAG **không dành cho số liệu chính xác**
DB / BI **không dành cho hiểu ngữ cảnh**

=> Nếu câu hỏi = số liệu → query DB  
Nếu câu hỏi = giải thích → dùng RAG  


RAG chỉ đọc lại nội dung đã viết
**không tính toán lại**, không query nguồn gốc
Có nhiều version text 
đọc được cái gì thì dùng cái đó

Có 2 dạng

| Dạng         | VD              |
| ------------ | --------------- |
| Structured   | SQL, Excel bảng |
| Unstructured | PDF, doc, text  |

![](../6.%20Vault/attachments/Pasted%20image%2020260422194243.png)

Các phương án
- Text hóa
- SQL query
- Tool/APi calling