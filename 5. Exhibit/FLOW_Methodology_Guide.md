# FLOW Methodology - Hướng Dẫn Toàn Diện Quản Lý Tri Thức Trong Obsidian

> **FLOW** là phương pháp quản lý tri thức linh hoạt và toàn diện cho Obsidian, kết hợp giữa cấu trúc cứng (thư mục) và lớp linh hoạt (tags, wikilinks, properties).

---

## 1. TỔNG QUAN FLOW

### Nguồn gốc
- Được phát triển bởi **Thịnh Vũ** (Learn Anything)
- Kết quả 3 năm trải nghiệm các hệ thống: Zettelkasten, PARA, CODE, Ideaverse (ACE)
- Tối ưu cho Obsidian nhưng áp dụng được cho mọi nền tảng lưu trữ

### Ý nghĩa tên gọi FLOW
- **F**orge (Rèn Luyện): Quá trình sáng tạo và hoàn thiện ý tưởng
- **L**ink (Liên Kết): Kết nối dự án, ý tưởng, nhiệm vụ
- **O**rganize (Tổ Chức): Sắp xếp và trưng bày thành phẩm
- **W**rite (Viết): Ghi chép và duy trì dòng chảy công việc

### Tại sao chọn FLOW?
| Vấn đề | Giải pháp FLOW |
|--------|----------------|
| Zettelkasten thiếu tính thực tiễn quản lý dự án | Tích hợp quản lý dự án thực tế |
| PARA quá hạn chế, khó liên kết | Linh hoạt, tận dụng tối đa Obsidian |
| Ideaverse quá cầu kỳ, nhiều lớp thư mục | Đơn giản, dễ tiếp cận |
| Quá tải nhận thức | Giới hạn 7±2 thư mục, giảm tải trí não |

---

## 2. CẤU TRÚC 6 THƯ MỤC CHÍNH

```
├─1. Capture      (Thu Thập)
├─2. Track        (Theo Dõi)
├─3. Forge        (Xưởng Rèn)
├─4. Blueprint    (Bản Thiết Kế)
├─5. Exhibit      (Phòng Trưng Bày)
└─6. Vault        (Kho Lưu Trữ)
```

### Chi tiết từng thư mục

#### 1. Capture (Thu Thập)
- **Chức năng**: Nơi ghi lại nhanh ý tưởng thô, suy nghĩ bất chợt, thông tin chưa xử lý
- **Cách dùng**: Ghi nhanh không cần lo cấu trúc, sử dụng template "New Note"
- **Properties**: `created`, `tags`, `category`
- **Ví dụ**: `1. Ý tưởng mới.md`, `2. Ghi chú nhanh.md`

#### 2. Track (Theo Dõi)
- **Chức năng**: Dòng chảy ghi chú hàng ngày, nhật ký, theo dõi tiến độ
- **Cách dùng**: Ghi chú ngày tháng, phản ánh cá nhân, theo dõi cảm xúc
- **Properties**: `created`, `tags`, `category`, `mood` (tùy chọn)
- **Ví dụ**: `2026-05-05.md`, `Week.md`

#### 3. Forge (Xưởng Rèn)
- **Chức năng**: Phát triển ý tưởng từ Capture thành bản nháp hoàn chỉnh
- **Cách dùng**: Rèn dũa ý tưởng, thử nghiệm, kết nối wikilinks
- **Properties**: `progress`, `impact`, `urgency`, `blueprint`
- **Ví dụ**: `1. Phát triển ý tưởng X.md`, `2. Bản nháp dự án Y.md`

#### 4. Blueprint (Bản Thiết Kế)
- **Chức năng**: Quản lý dự án tổng thể, bản đồ nội dung (TOC)
- **Cách dùng**: Tạo TOC tự động với Dataview, liên kết các ghi chú
- **Properties**: `aliases`, `tags`, `category`, `summary`
- **Ví dụ**: `Project X Map.md`, `Home.md`

