# FLOW Methodology - Hệ Thống Quản Lý Tri Thức Toàn Diện Cho Obsidian

> FLOW là phương pháp quản lý tri thức linh hoạt, kết hợp cấu trúc thư mục cứng và lớp linh hoạt (tags, wikilinks, properties).

---

## 🎯 Tổng Quan

- **Tác giả**: Thịnh Vũ ([Learn Anything](https://learn-anything.vn))
- **Nguồn gốc**: Kết tinh từ 3 năm trải nghiệm Zettelkasten, PARA, CODE, Ideaverse
- **Triết lý**: Tự do sáng tạo, gọn gàng, tương thích mọi nền tảng

### Ý Nghĩa FLOW
- **F**orge (Rèn Luyện) → Phát triển ý tưởng
- **L**ink (Liên Kết) → Kết nối dự án
- **O**rganize (Tổ Chức) → Sắp xếp thành phẩm
- **W**rite (Viết) → Duy trì dòng chảy

---

## 📂 Cấu Trúc 6 Thư Mục

```
├─1. Capture      (Thu Thập - Ý tưởng thô)
├─2. Track        (Theo Dõi - Nhật ký hàng ngày)
├─3. Forge        (Xưởng Rèn - Phát triển ý tưởng)
├─4. Blueprint    (Bản Thiết Kế - Quản lý dự án)
├─5. Exhibit      (Phòng Trưng Bày - Thành phẩm)
└─6. Vault        (Kho Lưu Trữ - Templates, Assets)
```

| Thư Mục | Chức Năng | Properties | Template |
|---------|------------|-------------|----------|
| **1. Capture** | Thu thập nhanh | `created`, `tags` | New Note |
| **2. Track** | Nhật ký, theo dõi | `created`, `tags`, `mood` | Daily |
| **3. Forge** | Rèn dũa ý tưởng | `progress`, `impact`, `urgency` | Thought, Deep Dive |
| **4. Blueprint** | TOC tự động, dự án | `aliases`, `tags`, `summary` | Blueprint, TOC |
| **5. Exhibit** | Trưng bày thành phẩm | `tags`, `publish` | Blog, Project |
| **6. Vault** | Templates, assets | `created`, `tags` | Profile, Read |

---

## 🔄 Vòng Đời Ghi Chú

```
raw → medium → done → published → archived
```

| Trạng Thái | Mô Tả |
|------------|--------|
| **raw** | Ý tưởng thô, chưa xử lý |
| **medium** | Đang phát triển, cần bổ sung |
| **done** | Đã hoàn thiện |
| **published** | Đã chia sẻ/công bố |
| **archived** | Lưu trữ dài hạn |

---

## 📋 Properties Chuẩn

| Trường | Kiểu | Giá Trị Mẫu |
|--------|------|--------------|
| `created` | Date & Time | `2024-09-16 21:09:00` |
| `progress` | Text | `raw`, `medium`, `done` |
| `impact` | Number (1-5) | `5` (cao nhất) |
| `urgency` | Number (0-1) | `1` (khẩn cấp) |
| `tags` | List | `#python`, `#tips` |
| `blueprint` | List | `[[Obsidian FLOW Methodology]]` |
| `publish` | Date & Time | `2024-09-20 06:15:00` |

---

## ✅ 8 Nguyên Tắc Vàng

| # | Nguyên Tắc | NÊN ✅ | KHÔNG ❌ |
|---|-----------|---------|----------|
| 1 | Đơn giản | Giữ 6 thư mục chính, nhất quán | Tạo nhiều thư mục con |
| 2 | Properties | Dùng `impact`, `urgency`, `tags` | Lạm dụng tags |
| 3 | Tuần tự | Capture → Forge → Blueprint → Exhibit | Để Capture tồn tại mãi |
| 4 | Nhất quán | Đánh số (1., 2., 3a...) | Đặt tên lung tung |
| 5 | Xem xét | Xem Forge hàng tuần | Để hệ thống cũ kỹ |
| 6 | Wikilinks | Liên kết ý tưởng giữa thư mục | Bỏ qua liên kết nội bộ |
| 7 | Linh hoạt | Ghi nhanh (raw) dù chưa hoàn hảo | Trì hoãn vì muốn hoàn hảo ngay |
| 8 | Cá nhân | Điều chỉnh theo nhu cầu | Ép mình theo khuôn mẫu cứng |

---

## 🔗 Wikilinks & Dataview

### Liên Kết Cơ Bản
```markdown
[[Tên ghi chú]]                    ← Liên kết cơ bản
[[Tên ghi chú\|Văn bản hiển thị]] ← Alias
[[Thư mục/]]                      ← Liên kết thư mục
```

### TOC Tự Động (Home.md)
```dataview
TABLE dateformat(date(file.ctime), "MMM dd") as Date
FROM "/"
WHERE number(impact) >= 4
SORT created DESC
LIMIT 20
```

---

## ⌨️ Phím Tắt Nhanh

| Chức Năng | Windows | macOS |
|-----------|---------|-------|
| Mở Settings | `Win + ,` | `⌘ + ,` |
| Toggle Left Sidebar | `Ctrl + Alt + L` | `⌘ + ⌥ + L` |
| Heading 1-6 | `Ctrl + Alt + 1-6` | `⌘ + ⌥ + 1-6` |
| New Note | `Ctrl + N` | `⌘ + N` |
| Insert Template | `Ctrl + Alt + ⇧ + T` | `⌘ + ⌥ + ⇧ + T` |
| Local Graph | `Ctrl + Alt + G` | `⌘ + ⌃ + G` |

> **Mẹo**: `Alt` = Giao diện, `Shift` = Chức năng nâng cao

---

## 🔌 Plugin Khuyên Dùng

**Core**: Templates, Daily Notes  
**Community**: Templater, Dataview, Calendar, Obsidian Projects, Icon Folder, Homepage, Floating TOC, Excalidraw

---

## 🌐 Tương Thích Đa Nền Tảng

FLOW hoạt động ngay cả khi **KHÔNG** có Obsidian (tags, wikilinks, properties).

- **Google Drive / OneDrive / Dropbox**: Duyệt thư mục chuẩn, mở bằng bất kỳ editor nào
- **GitHub + VS Code**: Version control, mở trực tiếp trên [vscode.dev](https://vscode.dev)
- **Ổ đĩa cục bộ**: Mở bằng Notepad, VS Code, không cần internet

---

## 🚀 Quy Trình Làm Việc (Workflow)

```
1. Capture: Ghi nhanh ý tưởng (Ctrl+N)
   ↓
2. Track: Cuối ngày viết nhật ký (Calendar)
   ↓
3. Forge: Chọn ý tưởng quan trọng → phát triển
   ↓
4. Blueprint: Tạo TOC quản lý dự án
   ↓
5. Exhibit: Chuyển thành phẩm, đặt publish date
   ↓
6. Vault: Lưu trữ templates, tài liệu
```

### Checklist Hàng Ngày
- [ ] Mở Home.md xem nhiệm vụ
- [ ] Ghi nhanh vào Capture khi có ý tưởng
- [ ] Cuối ngày viết Track (nhật ký)
- [ ] Xem lại Forge, cập nhật `progress`


---

> **Kết luận**: FLOW không chỉ là phương pháp quản lý tri thức, mà là lối sống số - nơi mọi ý tưởng đều có cơ hội phát triển từ hạt giống (Capture) đến cây trưởng thành (Exhibit). Hãy bắt đầu với sự đơn giản, và để dòng chảy (flow) dẫn lối cho sự sáng tạo của bạn.
