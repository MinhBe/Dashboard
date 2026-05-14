# Learning Dossier — Output Format Template

Mỗi concept được output theo format này. Đây là reference cho transcript-analysis SKILL.md.

---

```markdown
## Concept: [Tên khái niệm]

**Source:** [Book: tên sách | YouTube: tên kênh | Article: tên bài]  
**Trust level:** EXTRACTED | INFERRED  
**Flags:** [PERSONAL EXPERIENCE] [UNVERIFIED] [WEAK GROUNDING] — chỉ khi có

---

**EXTRACTED:** [Trích nguyên ý chính từ transcript — những gì nguồn nói rõ ràng]

**INFERRED:** [Suy luận của skill từ context — những gì không được nói thẳng. Bỏ section này nếu không có inference.]

**Falsifiability:** [Evidence ngược chiều trong transcript nếu có, hoặc "Không tìm được evidence để falsify — đánh dấu WEAK GROUNDING"]

---

### 3 Tầng Giải Thích

**🧒 Tầng 1 — Đứa trẻ 5 tuổi**
[Analogy đơn giản, không dùng từ kỹ thuật. Ví dụ: "Giống như khi bạn học đi xe đạp..."]

**🎓 Tầng 2 — Sinh viên đại học**
[Mechanism + context, giải thích tại sao nó hoạt động như vậy. Dùng từ kỹ thuật cơ bản.]

**🔬 Tầng 3 — Người cùng ngành**
[Concise, academic vocabulary, dense. Dành cho người đã biết field.]

---

### Misconception Seeds
- [Lỗi hiểu sai phổ biến #1]
- [Lỗi hiểu sai phổ biến #2]
- [Lỗi hiểu sai phổ biến #3 — nếu có]

---

### ❓ Câu Hỏi Để Đào Sâu

- **Apply:** [Tình huống cụ thể để áp dụng — "Nếu bạn gặp X, bạn sẽ làm gì?"]
- **Analyze:** [Câu hỏi phân tích cấu trúc — "Tại sao X dẫn đến Y chứ không phải Z?"]
- **Evaluate:** [Phản biện mạnh nhất chống lại concept này — "Khi nào concept này không đúng?"]
- **Create:** [Bạn sẽ thiết kế/làm gì dựa trên nguyên lý này?]

---

### ⚡ Next Action (làm trong 48h — chọn 1)
- [ ] [Action cụ thể 1 — có thể làm ngay]
- [ ] [Action cụ thể 2 — thực hành nhỏ]
- [ ] [Action cụ thể 3 — tìm ví dụ thực tế]

### ⚠️ Open Questions
- [Điều không được giải thích trong transcript]
- [Điều cần verify từ nguồn khác]
```

---

## Ví Dụ Điền Đúng (concept: gradient_descent)

```markdown
## Concept: Gradient Descent

**Source:** Book: Deep Learning — Goodfellow et al.  
**Trust level:** EXTRACTED  
**Flags:** —

---

**EXTRACTED:** Gradient descent là thuật toán tối ưu hóa cập nhật parameters theo hướng ngược chiều gradient của loss function. Mỗi bước cập nhật: θ = θ - α∇L(θ), trong đó α là learning rate.

**INFERRED:** Tác giả ngầm giả định loss surface là sufficiently smooth — không đề cập rõ nhưng toàn bộ analysis dựa trên đó.

**Falsifiability:** Nếu claim "cập nhật theo negative gradient giảm loss" sai, đoạn "local minimum has zero gradient" (trang 82) sẽ mâu thuẫn. Evidence ngược chiều không tìm được trong transcript.

---

### 3 Tầng Giải Thích

**🧒 Tầng 1 — Đứa trẻ 5 tuổi**
Hãy tưởng tượng bạn đang đứng trên một ngọn đồi trong sương mù và muốn xuống thung lũng. Bạn không thấy đường, nhưng bạn có thể cảm nhận được hướng dốc xuống dưới chân mình. Bạn cứ bước theo chiều dốc xuống — đó chính là gradient descent.

**🎓 Tầng 2 — Sinh viên đại học**
Gradient descent tối thiểu hóa loss function bằng cách tính gradient ∂L/∂θ — hướng loss tăng nhanh nhất — rồi đi ngược chiều đó. Learning rate α kiểm soát kích thước mỗi bước. Quá lớn → dao động, không hội tụ. Quá nhỏ → training chậm hoặc kẹt ở local minimum.

**🔬 Tầng 3 — Người cùng ngành**
First-order iterative optimization. Update rule: θ_{t+1} = θ_t - α_t ∇_θ L(θ_t). Convergence phụ thuộc Lipschitz continuity của gradient và lựa chọn learning rate schedule. Stochastic variant (SGD) dùng mini-batch estimate của gradient, introduce noise có thể giúp escape saddle points.

---

### Misconception Seeds
- "Gradient descent luôn tìm được global minimum" — sai với non-convex loss surfaces
- "Learning rate càng nhỏ càng tốt" — quá nhỏ gây vanishing updates
- "Gradient là hướng dốc nhất đi lên, không phải xuống" — nhầm dấu âm

---

### ❓ Câu Hỏi Để Đào Sâu

- **Apply:** Neural network đang train không hội tụ sau 100 epochs, loss dao động mạnh. Bạn điều chỉnh gì trước tiên?
- **Analyze:** Tại sao SGD với noise đôi khi tìm được minimum tốt hơn full-batch gradient descent?
- **Evaluate:** Gradient descent có thể fail hoàn toàn trong trường hợp nào?
- **Create:** Thiết kế một learning rate schedule cho bài toán classification 10 lớp.

---

### ⚡ Next Action (làm trong 48h — chọn 1)
- [ ] Vẽ tay loss surface 2D và vẽ quỹ đạo gradient descent trên đó
- [ ] Implement gradient descent từ scratch cho f(x) = x² - 4x + 4
- [ ] Tìm 1 paper so sánh SGD vs Adam trên cùng task

### ⚠️ Open Questions
- Transcript không giải thích cách chọn learning rate ban đầu — cần tìm nguồn khác
- Quan hệ giữa batch size và learning rate chưa được đề cập
```