#### 5. Exhibit (Phòng Trưng Bày)
- **Chức năng**: Trưng bày sản phẩm hoàn thiện, bài viết đã publish
- **Cách dùng**: Lưu trữ thành phẩm, dễ dàng truy cập tham khảo
- **Properties**: `tags`, `publish`, `category`
- **Ví dụ**: `Bài viết hoàn thiện.md`, `Dự án đã xong.md`

#### 6. Vault (Kho Lưu Trữ)
- **Chức năng**: Templates, attachments, scripts, tài liệu hệ thống
- **Cách dùng**: Lưu trữ tài nguyên không dùng thường xuyên
- **Properties**: `created`, `tags` (đơn giản)
- **Cấu trúc con**: `templates/`, `templater/`, `attachments/`, `bookshelf/`, `scripts/`

---

## 3. VÒNG ĐỜI GHI CHÚ (NOTE LIFECYCLE)

Hành trình của một ghi chú giống như trồng cây: từ hạt giống đến cây trưởng thành.

```
raw → medium → done → published → archived
```

| Trạng thái | Mô tả | Ví dụ |
|------------|--------|-------|
| **raw** | Ý tưởng thô sơ, chưa xử lý | Ghi chú mới tạo từ Capture |
| **medium** | Đang phát triển, cần bổ sung | Đang rèn dũa trong Forge |
| **done** | Đã hoàn thiện, sẵn sàng dùng | Dự án đã xong trong Blueprint |
| **published** | Đã chia sẻ/công bố | Bài viết đăng blog, Substack |
| **archived** | Lưu trữ dài hạn | Chuyển vào Vault khi không dùng thường xuyên |

### Quy trình luân chuyển
1. **Capture**: Ghi lại ý tưởng (status: `raw`)
2. **Forge**: Phát triển ý tưởng (status: `medium`)
3. **Blueprint**: Tổ chức dự án (status: `done`)
4. **Exhibit**: Trưng bày thành phẩm (status: `published`)
5. **Vault**: Lưu trữ (status: `archived`)

---

## 4. HỆ THỐNG PROPERTIES (METADATA)

### Bảng Properties chuẩn

| Trường | Mô tả | Kiểu dữ liệu | Giá trị mẫu |
|--------|--------|--------------|--------------|
| **aliases** | Tên thay thế của ghi chú | Text | "Gợi ý Python" |
| **created** | Thời gian tạo | Date & Time | `2024-09-16 21:09:00` |
| **progress** | Trạng thái ghi chú | Text | `raw`, `medium`, `done` |
| **publish** | Thời gian xuất bản | Date & Time | `2024-09-20 06:15:00` |
| **blueprint** | Ghi chú/dự án cha | List | `[[Obsidian FLOW Methodology]]` |
| **impact** | Mức độ quan trọng (1-5) | Number | 5 (cao nhất) |
| **urgency** | Mức độ cấp thiết (0-1) | Number | 1 (khẩn cấp) |
| **tags** | Thẻ phân loại | List | `#python`, `#tips` |
| **category** | Danh mục | List | "Tips", "Python" |
| **channel** | Kênh xuất bản | List | "LinkedIn", "Substack" |

### Cách dùng theo thư mục

| Thư mục | Properties chính | Ghi chú |
|---------|------------------|---------|
| Capture | `created`, `tags`, `category` | Ghi nhanh, tối giản |
| Track | `created`, `tags`, `mood` | Nhật ký hàng ngày |
| Forge | `progress`, `impact`, `urgency`, `blueprint` | Quản lý phát triển |
| Blueprint | `aliases`, `tags`, `summary` | TOC, quản lý dự án |
| Exhibit | `tags`, `publish`, `category` | Thành phẩm |
| Vault | `created`, `tags` | Tài nguyên hệ thống |

---

## 5. CHIẾN LƯỢC SỬ DỤNG TAGS

