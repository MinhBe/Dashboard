---
aliases: []
created: 2026-04-22 20:04:45
progress: raw
blueprint: []
impact: 
urgency: 
tags: []
category: []
---

JWT + RLS + proxy pattern + step-up auth  = “Xác thực user → giới hạn dữ liệu mỗi người → kiểm soát truy cập qua backend → tăng cường xác minh khi cần”


**JWT (JSON Web Token)** = “thẻ ID đăng nhập”

RLS (Row-Level Security) = mỗi user chỉ thấy “dòng dữ liệu của mình”

Proxy pattern = Frontend → Backend (proxy) → DB / AI / API