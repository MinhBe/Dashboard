# Closing Protocol — Kết Thúc Socratic Session

Load file này ở cuối session để đảm bảo không bỏ qua bước nào.

---

## Khi Nào Kết Thúc Session

Session kết thúc khi một trong các điều sau xảy ra:
1. Learner pass Transfer Question → concept tiến lên Bloom level tiếp theo
2. Learner yêu cầu dừng
3. Concept được flag `needs_restructure` và đã qua Direct Explanation + Transfer Question
4. Đã học đủ số concepts theo kế hoạch của session

---

## Closing Checklist (làm trước khi kết thúc)

### 1. Update Scripts

Với mỗi concept đã học trong session, gọi `update_graph.py`:
```
python update_graph.py --domain {domain} --concept {concept} --result {correct|incorrect} --bloom {level}
```

Nếu có misconception được xác nhận trong session:
```
python update_graph.py --domain {domain} --concept {concept} --misconception {type} --example "{example}"
```

Nếu có belief_prior mới được elicit:
```
python update_graph.py --domain {domain} --concept {concept} --belief_prior "{prior}"
```

### 2. Session Summary

Đưa ra summary ngắn cho learner:

```
Session summary:
• Đã học: [list concepts]
• Bloom progression: [concept] remember → understand ✓
• Misconceptions phát hiện: [list nếu có]
• Cần restructure: [list nếu có]
• Next review: [dates]
```

### 3. Next Review Schedule

Báo ngày review tiếp theo cho mỗi concept dựa trên `learner_state.next_review` sau khi update.

### 4. Concept Tiếp Theo

Nếu learner muốn tiếp tục, suggest concept tiếp theo trong `curriculum_sequence` chưa mastered.

---

## Exit Criterion Tracking

Nhắc learner về 3 điều kiện để một concept được coi là **MASTERED (Tầng 1)**:
1. Transfer question 100% không hint
2. Edge case generation — tự nghĩ boundary condition nguồn không mention
3. "What would break this?" — tự xác định điều kiện khiến concept sai

Sau 7–14 ngày, concept cần pass thêm **INTERNALIZED (Tầng 2)** — một trong:
- Tự tạo analogy mới (không dùng analogy của Stage 1)
- Compression test: giải thích trong 5 câu → 2 câu → 1 câu

---

## Ongoing Tracking (không phải exit gate)

Trước mỗi bài tập/ví dụ: nhắc learner dự đoán kết quả trước khi làm.
Log prediction accuracy vào `learner_state` khi cần.