> **Nguyên tắc**: Chỉ dùng tag khi nó mang lại giá trị thực tế, tránh "tag bloat"

### 10 loại tag hiệu quả

| Phân loại | Ví dụ | Trường hợp sử dụng |
|-----------|-------|-------------------|
| **1. Đa Dự Án** | `#Project-X`, `#Project-Y` | Một ghi chú liên quan nhiều dự án |
| **2. Chủ Đề** | `#psychology`, `#AI`, `#wellness` | Lọc nhanh theo chủ đề |
| **3. Trạng Thái** | `#medium`, `#finalizing`, `#waiting-for-feedback` | Theo dõi luồng công việc |
| **4. Ưu Tiên** | `#urgent`, `#priority`, `#low-priority` | Đánh dấu mức độ quan trọng |
| **5. Tạm Thời** | `#to-review`, `#needs-update`, `#stale` | Đánh dấu cần xử lý (sau đó xóa) |
| **6. Nguồn** | `#book`, `#article`, `#interview` | Theo dõi nguồn gốc thông tin |
| **7. Liên Kết Chéo** | `#related-projects`, `#shared-research` | Kết nối đa ngữ cảnh |
| **8. Hành Động** | `#follow-up`, `#requires-decision` | Chờ phản hồi/quyết định |
| **9. Phiên Bản** | `#version-1.0`, `#needs-revision` | Quản lý cập nhật nội dung |
| **10. Hệ Thống** | `#template`, `#system`, `#configuration` | Phân biệt tài nguyên hệ thống |

### Vòng đời tag
1. **Tạo**: Tag phải có mục đích rõ ràng
2. **Sử dụng**: Dùng thường xuyên để lọc/tìm kiếm
3. **Đánh giá**: Xem xét định kỳ, xóa tag trùng lặp/không dùng

---

## 6. QUY TẮC ĐẶT TÊN NỘI DUNG

### Đặt tên thư mục
- **Nguyên tắc 7±2**: Tối đa 7-9 thư mục mỗi cấp (theo Cognitive Load Theory)
- **Nhất quán**: Dùng danh từ (Capture, Forge) hoặc động từ nhất quán
- **Ngắn gọn**: Dễ hiểu, dễ nhớ

### Đặt tên file
#### Cấu trúc chuẩn
```
THỨ_TỰ + ". " + NỘI_DUNG_CHÍNH + ĐUÔI_FILE
```

#### Thứ tự thuận
```
1. Obsidian Methodology Map.canvas
2. Phương pháp tổ chức thông tin.md
3. Yêu cầu bắt trong cấu trúc Vault.md
```

#### Thứ tự chèn ngang (Insert)
```
1. Obsidian Methodology Map.canvas
2. Phương pháp tổ chức thông tin.md
3. Yêu cầu bắt trong cấu trúc Vault.md
3a. Cấu trúc mở rộng.md
4. Thiết kế hệ thống ghi chú.md
```
> Sử dụng phân nhánh chữ cái (3a, 3b...) để chèn mà không đánh số lại toàn bộ

#### Sử dụng ký tự đặc biệt
- `⚡ Quick Capture.md` - Nổi bật ghi chú quan trọng
- `📅 Daily Log 15-09-2024.md` - Ghi chú ngày tháng

### Làm nổi bật với Iconize Plugin
| Thư mục | Icon gợi ý |
|----------|-------------|
| Capture | ✍️ |
| Track | 📅 |
| Forge | 🔨 |
| Blueprint | 📐 |
| Exhibit | 🖼️ |
| Vault | 🗄️ |

---

## 7. HỆ THỐNG TEMPLATE

### Templates (Insert Template - Ctrl+Alt+Shift+T)

