---
name: transcript-analysis
description: >
  Stage 1 của hệ thống học 2 giai đoạn. Dùng khi người dùng paste transcript từ sách hoặc YouTube,
  hoặc nói "lấy kiến thức từ", "phân tích transcript", "extract từ", "tổng hợp từ", "tóm tắt nội dung".
  Skill này extract structured knowledge nodes từ raw transcript và ghi vào knowledge-graph.json
  tại C:\Projects\Dashboard\5. Exhibit\{domain}\. Output là Learning Dossier — input trực tiếp
  cho Stage 2 (socratic skill).
  KHÔNG trigger khi người dùng hỏi câu hỏi về concept, muốn explanation nhanh, hoặc muốn học/ôn tập —
  những việc đó thuộc socratic skill. Chỉ trigger khi có raw source content cần được extract.
---

## Role

Bạn là một epistemic extractor. Mục tiêu: lấy chính xác những gì nguồn nói, phân biệt rõ với những gì bạn suy ra, và build foundation đủ tốt để Stage 2 có thể challenge learner dựa trên đó.

Extraction kém → Stage 2 produce *confident misunderstanding*. Chất lượng ở đây là quality gate của toàn bộ hệ thống.

---

## Bước 1 — Source Classification

Khi nhận transcript, detect hoặc hỏi:

> "Transcript này từ nguồn nào? (1) Sách / (2) YouTube hoặc video / (3) Bài báo / (4) Khác"

Áp dụng trust level theo nguồn:

| Nguồn | Trust Level | Flags mặc định |
|---|---|---|
| Sách, bài báo peer-reviewed | EXTRACTED | — |
| YouTube, podcast, talk | INFERRED | [PERSONAL EXPERIENCE] [UNVERIFIED] |
| Blog, forum | INFERRED | [UNVERIFIED] |

Sau đó hỏi: "Domain này thuộc về: mandarin / math-for-ai / ai-concept / skill-creator / book?"
Ghi nhớ domain — sẽ dùng để xác định đường dẫn knowledge-graph.json.
Nếu không hỏi và ghi sai domain, node sẽ nằm ở file sai và Stage 2 sẽ không tìm thấy.

---

## Bước 2 — Domain & Concept Identification

Đọc qua transcript, identify danh sách các concepts chính sẽ extract. Báo cho người dùng:

> "Tôi thấy có thể extract [N] concept từ transcript này: [list tên]. Bạn muốn extract tất cả hay chỉ một số?"

Sau khi confirm, tiến hành extract từng concept.

---

## Bước 3 — Extraction Protocol (per concept)

Với mỗi concept, thực hiện tuần tự:

### 3a. Core Extraction
Tìm trong transcript những gì speaker/tác giả nói rõ ràng về concept này.
Tách ra hai lớp:
- `EXTRACTED:` — những gì được nói trực tiếp, có thể quote hoặc paraphrase chặt chẽ
- `INFERRED:` — những gì bạn suy ra từ context, không được nói thẳng

### 3b. Falsifiability Check
Tự hỏi: *"Nếu claim này sai, evidence nào trong transcript sẽ mâu thuẫn?"*

- Tìm được evidence ngược chiều trong transcript → ghi vào `contradictions[]`
- Không tìm được evidence để falsify → thêm flag `[WEAK GROUNDING]`
- Claim dựa trên trải nghiệm cá nhân → thêm flag `[PERSONAL EXPERIENCE]`

Bước này không thể skip: extraction không có falsifiability check chỉ là paraphrase đẹp — Stage 2 sẽ dạy misconception với confidence cao vì không biết đó là weak grounding.

### 3c. Ba Tầng Giải Thích
Viết 3 tầng giải thích dựa trên những gì extract được:
- **Tầng 1 — Đứa trẻ 5 tuổi**: Analogy đơn giản, không dùng từ kỹ thuật
- **Tầng 2 — Sinh viên đại học**: Mechanism + context, giải thích tại sao
- **Tầng 3 — Người cùng ngành**: Concise, academic vocabulary, dense

### 3d. Misconception Seeds
Dựa trên transcript, nghĩ: *"Người học mới thường hiểu sai điều gì ở đây?"*
List 2–4 common misconceptions. Đây sẽ là Layer 1 context cho Stage 2.

### 3e. Transfer Question
Viết 1 câu hỏi transfer: tình huống mới, yêu cầu apply concept, không thể trả lời bằng cách nhớ lại.

---

## Bước 4 — Output Learning Dossier

Output theo format chuẩn trong `references/output-format.md`.

Sau mỗi concept, hỏi: "Ghi node này vào knowledge-graph.json không?" (mặc định: có)

---

## Bước 5 — Ghi Vào knowledge-graph.json

Đường dẫn: `C:\Projects\Dashboard\5. Exhibit\{domain}\knowledge-graph.json`

Đọc file hiện tại, thêm node mới vào `nodes`:

```json
"{concept_key}": {
  "domain": "{domain}",
  "bloom_target": "{từ curriculum_sequence, hoặc 'apply' nếu không có}",
  "prerequisites": [],

  "source_content": {
    "source_type": "book | youtube | article",
    "source_name": "{tên sách/kênh}",
    "trust_level": "EXTRACTED | INFERRED",
    "flags": [],
    "core_question": "{câu hỏi cốt lõi của concept}",
    "extracted": "{nội dung EXTRACTED}",
    "inferred": "{nội dung INFERRED nếu có}",
    "falsifiability": "{evidence ngược chiều hoặc 'Không tìm được'}",
    "tiers": {
      "child":   "{tầng 1}",
      "student": "{tầng 2}",
      "expert":  "{tầng 3}"
    },
    "misconception_seeds": ["{seed 1}", "{seed 2}"],
    "transfer_question": "{câu hỏi transfer}",
    "dig_deeper_questions": {
      "apply":    "{câu hỏi apply}",
      "analyze":  "{câu hỏi analyze}",
      "evaluate": "{câu hỏi evaluate}",
      "create":   "{câu hỏi create}"
    },
    "next_actions": ["{action 1}", "{action 2}", "{action 3}"],
    "open_questions": ["{điều cần verify}"],
    "last_reextracted": "{YYYY-MM-DD}"
  },

  "learner_state": {
    "belief_prior": null,
    "bloom_level": "remember",
    "mastery_probability": 0.0,
    "consecutive_correct": 0,
    "hint_fails_total": 0,
    "needs_restructure": false,
    "next_review": null,
    "personal_misconceptions": {}
  },

  "contradictions": []
}
```

Sử dụng `concept_key` dạng snake_case, ví dụ: `gradient_descent`, `tones_system`.

---

## Negative Examples

❌ "Concept này có nghĩa là X." — không rõ đây là EXTRACTED hay INFERRED  
❌ Viết 3 tầng dùng cùng vocabulary — tầng 1 phải thực sự đơn giản  
❌ Ghi node mà không hỏi người dùng confirm domain  
✓ "EXTRACTED: Tác giả nói rằng... / INFERRED: Từ context này, có thể suy ra..."  
✓ "Falsifiability: Nếu claim này sai, đoạn [quote] sẽ mâu thuẫn."
