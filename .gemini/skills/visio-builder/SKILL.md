---
name: visio-builder
description: Chuyên gia xây dựng sơ đồ mạng và hạ tầng vật lý bằng Microsoft Visio (.vsdx). Sử dụng khi cần tạo sơ đồ từ mô tả văn bản, tự động hóa việc sắp xếp các hình khối (shapes) để tránh chồng chéo, và duy trì tính nhất quán bằng cách sử dụng các mẫu (templates) có sẵn.
---

# Visio Builder Skill

Skill này giúp bạn tạo ra các sơ đồ Visio chuyên nghiệp (đặc biệt là sơ đồ mạng và vật lý) bằng cách sử dụng thư viện Python `vsdx`. Thay vì phải kéo thả thủ công, bạn có thể mô tả cấu trúc mạng và để AI agent thực hiện việc vẽ và sắp xếp.

## Workflow chính

### 1. Phân tích mô hình (Topology Analysis)
Khi bạn cung cấp một mô tả mạng (ví dụ: danh sách thiết bị và kết nối), Skill này sẽ:
- Xác định các loại thiết bị (Router, Switch, Firewall, Server).
- Tham chiếu đến các "Master Shape" trong file template của bạn.
- Tính toán tọa độ để tránh các thiết bị đè lên nhau.

### 2. Chuẩn bị dữ liệu (Data Preparation)
Dữ liệu đầu vào nên có định dạng JSON như sau:
```json
{
  "template": "C:/path/to/your/template.vsdx",
  "output": "C:/path/to/output.vsdx",
  "device_map": {
    "switch": "ID_CỦA_HÌNH_MẪU_SWITCH",
    "router": "ID_CỦA_HÌNH_MẪU_ROUTER"
  },
  "devices": [
    {"name": "SW-CORE-01", "type": "switch"},
    {"name": "FW-01", "type": "firewall"}
  ],
  "connections": [
    {"from": "SW-CORE-01", "to": "FW-01"}
  ]
}
```

### 3. Thực thi (Execution)
Agent sẽ chạy script `visio_gen.py` để tạo ra file `.vsdx` cuối cùng.

## Cách lấy ID của hình mẫu (Master Shapes)
Để script hoạt động chính xác, bạn cần biết ID của các hình mẫu trong file template. Bạn có thể yêu cầu Agent chạy lệnh sau để liệt kê các hình có sẵn trong một file:
`python scripts/visio_gen.py --analyze C:/path/to/template.vsdx`

## Nguyên tắc sắp xếp (Layout)
- **Grid Layout**: Mặc định sắp xếp theo hàng và cột.
- **Tự động tránh chồng chéo**: Script sẽ tính toán khoảng cách (spacing) dựa trên kích thước trang và số lượng thiết bị.

## Lưu ý bảo mật
Skill này chỉ thao tác trên các file được chỉ định. Luôn sao lưu các file quan trọng trước khi thực hiện ghi đè.