| Template | Vị trí | Mục đích |
|----------|---------|-----------|
| **1. New Note** | `6. Vault/templates/1. New Note.md` | Ghi chú mới (mặc định Capture) |
| **2. Thought** | `6. Vault/templates/2. Thought.md` | Ghi chú suy nghĩ |
| **3. Blog** | `6. Vault/templates/3. Blog.md` | Bài viết blog |
| **4. Deep Dive** | `6. Vault/templates/4. Deep Dive.md` | Nghiên cứu sâu |
| **5. Daily** | `6. Vault/templates/5. Daily.md` | Nhật ký hàng ngày |
| **6. Read** | `6. Vault/templates/6. Read.md` | Ghi chú đọc sách |
| **7. Project** | `6. Vault/templates/7. Project.md` | Quản lý dự án |
| **8. Profile** | `6. Vault/templates/8. Profile.md` | Hồ sơ cá nhân |
| **9. TOC** | `6. Vault/templates/9. TOC.md` | Bản đồ nội dung |
| **10. Blueprint** | `6. Vault/templates/10. Blueprint.md` | Bản thiết kế |

### Templater Scripts (Tự động khi tạo mới)

| Script | Vị trí | Chức năng |
|--------|---------|-----------|
| **New.md** | `6. Vault/templater/New.md` | Ghi chú mới tự động (khi click chuột phải) |
| **Daily.md** | `6. Vault/templater/Daily.md` | Tạo ghi chú ngày (khi click vào Calendar) |
| **TOC.md** | `6. Vault/templater/TOC.md` | Tạo TOC tự động |

### Cài đặt Template
1. Bật Core Plugin **Templates**
2. Chỉ định thư mục: `6. Vault/templates`
3. Sử dụng: `Ctrl/Cmd + Alt + Shift + T` hoặc Command Palette > "Insert Template"
4. Templater: Cài plugin, trỏ đến `6. Vault/templater`

---

## 8. SỬ DỤNG DATAVIEW ĐỂ TẠO TOC

### TOC cho toàn bộ Vault (Home.md)
```dataview
TABLE dateformat(date(file.ctime), "MMM dd") as Date
FROM "/"
WHERE number(impact) >= 4 AND date(created) >= date(this.created-after)
SORT created DESC
LIMIT 20
```

### TOC cho dự án cụ thể (Blueprint)
```dataview
TABLE status, impact, created
FROM -"6. Vault"
WHERE contains(string(join(blueprint, "  ")), this.file.name) 
AND number(impact) >= number(this.min-impact)
SORT created DESC
```

### Lọc theo trạng thái
```dataview
TABLE status, urgency, updated
FROM "3. Forge"
WHERE status = "medium" OR status = "done"
SORT urgency DESC
```

### Lịch hiển thị (Calendar)
```dataview
CALENDAR file.ctime
LIMIT 5
```

---

## 9. WIKILINKS & LIÊN KẾT

### Tại sao dùng Wikilinks?
- Tạo mạng lưới tri thức liên kết
- Dễ dàng điều hướng giữa các ý tưởng
- Không phụ thuộc vị trí thư mục

### Cách sử dụng
```markdown
[[Tên ghi chú]]              # Liên kết cơ bản
[[Tên ghi chú|Văn bản hiển thị]]  # Liên kết có alias
[[Thư mục/]]                  # Liên kết thư mục
```

### Best Practices
- Liên kết từ Forge → Blueprint để kết nối ý tưởng với dự án
- Liên kết các chủ đề liên quan trong Exhibit
- Sử dụng `blueprint` property thay vì tag cho quan hệ cha-con

---

## 10. 8 NGUYÊN TẮC ÁP DỤNG FLOW

### Nguyên tắc 1: Giữ hệ thống đơn giản
✅ **NÊN**: Giữ cấu trúc rõ ràng, nhất quán với 6 thư mục chính
❌ **KHÔNG**: Tạo quá nhiều thư mục con phức tạp

### Nguyên tắc 2: Sử dụng properties/thẻ có mục đích
✅ **NÊN**: Dùng `impact`, `urgency`, `tags` để lọc và tìm kiếm
❌ **KHÔNG**: Lạm dụng tag không cần thiết

