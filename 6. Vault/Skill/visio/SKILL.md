---
name: visio
description: Chuyên gia phân tích và xây dựng sơ đồ Visio (.vsdx). Bao gồm khả năng 'analyst' (đọc hiểu kiến trúc mạng, thiết bị, ISP, Firewall, L2/L3) và 'builder' (tạo sơ đồ tự động từ mô tả văn bản, tránh chồng chéo).
---

# Visio Skill (Analyst & Builder)

Skill này kết hợp hai khả năng mạnh mẽ để quản lý sơ đồ Microsoft Visio chuyên dụng cho hạ tầng mạng.

## 1. Khả năng Analyst (Phân tích)
Dùng để đọc hiểu toàn bộ nội dung của một file `.vsdx`. Skill sẽ phân tích các thiết bị, hãng sản xuất, chức năng và các tầng mạng (Layer 2, Layer 3).

### Cách sử dụng:
Yêu cầu Agent chạy script phân tích:
`python scripts/analyst.py <đường_dẫn_file.vsdx>`

### Các nội dung phân tích:
- **Inventory**: Phân loại Firewall (Forti, Sophos), Switch (Juniper, Cisco), Load Balancer (F5).
- **Network Layers**: Nhận diện ISP (CMC, VNPT), các vùng mạng (DMZ, Internal).
- **Chức năng**: Xác định vai trò của thiết bị (DNS, Database, Gateway).

## 2. Khả năng Builder (Xây dựng)
Dùng để tạo mới hoặc cập nhật sơ đồ dựa trên mô tả. Builder sử dụng cơ chế sắp xếp tự động để tránh các thiết bị đè lên nhau.

### Cách sử dụng:
1. Chuẩn bị file JSON topology (xem mẫu trong `references/topology_sample.json`).
2. Chạy script xây dựng:
`python scripts/builder.py <đường_dẫn_json>`

### Tính năng Builder:
- **Tự động sắp xếp**: Sử dụng Grid Layout với khoảng cách (spacing) tùy chỉnh.
- **Sử dụng Master Shapes**: Copy hình dáng từ file template để đảm bảo tính thẩm mỹ chuyên nghiệp.
- **Tránh chồng chéo**: Tự động tính toán tọa độ X, Y dựa trên số lượng thiết bị.

## Cấu trúc tài nguyên
- `scripts/analyst.py`: Script phân tích sâu XML/Shapes.
- `scripts/builder.py`: Script tạo sơ đồ tự động.
- `references/`: Chứa các tài liệu hướng dẫn chi tiết cho từng khả năng.

---
Sử dụng skill này khi bạn cần hiểu một hệ thống mạng phức tạp từ file Visio cũ hoặc khi muốn vẽ nhanh một mô hình mạng mới từ yêu cầu văn bản.
