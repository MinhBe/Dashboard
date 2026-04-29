---
aliases: []
created: 2026-04-29 07:28:18
progress: raw
blueprint: []
impact: 
urgency: 
tags: []
category: []
---
# Đề tài

**NGHIÊN CỨU MÔ HÌNH GAN** **CHO SINH DỮ LIỆU TẤN CÔNG SQLI NHẰM NÂNG CAO** **MÔ HÌNH PHÁT HIỆN DỰA TRÊN HỌC MÁY**


# Mục lục
**I.**    **DỰ KIẾN CÁC CHƯƠNG MỤC**

**MỤC LỤC**

**DANH MỤC CÁC TỪ VIẾT TẮT**

**DANH MỤC CÁC BẢNG BIỂU**

**DANH MỤC CÁC HÌNH VẼ**

**MỞ ĐẦU**

**CHƯƠNG 1. TỔNG QUAN VỀ SQL INJECTION VÀ PHÁT HIỆN DỰA TRÊN HỌC MÁY**

Chương 1 hệ thống hóa kiến thức nền tảng về SQL Injection và các hướng tiếp cận phát hiện bằng học máy; phân tích hạn chế của các phương pháp hiện có để xác định khoảng trống nghiên cứu mà luận văn giải quyết.

**1.1. Tổng quan về SQL Injection**

·      Phân loại: In-band (Error-based, Union-based), Blind (Boolean-based, Time-based), Out-of-band

·      Đặc trưng cú pháp payload và kỹ thuật obfuscation/bypass WAF (URL-encoding, comment injection, case variation, string concatenation)

·      Tác động của obfuscation đến mô hình phát hiện dựa trên đặc trưng ký tự/từ vựng

**1.2. Các phương pháp phát hiện SQL Injection hiện tại và hạn chế**

·      Phát hiện dựa trên chữ ký/luật (WAF, regex): hiệu quả cao với payload đã biết, dễ bypass bằng obfuscation

·      Phát hiện bất thường và học máy (TF-IDF, Random Forest, Extra Trees): hiệu suất phụ thuộc chất lượng dữ liệu huấn luyện

·      **Hạn chế cốt lõi:** mất cân bằng dữ liệu (Imbalance Ratio cao), dữ liệu tấn công khó thu thập, mô hình dễ overfit trên tập nhỏ

**1.3. Các phương pháp xử lý mất cân bằng và sinh dữ liệu**



**1.4. Nhận xét hạn chế của các nghiên cứu trước**

Tổng hợp các nghiên cứu liên quan, phân tích và chỉ ra những hạn chế còn tồn tại. Từ đó, luận văn đề xuất mô hình sinh dữ liệu cải thiện những hạn chế đó

**CHƯƠNG 2. DỮ LIỆU, TIỀN XỬ LÝ VÀ THIẾT KẾ PIPELINE**



**2.1. Nguồn dữ liệu và mô tả trường dữ liệu**



**2.2. Tiền xử lý dữ liệu**



**2.3. Các kiến trúc và mô hình đề xuất**



**CHƯƠNG 3. THỰC NGHIỆM VÀ ĐÁNH GIÁ**



**3.1. Môi trường thiết kế và thử nghiệm**



**3.2. Chỉ số đánh giá và cách diễn giải**



**3.3. Kết quả thực nghiệm**



**3.4. Phân tích và thảo luận**



**KẾT LUẬN**



**TÀI LIỆU THAM KHẢO**

[1]. . . . . . . . . . . . . . . . . .

[2]. . . . . . . . . . . . . . . . . .