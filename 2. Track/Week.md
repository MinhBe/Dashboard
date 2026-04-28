---
aliases:
tags: weekly
created: <% tp.file.creation_date("YYYY-MM-DD HH:mm:ss") %>
feeling:
summary:
week: <% tp.date.now("WW") %>
---

# 📅 Tuần <% tp.date.now("WW") %> — <% tp.date.now("DD/MM/YYYY") %>

---

# 🔴 Overdue — Việc Chưa Xong Tuần Này

```dataview
TASK
FROM "2. Track"
WHERE !completed
AND string(file.name) < string(dateformat(date(today), "yyyy-MM-dd"))
AND contains(file.name, "-")
```

---

# 🎯 Mục Tiêu Tuần Tới

## Công việc
- [ ] 

## Cá nhân
- [ ] 

## Đọc sách / Học
- [ ] 

---

# 💬 Nhìn Lại Tuần Này

**Làm tốt:**

**Chưa làm được:**

**Bài học:**

---

# 📊 Tổng Kết
```dataview
TABLE feeling, summary
FROM "2. Track"
WHERE string(file.name) >= string(dateformat(date(today) - dur(7 days), "yyyy-MM-dd"))
AND string(file.name) <= string(dateformat(date(today), "yyyy-MM-dd"))
AND contains(file.name, "-")
SORT file.name ASC
```
# 📅 Tuần <% tp.date.now("WW") %> — <% tp.date.now("DD/MM/YYYY") %>

---

# 🔴 Overdue — Việc Chưa Xong Tuần Này

```dataview
TASK
FROM "2. Track"
WHERE !completed
AND string(file.name) < string(dateformat(date(today), "yyyy-MM-dd"))
AND contains(file.name, "-")
```

---

# 🎯 Mục Tiêu Tuần Tới

## Công việc
- [ ] 

## Cá nhân
- [ ] 

## Đọc sách / Học
- [ ] 

---

# 💬 Nhìn Lại Tuần Này

**Làm tốt:**

**Chưa làm được:**

**Bài học:**

---

# 📊 Tổng Kết
```dataview
TABLE feeling, summary
FROM "2. Track"
WHERE string(file.name) >= string(dateformat(date(today) - dur(7 days), "yyyy-MM-dd"))
AND string(file.name) <= string(dateformat(date(today), "yyyy-MM-dd"))
AND contains(file.name, "-")
SORT file.name ASC
```# Missions ✨


# Thoughts 💬


# Notes 📝

```dataview
TABLE impact as Impact, created as Created
FROM -"6. Vault"
WHERE dateformat(file.ctime,"yyyy-MM-dd") = dateformat(date(this.created, "yyyy-MM-dd HH:mm:ss"), "yyyy-MM-dd")
SORT rank DESC, created DESC
```