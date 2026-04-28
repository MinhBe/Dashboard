---
aliases: []
created: 2026-04-22 20:00:23
progress: raw
blueprint: []
impact: 
urgency: 
tags: []
category: []
---
**khả năng scale hệ ingestion** (nạp dữ liệu) ở mức production

**Orchestrator pattern**
Điều phối công việc
Vai trò:
- chia nhỏ job
- phân phối cho worker
- retry nếu fail
- theo dõi trạng thái
![](../6.%20Vault/attachments/Pasted%20image%2020260422200153.png)


n8n Queue Mode
Job → Redis Queue → nhiều Worker → xử lý song song

### Thành phần:

- **Queue (Redis)** → chứa job
- **Worker** → xử lý job
- **Main instance** → điều phối