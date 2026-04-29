---
aliases: [Skill Engineering, Modular AI Capabilities, SKILL.md Architecture]
created: 2026-04-29 03:45:00
progress: raw
blueprint: []
impact: 
urgency: 
tags: [foundation, skill-engineering, claude-code, modularity]
category: [theory]
---
# Foundation: Kỹ nghệ Kỹ năng (Skill Engineering) cho AI Agent

## 1. Triết lý Mô-đun hóa (The Modular Philosophy)
Thay vì xây dựng một Agent khổng lồ biết tuốt mọi thứ (monolithic), chúng ta xây dựng một Agent cốt lõi (Core Agent) tinh gọn và mở rộng nó thông qua các **Skills**.

- **Skill:** Là một gói tài nguyên tự chứa (self-contained) bao gồm hướng dẫn, logic và công cụ để thực hiện một nhiệm vụ chuyên biệt.
- **Lợi ích:** Tiết kiệm ngữ cảnh (context window), dễ bảo trì, và cho phép Agent "học" kỹ năng mới chỉ bằng cách thêm một thư mục.

## 2. Cấu trúc Tiêu chuẩn của một Skill
Dựa trên kiến trúc của Anthropic và các Agent hiện đại, một Skill thường được tổ chức trong một thư mục với cấu trúc sau:

```text
skill-name/
├── SKILL.md          # Tệp quan trọng nhất: Chứa định nghĩa và hướng dẫn
├── requirements.txt  # (Tùy chọn) Các thư viện cần thiết cho skill
├── tools/            # (Tùy chọn) Chứa các script (Python, Bash) thực thi
└── examples/         # (Tùy chọn) Các ví dụ mẫu (few-shot)
```

### 2.1. Tệp SKILL.md
Đây là "bản đồ gene" của kỹ năng. Nó sử dụng YAML Frontmatter để Agent có thể hiểu và Markdown để hướng dẫn Agent hành động.

```markdown
---
name: "tên-kỹ-năng"
description: "Mô tả chi tiết khi nào Agent nên sử dụng kỹ năng này."
---
# Hướng dẫn (Instructions)
- Các chỉ thị cấp hệ thống.
- Các quy tắc ràng buộc.

# Ví dụ (Examples)
- Mẫu input/output để Agent bắt chước.
```

## 3. Cơ chế Vận hành (Execution Workflow)

1.  **Discovery (Khám phá):** Agent quét thư mục chứa các Skills hiện có.
2.  **Activation (Kích hoạt):** Dựa trên yêu cầu của người dùng, Agent so khớp ngữ nghĩa (semantic matching) với trường `description` trong `SKILL.md`.
3.  **Context Injection (Bơm ngữ cảnh):** Nội dung của `SKILL.md` được nạp vào cửa sổ ngữ cảnh của Agent.
4.  **Tool Execution (Thực thi công cụ):** Nếu nhiệm vụ yêu cầu hành động, Agent sẽ gọi các script trong thư mục `tools/` của skill đó.

## 4. Phân loại Skills

| Loại Skill | Thành phần chính | Mục đích |
| --- | --- | --- |
| **Instructional** | Chỉ có `SKILL.md`. | Định hướng phong cách, tuân thủ quy trình (Ví dụ: Quy tắc đặt tên file). |
| **Functional** | `SKILL.md` + Scripts. | Thực hiện hành động thực tế (Ví dụ: Trích xuất PDF, Tấn công thử nghiệm SQLi). |
| **Encoded Preference** | `SKILL.md` với nhiều ví dụ. | Giúp Agent hiểu gu thẩm mỹ hoặc tiêu chuẩn riêng của một cá nhân/tổ chức. |

## 5. Ứng dụng trong Project của bạn
Thay vì chỉ nói về GAN, bạn có thể xây dựng các Skill sau để "nạp" vào Agent của mình:

- **Skill: SQL-Syntax-Validator:** Giúp Agent kiểm tra cú pháp SQL trước khi xuất ra.
- **Skill: WAF-Bypass-Strategy:** Chứa các mẫu bypass (Case folding, Hex encoding) để Agent áp dụng khi sinh dữ liệu.
- **Skill: GAN-Training-Monitor:** Chứa các logic để Agent tự đọc log huấn luyện và đưa ra điều chỉnh.

## 6. Kết nối & Mở rộng
- **Skill Discovery Protocol:** Cách Agent tự tìm và cài đặt skill mới từ các repository (như ClawHub).
- **Skill Composition:** Khả năng kết hợp nhiều skill cùng lúc để giải quyết một nhiệm vụ phức tạp.
