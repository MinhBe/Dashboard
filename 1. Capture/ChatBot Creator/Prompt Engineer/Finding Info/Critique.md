---
aliases: []
created: 2026-05-08 14:38:30
progress: raw
blueprint: []
impact:
urgency:
tags: []
category: []
---
## Kĩ thuật
### Sửa tiểu tiết
Chỉnh từng cái
- Chỉnh từng **câu** hoặc từng **đoạn** một
- Brainstorm nhiều cách diễn đạt khác nhau

### Đánh giá
Nếu yêu cầu phê bình mà không có hướng dẫn rõ ràng -> có xu hướng khen ngợi
**Yêu cầu đánh giá tốt cần có:**
Tiêu chí cụ thể
Điểm số rõ ràng -> có điểm hoặc 0 điểm
Câu hỏi đúng sai -> không có vùng xám, nhận định chung chung
Thứ tự thực hiện


Vấn đề với prompt thiếu chi tiết
- Yêu cầu điểm tổng trước → AI đoán điểm rồi mới tìm lý do để biện minh
- Các tiêu chí mơ hồ, không có hướng dẫn cụ thể
- Kết quả: điểm thường cao hơn so với rubric khách quan

### Cross-Model Review
Đưa kết quả model này sang model khác để đánh giá
- Tích hợp kiến thức từ hai model khác nhau
- Tránh "blind spot" khi một model tự đánh giá chính mình
- Cho kết quả khách quan hơn một chút

### Thường xuyên thử nhiều AI model khác nhau

Các model liên tục được cập nhật và cải thiện
- Model tốt nhất cho một task hôm nay có thể không còn tốt nhất sau vài tháng
- -> Đưa cùng một prompt cho nhiều model 
- → so sánh kết quả 
- → dần dần xây dựng trực giác về "model nào tốt cho việc gì"