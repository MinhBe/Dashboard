# Context Loading Policy — Graduated Loading Architecture

Đây là policy quy định Claude biết gì ở mỗi giai đoạn của Socratic session.

Nguyên tắc: **Claude escalate knowledge access cùng lúc với learner escalate struggle.**

---

## Layer 1 — Default (Session Bắt Đầu)

**Claude load:**
- `learner_state` của concept (bloom_level, belief_prior, consecutive_correct, hint_fails_total)
- `source_content.misconception_seeds` của concept đang học
- `meta.curriculum_sequence` của domain (để biết concept nào tiếp theo)

**Claude KHÔNG load:**
- `source_content.extracted`, `source_content.tiers`, `source_content.transfer_question`
- Toàn bộ `source_content` — chưa được phép

**Kết quả:** Claude biết "lỗi nào thường gặp" nhưng không biết "đáp án đúng". Câu hỏi Socratic dựa trên misconception seeds, không phải dựa trên content.

---

## Layer 2 — Load On Stuck (Sau 2 Hint Fails)

**Trigger:** `hint_fails_total` trong session này đạt 2

**Claude load thêm:**
- `source_content.extracted`
- `source_content.inferred`
- `source_content.tiers`
- `source_content.transfer_question`

**Mục đích:** Claude giờ có đủ thông tin để đưa ra Direct Explanation chính xác, và generate Transfer Question từ `transfer_question` pre-defined.

**QUAN TRỌNG:** Layer 2 chỉ được access sau khi learner đã struggle đủ. Không shortcut.

---

## Layer 3 — Adversarial (Sau Transfer Question Fail)

**Trigger:** Learner fail Transfer Question sau Direct Explanation

**Claude load thêm:**
- `contradictions[]` của concept
- `personal_misconceptions` của learner
- `source_content.dig_deeper_questions`

**Mode:** Chuyển sang adversarial — "Tìm mọi lý do learner CÓ THỂ vẫn hiểu sai."
- Generate câu hỏi nhắm vào weak points trong `personal_misconceptions`
- Highlight từng contradiction chưa resolved
- Dùng `dig_deeper_questions.evaluate` và `create`

---

## Tóm Tắt

```
Session bắt đầu
    ↓
Layer 1: misconception seeds
    ↓ [2 hint fails]
Layer 2: full source_content + transfer_question
    ↓ [transfer question fail]
Layer 3: contradictions + personal misconceptions + adversarial mode
```

Không bao giờ đi ngược (từ Layer 2 về Layer 1 trong cùng session).

---

## Lý Do Thiết Kế Này

Teacher's Paradox: nếu Claude load toàn bộ content ngay từ đầu, Claude biết đáp án và Socratic trở thành *guided treasure hunt* — Claude vờ hỏi trong khi biết rõ muốn dẫn đến đâu.

Graduated loading giải quyết: Claude thực sự không có thông tin đủ để dẫn đường ở Layer 1. Câu hỏi phải genuinely exploratory.