### Nguyên tắc 3: Quy trình tuần tự và linh hoạt
✅ **NÊN**: Capture → Forge → Blueprint → Exhibit
❌ **KHÔNG**: Để Capture tồn tại vĩnh viễn không xử lý

### Nguyên tắc 4: Nhất quán đặt tên
✅ **NÊN**: Đánh số (1., 2., 3a...) và sắp xếp đúng thư mục
❌ **KHÔNG**: Dùng nhiều cách đặt tên khác nhau

### Nguyên tắc 5: Thường xuyên xem xét
✅ **NÊN**: Xem lại Forge hàng tuần, chuyển `done` sang Exhibit
❌ **KHÔNG**: Để hệ thống cũ kỹ không cập nhật

### Nguyên tắc 6: Tận dụng Wikilinks
✅ **NÊN**: Liên kết ý tưởng giữa các thư mục
❌ **KHÔNG**: Bỏ qua việc tạo liên kết nội bộ

### Nguyên tắc 7: Tránh hoàn hảo hóa
✅ **NÊN**: Ghi nhanh ý tưởng dù chưa hoàn hảo (raw)
❌ **KHÔNG**: Trì hoãn vì muốn ghi chú hoàn hảo ngay lập tức

### Nguyên tắc 8: Cá nhân hóa
✅ **NÊN**: Điều chỉnh FLOW theo nhu cầu cá nhân
❌ **KHÔNG**: Ép bản thân theo khuôn mẫu cứng nhắc

---

## 11. HỆ THỐNG PHÍM TẮT (HOTKEYS)

### Cài đặt chung
- **macOS**: ⌘ = Command, ⌥ = Option, ⇧ = Shift, ⌃ = Control
- **Windows**: Ctrl = Control, Alt = Option, Shift = Shift

### Bảng phím tắt chuẩn FLOW

| Nhóm chức năng | Mô tả | macOS | Windows |
|----------------|--------|-------|----------|
| **Cài đặt** | Mở Settings | `⌘ + ,` | `Windows + ,` |
| **Sidebars** | Toggle Left Sidebar | `⌘ + ⌥ + L` | `Ctrl + Alt + L` |
| | Toggle Right Sidebar | `⌘ + ⌥ + R` | `Ctrl + Alt + R` |
| | Toggle App Ribbon | `⌘ + .` | `Ctrl + .` |
| **Headings** | Heading 1-6 | `⌘ + ⌥ + 1-6` | `Ctrl + Alt + 1-6` |
| **Note Actions** | New Note | `⌘ + N` | `Ctrl + N` |
| | Insert Tag | `⌘ + ⌥ + T` | `Ctrl + Alt + T` |
| | Insert Template | `⌘ + ⌥ + ⇧ + T` | `Ctrl + Alt + Shift + T` |
| | Insert Callout | `⌘ + ⇧ + .` | `Ctrl + Shift + .` |
| | Toggle Bullets | `⌘ + ⌃ + ⇧ + B` | `Ctrl + Ctrl + Shift + B` |
| | Toggle Highlight | `⌘ + ⌥ + H` | `Ctrl + Alt + H` |
| | Fold/Unfold All | `⌘ + ⌥ + E/C` | `Ctrl + Alt + E/C` |
| | Move Line Up/Down | `⌘ + U` / `⌘ + ⇧ + U` | `Ctrl + U` / `Ctrl + Shift + U` |
| **Graph & Links** | Local Graph | `⌘ + ⌃ + G` | `Ctrl + Alt + G` |
| | Outline | `⌘ + ⌥ + U` | `Ctrl + Alt + U` |
| | Links In Note | `⇧ + ⌥ + B` | `Shift + Alt + B` |
| | Links Out Note | `⇧ + ⌥ + O` | `Shift + Alt + O` |
| **File Mgmt** | Delete Note | `⌘ + ⌫` | `Ctrl + Delete` |
| | Move Note | `⌘ + ⌥ + ⇧ + M` | `Ctrl + Alt + Shift + M` |
| | Export to PDF | `⇧ + ⌥ + E` | `Shift + Alt + E` |
| **UI** | Zoom In/Out | `⌘ + =/-` | `Ctrl + =/-` |
| | Light Mode | `⇧ + ⌥ + L` | `Shift + Alt + L` |
| | Dark Mode | `⇧ + ⌥ + D` | `Shift + Alt + D` |
| **Pin & Bookmark** | Pin Note | `⌘ + ⌥ + P` | `Ctrl + Alt + P` |
| | Bookmark Search | `⌘ + ⌥ + B` | `Ctrl + Alt + B` |
| | Open Bookmark | `⌘ + ⇧ + B` | `Ctrl + Shift + B` |
| **Tables** | Insert Table | `⇧ + ⌥ + T` | `Shift + Alt + T` |
| **Plugins** | Create Mind Map | `⌘ + ⌥ + M` | `Ctrl + Alt + M` |
| | Toggle Mind Map | `⇧ + ⌥ + M` | `Shift + Alt + M` |
| | Callout Manager | `⌘ + ⌥ + ⇧ + C` | `Ctrl + Alt + Shift + C` |
| | New Excalidraw | `⌘ + ⌥ + ⇧ + V` | `Ctrl + Alt + Shift + V` |
| **Canvas** | New Canvas | `⇧ + ⌥ + C` | `Shift + Alt + C` |
| | Canvas Presentation | `⇧ + ⌥ + M` | `Shift + Alt + M` |

