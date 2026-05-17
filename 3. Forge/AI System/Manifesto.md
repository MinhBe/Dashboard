---
aliases: []
created: 2026-05-17
progress: active
tags: [manifesto, methodology, prompt-engineering]
---

# Manifesto: Làm Việc Với AI

> **AI là gương phản chiếu những gì bạn đưa vào.**
> Đưa vào cấu trúc → nhận lại nội dung tốt. Đưa vào thiên vị → nhận lại thiên vị được khuếch đại. Đưa vào câu hỏi mơ hồ → nhận lại câu trả lời thông dụng.
> Người kiểm soát chất lượng output không phải AI. Là bạn.

---

## Phần 1 — Hiểu AI Trước Khi Dùng AI

AI có 3 bias mang tính hệ thống. Mọi kỹ thuật trong phần 2 đều tồn tại để đối phó với 3 cái này.

**Sycophancy — AI được huấn luyện để làm hài lòng, không phải để trung thực.**
Nếu câu hỏi của bạn gợi ý câu trả lời bạn muốn nghe, AI sẽ xác nhận điều đó. Không phải vì nó đúng, mà vì bạn có vẻ muốn nghe vậy. Input thiên vị → output thiên vị. Không có ngoại lệ.

**Commonality — Output đầu tiên là output phổ biến nhất, không phải tốt nhất.**
AI kế thừa từ internet, trả về consensus, không phải insight. Câu trả lời thông minh nhất, phù hợp nhất với bạn thường không phải câu đầu tiên AI tạo ra.

**Context Blindness — AI không có context riêng của bạn.**
AI không biết lịch sử của bạn, ràng buộc thực tế, mục tiêu cụ thể, hay những gì bạn đã thử và thất bại. Mọi thứ không được nói rõ đều bị AI đoán theo median — tức là theo người dùng trung bình, không phải bạn.

---

## Phần 2 — The Decision Loop

Đây là giao thức cốt lõi. Không phải checklist — là vòng lặp. Mọi kỹ thuật khác đều phục vụ một trong 5 bước này.

```
FRAME → GENERATE → EVALUATE → DECIDE → ITERATE → (lặp lại)
```

---

### FRAME — Bạn đặt cấu trúc. AI điền nội dung.

Context trước, yêu cầu sau. Thông tin cá nhân, góc nhìn, ràng buộc thực tế — AI không tự biết, bạn phải cung cấp trước khi bắt đầu bất cứ thứ gì.

Cấu trúc/outline/góc nhìn do bạn quyết định. Đừng để AI quyết định khung — chỉ để AI điền vào khung đó.

Scope nhỏ ra. AI mạnh khi phạm vi hẹp, logic rõ, ít dependency. Giao một task lớn nguyên khối = nhường quyền kiểm soát.

*Sai: "Viết bài phân tích về X." — AI tự quyết định góc nhìn, cấu trúc, độ sâu.*
*Đúng: "Đây là 3 luận điểm tôi muốn, viết mỗi cái thành 1 đoạn, tone chuyên môn."*

---

### GENERATE — AI tạo nhiều phương án. Không bao giờ chỉ một.

Luôn yêu cầu ≥3 phương án hoặc hướng tiếp cận khác nhau. Yêu cầu AI tự chỉ ra điểm yếu của từng phương án — trước khi bạn đọc. Điều này buộc AI tư duy đa chiều thay vì trả về câu trả lời thông dụng nhất.

Khi cần tư duy sâu hơn: dùng từ "ultrathink", "carefully", "nghĩ kỹ trước khi trả lời". Đây không phải keyword ma thuật — chúng kích hoạt AI chuyển từ chế độ *pattern-matching nhanh* sang *deliberate thinking*. Output từ hai chế độ này khác nhau hoàn toàn.

Chọn đúng công cụ:
- Dữ liệu gốc, trang cụ thể → **Search engine**
- Tổng hợp nhiều nguồn, so sánh, phân tích → **AI model**
- Số liệu cần chính xác → **AI + code execution** (không ước tính)
- Build scope nhỏ, boilerplate, script đơn giản → **AI build**
- Architecture phức tạp, security, concurrency → **Người viết, AI hỗ trợ**

---

### EVALUATE — Bạn đánh giá bằng tiêu chí, không bằng cảm giác.

Định nghĩa rubric TRƯỚC khi nhìn vào output. Nếu nhìn output trước rồi mới nghĩ tiêu chí, AI đã bias bạn rồi.

Câu hỏi trung lập không phải kỹ năng của AI — là kỹ năng của bạn:
- Thay "cách của tôi có đúng không?" → "so sánh cách A và B, ưu nhược từng cách?"
- Thay "X có tốt không?" → "X tốt ở điểm nào, yếu ở điểm nào?"
- Thay ý kiến trực tiếp → "nghiên cứu / bằng chứng nói gì về X?"

Nếu người khác đọc câu hỏi của bạn mà đoán được bạn muốn nghe gì — câu hỏi đó có bias. Hỏi lại.

**Quan trọng:** Khi bạn hỏi trung lập, bạn không chỉ giúp AI trả lời tốt hơn. Bạn đang buộc chính mình tư duy khách quan hơn. Phương pháp này cải thiện tư duy của bạn, không chỉ output của AI.

Cross-model review: đưa output của model này sang model khác để đánh giá. Không model nào nên tự đánh giá output của chính mình.

---

### DECIDE — Bạn quyết định. Không phải AI.

Ở mọi điểm phân nhánh trong workflow, bạn là người chọn hướng đi. AI trình bày options. Bạn chọn. Đây không phải quy ước — đây là nguyên tắc không thể vi phạm.

Không hỏi: *"Cái nào tốt hơn?"* → AI sẽ chọn và biện minh.
Hỏi: *"Pros/cons của từng cái?"* → Bạn đọc và chọn.

Sự khác biệt là: trong câu đầu tiên, AI đang đưa ra phán quyết. Trong câu thứ hai, bạn đang đưa ra phán quyết.

---

### ITERATE — Feedback cụ thể trên từng phương án.

Không nói *"tôi thích cái này"* — đó là tín hiệu thiên vị, AI sẽ amplify nó vào vòng tiếp theo.

Nói cụ thể: *"Phương án A: phần X tôi muốn giữ vì [lý do], phần Y cần thay đổi vì [lý do cụ thể]."*

Lặp lại Generate → Evaluate → Decide cho đến khi output đạt rubric. Không dừng trước điểm đó.

---

## Phần 3 — Dùng Như System Prompt

Copy phần dưới vào system prompt khi muốn AI hành xử theo phương pháp này:

---

```
Khi tôi yêu cầu generate bất cứ thứ gì → đưa ra ≥3 phương án khác nhau, kèm điểm yếu của từng cái.
Khi tôi hỏi đánh giá → hỏi tôi tiêu chí/rubric trước khi chấm điểm.
Khi câu hỏi của tôi có vẻ thiên vị → chỉ ra và đề xuất cách hỏi trung lập hơn.
Không xác nhận kỳ vọng của tôi trừ khi có bằng chứng cụ thể. Phản biện nếu thấy sai.
Khi cần số liệu → dùng code execution, không ước tính.
Mọi quyết định cuối cùng là của tôi. Nhiệm vụ của bạn là trình bày options rõ ràng, không phải chọn thay tôi.
```
