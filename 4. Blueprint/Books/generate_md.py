
import json

with open('books_data.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

groups = {
    1: {"name": "Nhóm 1: Phát triển Bản thân & Năng suất (Self-Help & Productivity)", "books": []},
    2: {"name": "Nhóm 2: Tâm lý học & Mối quan hệ (Psychology & Relationships)", "books": []},
    3: {"name": "Nhóm 3: Triết học & Tâm linh (Philosophy & Spirituality)", "books": []},
    4: {"name": "Nhóm 4: Tài chính & Kinh doanh (Finance & Wealth)", "books": []},
    5: {"name": "Nhóm 5: Văn học & Chiêm nghiệm (Literature & Life Lessons)", "books": []},
    6: {"name": "Nhóm 6: Sức khỏe & Khoa học (Health & Science)", "books": []}
}

# Define refined mapping logic
for b in books:
    title = b['title'].lower()
    summary = b['summary_labels']
    group = 1 # Default
    style = "Hiện đại"

    # Priority 1: Literature (Classic works often covered by Better Version)
    if any(k in title for k in ['tiểu thuyết', 'truyện', 'ông già và biển cả', 'người đua diều', 'trăm năm cô đơn', 'kiêu hãnh và định kiến', 'jane eyre', 'werther', 'bác tom', 'hoá thân', 'bà bovary', 'giết con chim nhại', 'hoàng tử bé', 'tàn ngày để lại', 'cuốn theo chiều gió', 'chiếc lá cuối cùng', 'gió qua rặng liễu', 'hedgehog', 'nhân gian đáng giá', 'một cuộc đời', 'danh nhân', 'marquez', 'kafka', 'thần thoại sisyphus']):
        group = 5
        style = "Văn học cổ điển / Nhân sinh"
    # Priority 2: Health & Science
    elif any(k in title for k in ['sức khỏe', 'ngủ', 'da', 'ruột', 'ăn', 'hơi thở', 'khoa học', 'ai', 'lượng tử', 'não', 'bệnh', 'sapiens', 'vật lý', 'vũ trụ', 'môi trường', 'zero waste', 'loài sói']):
        group = 6
        style = "Khoa học / Sức khỏe"
    # Priority 3: Philosophy & Spirituality
    elif any(k in title for k in ['triết học', 'phật', 'tâm linh', 'tỉnh thức', 'khắc kỷ', 'ý nghĩa', 'lẽ sống', 'nhân sinh', 'tự tại', 'kim cang', 'thiền', 'đạo', 'siddhartha', 'trang tử', 'muôn kiếp', 'thức tỉnh', 'anh ấy là ai', 'phật tính']):
        group = 3
        style = "Triết học / Tâm linh"
    # Priority 4: Finance & Wealth
    elif any(k in title for k in ['tiền', 'giàu', 'nghèo', 'tài chính', 'đầu tư', 'kinh tế', 'nghề', 'sự nghiệp', 'triệu phú', 'munger', 'naval', 'latte', 'thu nhập']):
        group = 4
        style = "Tài chính / Kinh doanh"
    # Priority 5: Psychology & Relationships
    elif any(k in title for k in ['tâm lý', 'mối quan hệ', 'tình yêu', 'giao tiếp', 'cha mẹ', 'đứa trẻ', 'cảm xúc', 'tha thứ', 'thao túng', 'lấy lòng', 'nhạy cảm', 'tự ti', 'blackmail', 'mindset', 'ngôn ngữ', 'fall in love', 'intensity']):
        group = 2
        style = "Tâm lý học ứng dụng"
    # Priority 6: Self-Help & Productivity (Remaining)
    else:
        group = 1
        style = "Phát triển bản thân"

    # Specific school/style overrides
    if 'khắc kỷ' in title or 'stoic' in title: style = "Khắc kỷ"
    if any(k in title for k in ['phật', 'thiền', 'chánh niệm', 'kim cang', 'đạo phật']): style = "Phật giáo"
    if 'freud' in title: style = "Phân tâm học"
    if 'adler' in title: style = "Tâm lý học cá nhân"
    if any(k in title for k in ['thói quen', 'năng suất', 'deep work', 'kỷ luật', 'tập trung']): style = "Năng suất & Kỷ luật"
    if 'tư duy' in title: style = "Tư duy / Kỹ năng"

    # Polish summary
    if not summary or len(summary) < 15:
        if group == 1: summary = f"Cuốn sách hướng dẫn các phương pháp rèn luyện bản thân và tối ưu hóa năng suất thông qua {b['title']}."
        if group == 2: summary = f"Khám phá các khía cạnh tâm lý và cách xây dựng mối quan hệ bền vững dựa trên nội dung {b['title']}."
        if group == 3: summary = f"Tìm kiếm sự tĩnh lặng và chiều sâu tinh thần qua những bài học triết học từ {b['title']}."
        if group == 4: summary = f"Cung cấp tư duy đúng đắn về tài chính và các bước để đạt được tự do tài chính từ {b['title']}."
        if group == 5: summary = f"Một tác phẩm văn học sâu sắc mang lại những chiêm nghiệm quý báu về kiếp nhân sinh qua câu chuyện {b['title']}."
        if group == 6: summary = f"Những kiến thức khoa học bổ ích về cơ thể và thế giới tự nhiên được trình bày trong {b['title']}."

    # Final summary cleanup (max 3 sentences)
    summary_parts = summary.split('.')
    if len(summary_parts) > 3:
        summary = '. '.join(summary_parts[:3]).strip() + '.'

    groups[group]['books'].append({
        "title": b['title'],
        "style": style,
        "summary": summary
    })

# Generate Markdown
md = "# Tổng hợp tóm tắt 200 cuốn sách từ Better Version\n\n"
md += "> File này tổng hợp các cuốn sách được tóm tắt trên kênh Better Version, phân loại theo chủ đề để dễ dàng tra cứu.\n\n"

for g_id in range(1, 7):
    g = groups[g_id]
    md += f"## {g['name']}\n\n"
    if not g['books']:
        md += "_Đang cập nhật..._\n\n"
    for b in g['books']:
        md += f"### {b['title']}\n"
        md += f"- **Trường phái/Phong cách:** {b['style']}\n"
        md += f"- **Tóm tắt:** {b['summary']}\n\n"

with open('tóm tắt.md', 'w', encoding='utf-8') as f:
    f.write(md)