### Mẹo ghi nhớ
- `⌥/Alt` = Giao diện và điều hướng
- `⇧/Shift` = Chức năng nâng cao/mạnh hơn
- Số 1-6 = Heading levels
- L/R = Left/Right Sidebar
- P = Pin, B = Bookmark

---

## 12. THƯ VIỆN PLUGIN KHUYÊN DÙNG

### Core Plugins (Có sẵn)
| Plugin | Vai trò |
|--------|---------|
| **Templates** | Chèn mẫu ghi chú |
| **Daily Notes** | Tạo ghi chú hàng ngày |

### Community Plugins (Cài thêm)

| Plugin | Mục đích | Cách dùng |
|--------|-----------|-----------|
| **Templater** | Tạo template động với JavaScript | Tự động điền `created`, `progress` |
| **Dataview** | Truy vấn metadata tự động | Tạo TOC, lọc theo `impact`, `status` |
| **Calendar** | Lịch chọn ngày, tạo daily note | Click ngày → tạo/mở ghi chú ngày |
| **Obsidian Projects** | Quản lý dự án Kanban/Table | Quản lý Blueprint với `publish` date |
| **Obsidian Icon Folder** | Thêm icon cho thư mục/file | Làm nổi bật 6 thư mục chính |
| **Homepage** | Đặt trang chủ mặc định | Trỏ đến `Home.md` |
| **Dashboard Navigator** | Điều hướng vault nhanh | Ribbon navigation |
| **Callout Manager** | Quản lý callout blocks | Tạo ghi chú nổi bật |
| **Floating TOC** | TOC nổi bên phải | Điều hướng heading nhanh |
| **Obsidian Linter** | Tự động format markdown | Dọn dẹp ghi chú |
| **File Cleaner Redux** | Dọn file rác/tạm | Xóa file không dùng |
| **Obsidian Banners** | Thêm banner cho ghi chú | Trang trí Exhibit |
| **Obsidian Reminder** | Nhắc hạn công việc | Kết hợp với `urgency` |
| **Tasks Calendar Wrapper** | Lịch hiển thị tasks | Quản lý `TASK` trong Dataview |
| **Heatmap Calendar** | Heatmap hoạt động | Theo dõi thói quen |
| **Flashcards** | Tạo thẻ ghi nhớ | Học tập từ Vault |
| **Obsidian Excalidraw** | Vẽ sơ đồ tay | Mindmap, flowchart |
| **Obsidian Enhancing Mindmap** | Tạo mindmap tự động | Từ outline → mindmap |
| **Obsidian List Callouts** | List đẹp hóa | Danh sách styled |
| **NL Dates** | Ngày tự nhiên (hôm nay, tuần sau) | `{{date}}`, `{{time}}` |
| **Obsidian Style Settings** | Tùy chỉnh theme | Cá nhân hóa giao diện |
| **Editing Toolbar** | Thanh công cụ soạn thảo | Dễ dùng cho người mới |
| **Buttons** | Tạo nút bấm trong note | Tự động hóa tác vụ |

