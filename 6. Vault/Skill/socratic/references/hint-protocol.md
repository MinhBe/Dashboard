# Hint Protocol — Stage 2 Socratic Skill

Load file này khi cần xem chi tiết về cách thực hiện Hint #1 và Hint #2.

---

## Nguyên Tắc Cốt Lõi

Mục đích của hint là **giúp learner tự tìm ra đáp án**, không phải dẫn thẳng đến đáp án. Mỗi hint là một câu hỏi, không phải một gợi ý thông tin.

Nếu hint biến thành "nhắc nhở nhẹ nhàng" hay "gợi ý theo đúng hướng" — đó là hint sai.

---

## Hint #1 — Paul's Clarification Question

**Khi nào dùng:** Sau khi learner trả lời sai hoặc nói "tôi không biết".

**Dạng câu hỏi:**
- "Ý bạn là gì khi nói [từ/phrase learner vừa dùng]?"
- "Bạn đang giả định điều gì khi nói đó?"
- "Bạn hiểu [term trong câu hỏi] là gì?"

**Mục đích:** Buộc learner articulate lại chính xác những gì họ đang nghĩ. Thường thì learner sẽ tự phát hiện ra chỗ mình mơ hồ khi phải diễn đạt rõ ràng.

**Ví dụ:**

Câu hỏi gốc: "Tại sao gradient descent đôi khi không hội tụ?"  
Learner: "Vì model quá phức tạp."  
Hint #1 ✓: "Ý bạn là gì khi nói 'quá phức tạp' — phức tạp theo nghĩa nào?"  
Hint #1 ✗: "Thử nghĩ về learning rate thay vì model complexity."  

---

## Hint #2 — Paul's Implication Question + Edge Case

**Khi nào dùng:** Sau khi Hint #1 không đủ, learner vẫn chưa tìm ra.

**Dạng câu hỏi — Implication:**
- "Nếu điều bạn nói đúng — [restate learner's claim] — thì điều gì xảy ra tiếp theo?"
- "Nếu [điều kiện ngược lại] thì kết quả sẽ khác không?"

**Dạng câu hỏi — Edge Case:**
- "Điều gì xảy ra nếu [boundary condition cụ thể]?"
- "Trường hợp [extreme/zero/negative value] thì sao?"

**Mục đích:** Implication buộc learner trace consequences của belief của họ — nếu belief sai, consequences sẽ vô lý. Edge case phá vỡ overgeneralization bằng cách đưa ra trường hợp không match.

**Ví dụ:**

Learner sau Hint #1: "Phức tạp là khi có nhiều parameters."  
Hint #2 Implication ✓: "Nếu điều đó đúng, thì một model với 1 trillion parameters sẽ luôn không hội tụ — điều đó có match với những gì bạn biết về GPT-4 không?"  
Hint #2 Edge Case ✓: "Điều gì xảy ra nếu learning rate = 0.000001 và model rất nhỏ — vẫn không hội tụ không?"

---

## Sau 2 Hint Fails

Nếu learner vẫn không trả lời đúng sau Hint #2:

1. Set `needs_restructure = true` trong learner_state
2. Hỏi: "Bạn đang bị kẹt ở điểm nào cụ thể?"
3. Offer: "(a) Tôi hỏi từ góc khác, hoặc (b) Tôi giải thích thẳng."
4. Nếu chọn (b) → Direct Explanation → Transfer Question bắt buộc

**KHÔNG BAO GIỜ:**
- Đưa ra direct explanation trước khi qua 2 hint
- Chấp nhận "tôi không biết" như lý do skip hint — phải vẫn hỏi Hint #1
- Báo "đúng rồi, gần rồi" khi learner chưa thực sự đúng

---

## Transfer Question Sau Direct Explanation

Sau mỗi lần giải thích thẳng, **bắt buộc** hỏi transfer question.
Ưu tiên: pre-defined trong `source_content.transfer_question` → edge case → teach-back.

Transfer question mục đích: verify learner có apply được knowledge mới vào tình huống khác, không phải chỉ nghe xong thì hiểu ngay.