---

## 13. KIM TỰ THÁP DIKW & FLOW

```
        Wisdom (Thông Thái)
           ↑
      Knowledge (Tri Thức)
           ↑
      Information (Thông Tin)
           ↑
        Data (Dữ Liệu)
```

### Ánh xạ FLOW với DIKW

| Giai đoạn DIKW | Thư mục FLOW | Mô tả |
|---------------|--------------|--------|
| **Data** | Capture | Dữ liệu thô, ý tưởng vụn vặt chưa xử lý |
| **Information** | Track | Đặt bối cảnh, tạo dòng chảy thời gian và sự kiện |
| **Knowledge** | Forge | Kết nối, liên kết, rèn dũa thành tri thức có cấu trúc |
| **Wisdom** | Exhibit | Áp dụng tri thức, giải quyết vấn đề, chia sẻ ra ngoài |

> "Kim Tự Tháp DIKW và FLOW giống như hai bánh răng đồng bộ, biến dữ liệu thô thành sự thông thái thông qua dòng chảy không ngừng."

---

## 14. TƯƠNG THÍCH ĐA NỀN TẢNG

FLOW hoạt động hiệu quả ngay cả khi KHÔNG có Obsidian dynamics (tags, wikilinks, properties).

### Google Drive / OneDrive / Dropbox
- Duyệt thư mục giống nhau trên mọi nền tảng
- Mở file `.md` bằng Google Docs, Word, Notepad
- Cấu trúc cứng đảm bảo tìm thấy file dù không có Obsidian

### GitHub + VS Code (vscode.dev)
- Lưu trữ version control với Git
- Mở và sửa trực tiếp trên trình duyệt (không cần cài đặt)
- Xem markdown chuẩn GitHub Flavored
- Làm việc nhóm qua Pull Requests

### Ổ đĩa cục bộ
- Mở bằng Notepad, VS Code, TextEdit
- Cấu trúc thư mục rõ ràng giúp tìm kiếm nhanh
- Không phụ thuộc internet

> **Lợi thế độc đáo**: FLOW không phụ thuộc vào tính năng động của Obsidian, đảm bảo trải nghiệm liền mạch trên mọi thiết bị và nền tảng.

---

## 15. BIẾN THỂ TÊN THƯ MỤC (TÙY CHỈNH PHONG CÁCH)

| Chủ đề | Capture | Track | Forge | Blueprint | Exhibit | Vault |
|--------|---------|-------|-------|-----------|---------|-------|
| **Gardener** | Seed | Growth Cycle | Greenhouse | Root System | Knowledge Garden | Old Roots |
| **Explorer** | Compass | Trail | Expedition | Basecamp | Treasure Trove | Lost Archives |
| **Writer** | Scribble | Drafts | Workshop | Story Arc | Library | Archive |
| **Alchemist** | Spark | Transmutation | Crucible | Formula | Elixir | Vault of Secrets |
| **Navigator** | Map | Voyage | Dock | Navigation Plan | Captain's Log | Shipwreck |
| **Architect** | Blueprint | Foundation | Construction | Master Plan | Archive | Blueprints Vault |
| **Scholar** | Query | Study | Lab | Thesis | Codex | Manuscript Vault |
| **Strategist** | Intelligence | Operations | Command Post | Strategy Board | Archive | Classified |
| **Inventor** | Idea | Experiment | Workshop | Invention Plan | Patent Library | Prototype Vault |
| **Historian** | Chronicle | Timeline | Archives | Historical Map | Library of Records | Lost Relics |

> Ví dụ: Nếu bạn chọn **Writer**, cấu trúc sẽ là: `Scribble`, `Drafts`, `Workshop`, `Story Arc`, `Library`, `Archive`

---

## 16. QUY TRÌNH LÀM VIỆC NHANH (WORKFLOW)

### Quy trình chuẩn (Khuyên dùng)
```
1. Capture: Ghi nhanh ý tưởng (Ctrl+N, Template "New Note")
   ↓
2. Track: Cuối ngày, ghi lại nhật ký (Calendar plugin)
   ↓
3. Forge: Xem lại Capture, chọn ý tưởng quan trọng → phát triển
   ↓
4. Blueprint: Tạo TOC quản lý dự án (Dataview query)
   ↓
5. Exhibit: Khi xong → chuyển sang trưng bày, đặt publish date
   ↓
6. Vault: Lưu trữ template, scripts, tài liệu tham khảo
```

### Checklist hàng ngày
- [ ] Mở Obsidian, xem Home.md (nhiệm vụ hôm nay)
- [ ] Ghi chú nhanh vào Capture khi có ý tưởng
- [ ] Cuối ngày: viết Track (nhật ký, phản ánh)
- [ ] Xem lại Forge, cập nhật `progress` cho ghi chú

### Checklist hàng tuần
- [ ] Xem lại Capture, chuyển ý tưởng tốt sang Forge
- [ ] Cập nhật Blueprint TOC (kiểm tra `impact` >= 4)
- [ ] Chuyển ghi chú `done` từ Forge → Exhibit
- [ ] Xóa tag tạm thời (#to-review, #needs-update)
- [ ] Đánh giá lại tags, xóa tag không dùng

---

## 17. MỘT SỐ LƯU Ý QUAN TRỌNG

### Cần làm
✅ Giữ cấu trúc đơn giản, tối đa 7-9 thư mục gốc
✅ Sử dụng properties có mục đích (impact, urgency, progress)
✅ Thường xuyên xem xét và cập nhật trạng thái ghi chú
✅ Cá nhân hóa hệ thống theo nhu cầu
✅ Tận dụng Dataview để tự động hóa TOC

### Tránh làm
❌ Tạo quá nhiều thư mục con phức tạp
❌ Lạm dụng tags không cần thiết (tag bloat)
❌ Để Capture tồn tại vĩnh viễn không xử lý
❌ Ép bản thân theo khuôn mẫu cứng nhắc
❌ Trì hoãn vì muốn ghi chú hoàn hảo ngay

---

## 18. TÀI LIỆU THAM KHẢO & KÊNH HỖ TRỢ

### Kênh chính thức
- 📰 **Substack**: [learnanything.substack.com](https://learnanything.substack.com)
- 🏠 **Website**: [learn-anything.vn](https://learn-anything.vn)
- 😄 **Facebook**: facebook.com/mr.thinh.ueh

### Tải về
- **GitHub Repository**: [github.com/anomalyco/opencode](https://github.com/anomalyco/opencode)
- **Template Vault**: [learn-anything.vn/download-obsidian-flow](https://learn-anything.vn/download-obsidian-flow)

---

> **Kết luận**: FLOW không chỉ là phương pháp quản lý tri thức, mà là một lối sống số - nơi mọi ý tưởng đều có cơ hội phát triển từ hạt giống (Capture) đến cây trưởng thành (Exhibit). Hãy bắt đầu với sự đơn giản, và để dòng chảy (flow) dẫn lối cho sự sáng tạo của bạn.
