# Hướng Dẫn Console Command - Hero's Adventure (大侠立志传)

## Cách mở Console
Nhấn **Ctrl+F11** sau khi chọn MOD và load game.

> **Lưu ý quan trọng**: Các lệnh dùng chữ Trung Quốc, copy chính xác từng dòng và paste vào console.

---

## 1. LỆNH CƠ BẢN

| Lệnh | Chức Năng |
|------|-----------|
| `money XXX` | Đặt tiền thành XXX |
| `onepunch 1` | Bật chế độ một đòn chết (hạ gục ngay lập tức) |
| `onepunch 0` | Tắt chế độ một đòn chết |
| `tp X Y Z` | Dich chuyển tới tọa độ (Y,Z) của map X |
| `item [ID, số_lượng]` | Nhận vật phẩm, VD: `item 32121,100` (dùng dấu phẩy) |
| `timepass XXX` | Tua nhanh XXX giây (96 giây = 1 ngày) |
| `relation XXX YYY` | Đặt quan hệ NPC ID XXX thành YYY |
| `fame XXX YYY` | Đặt danh tiếng thế lực XXX thành YYY |
| `attr XXX YYY ZZZ` | Đặt thuộc tính YYY của nhân vật XXX thành ZZZ |
| `exp XXX YYY` | Thêm YYY kinh nghiệm cho nhân vật XXX |
| `tribute XXX` | Đặt điểm cống hiến môn phái |
| `buff XXX YYY` | Thêm buff/trait YYY cho nhân vật XXX |
| `kungfu XXX YYY ZZZ` | Học võ công YYY cấp ZZZ cho nhân vật thứ X trong đội (MC=0) |
| `invisible` | Tàng hình (NPC không thấy bạn) |
| `speed X` | Tăng tốc game lên X lần |
| `pagoda XXX` | Đặt điểm Tháp Thiên thành XXX |
| `fiefmax` | Nâng cấp hết nhà cửa |

---

## 2. CHỈ SỐ CƠ BẢN (五维) - set tất cả = 25

```
attr 100401 臂力 25      (Strength - Sức mạnh)
attr 100401 敏捷 25      (Dexterity - Nhanh nhẹn)
attr 100401 悟性 25      (Intelligence - Trí tuệ)
attr 100401 福缘 25      (Luck - May mắn)
attr 100401 体质 25      (Constitution - Thể chất)
```

## 3. CHỈ SỐ ĐẠO ĐỨC (六项品德) - set tất cả = 25

```
attr 100401 仁德 25      (Benevolence - Nhân đức)
attr 100401 义气 25      (Loyalty - Nghĩa khí)
attr 100401 礼节 25      (Propriety - Lễ phép)
attr 100401 智慧 25      (Wisdom - Trí tuệ)
attr 100401 信用 25      (Trustworthiness - Tín dụng)
attr 100401 勇气 25      (Courage - Dũng khí)
```

## 4. CHỈ SỐ CHIẾN ĐẤU

```
attr 100401 拳掌 200     (Fist - Quyền chưởng)
attr 100401 御剑 200     (Sword - Ngự kiếm)
attr 100401 耍刀 200     (Blade - Đao pháp)
attr 100401 长兵 200     (Long Weapon - Trường binh)
attr 100401 短兵 200     (Short Weapon - Đoản binh)
attr 100401 乐器 200     (Musical - Nhạc khí)
attr 100401 医术 200     (Medical - Y thuật)
attr 100401 毒术 200     (Toxicology - Độc thuật)
attr 100401 暗器 200     (Throwing - Ám khí)
attr 100401 武学常识 200 (Knowledge - Võ học thường thức)
```

## 5. CHỈ SỐ KHÁC

```
attr 100401 攻击 9999         (Attack - Tấn công)
attr 100401 防御 9999         (Defense - Phòng thủ)
attr 100401 江湖历练 1000000  (Jianghu Experience - Kinh nghiệm giang hồ)
attr 100401 冲穴点数 999      (Acupuncture Points - Điểm xung huyệt)
```

## 6. KỸ NĂNG ĐỜI SỐNG (能力)

### 6a. Thu thập (采集)
```
attr 100401 能力_采集_采矿 12000   (Mining - Khai thác)
attr 100401 能力_采集_伐木 12000   (Woodcutting - Đốn gỗ)
attr 100401 能力_采集_采药 12000   (Gathering - Thu thập)
attr 100401 能力_采集_钓鱼 12000   (Fishing - Câu cá)
attr 100401 能力_采集_捉虫 12000   (Bug-catching - Bắt côn trùng)
```

### 6b. Chế tạo (制造)
```
attr 100401 能力_制造_兵器 12000   (Weapon Smithing - Rèn vũ khí)
attr 100401 能力_制造_护甲 12000   (Armor Smithing - Rèn giáp)
attr 100401 能力_制造_食物 12000   (Cooking - Nấu ăn)
attr 100401 能力_制造_丹药 12000   (Alchemy - Luyện đan)
attr 100401 能力_制造_饰品 12000   (Accessory Crafting - Làm trang sức)
attr 100401 能力_制造_合成 12000   (Tool Crafting - Chế tạo)
```

### 6c. Giám định (鉴定)
```
attr 100401 能力_鉴定_字画 12000   (Appraise Artwork - Giám định tranh chữ)
attr 100401 能力_鉴定_书籍 12000   (Appraise Book - Giám định sách)
attr 100401 能力_鉴定_古董 12000   (Appraise Antique - Giám định cổ vật)
attr 100401 能力_鉴定_饰品 12000   (Appraise Accessory - Giám định trang sức)
attr 100401 能力_鉴定_丹药 12000   (Appraise Medicine - Giám định thuốc)
```

### 6d. Thị tỉnh/Kỹ năng đen (市井)
```
attr 100401 能力_市井_暗取 12000   (Steal - Ăn trộm)
attr 100401 能力_市井_点穴 12000   (Immobilize - Điểm huyệt)
attr 100401 能力_市井_下毒 12000   (Poison - Đầu độc)
attr 100401 能力_市井_机关 12000   (Machinery - Cơ quan)
attr 100401 能力_市井_突袭 12000   (Ambush - Đột kích)
```

### 6e. Sinh tồn (生存)
```
attr 100401 能力_生存_口才 12000   (Persuade - Tài ăn nói)
attr 100401 能力_生存_经商 12000   (Mercantile - Buôn bán)
attr 100401 能力_生存_探索 12000   (Explore - Thám hiểm)
attr 100401 能力_生存_识图 12000   (Pathfinding - Nhận biết bản đồ)
attr 100401 能力_生存_驯兽 12000   (Beast Taming - Thuần thú)
```

## 7. HỌC VÕ CÔNG (kungfu)

```
kungfu 0 130631 1   (Cruel World - Legend)
kungfu 0 130641 1   (Overcoming Hardship - Legend)
kungfu 0 130651 1   (Six Character Charm - Legend)
kungfu 0 130661 1   (Tianlai Magic Sound - Legend)
kungfu 0 130671 1   (The Silent Mountain)
kungfu 0 130681 1   (Nine Flow Unification - Legend)
kungfu 0 130691 1   (Hidden Dragon, Don't Use - Legend)
kungfu 0 130111 1 Revitalization
kungfu 0 130081 1 New Future
kungfu 0 130181 1 Scattered Petals
kungfu 0 130101 1 Ten Thousand Sword (Legend)
kungfu 0 130171 1 Rainstorm Flower
kungfu 0 130381 1 Heaven Breaker (Legend)
kungfu 0 130121 1 Confucius Era
kungfu 0 130481 1 Star Casher
kungfu 0 130221 1 Soulbreaker Mist
kungfu 0 130201 1 Red Lotus Sinful Flame
kungfu 0 130151 1 Money Over Survival
kungfu 0 130681 1 Nine Flow Unification (Legend)
kungfu 0 130131 1 Buddha Golden Body
kungfu 0 130781 1 Feather and Blow snow
kungfu 0 130231 1 Muscle Relaxant Incense
kungfu 0 130881 1 Origin Qi (Legend)
kungfu 0 130291 1 Earthquake
kungfu 0 130271 1 Pircing Spear
kungfu 0 130091 1 Dust Clearing
kungfu 0 130071 1 Ferocious Dragon Charge
kungfu 0 130061 1 Human Wave Tactic
kungfu 0 130051 1 No Escape
kungfu 0 130021 1 Shattering Thunder
kungfu 0 130241 1 Flying Sand Kick
kungfu 0 130031 1 Quicklime Rain
kungfu 0 130041 1 Soulchaser Words
kungfu 0 130011 1 Taichi Thirteen Forms
kungfu 0 130001 1 Marvelous Blade
kungfu 0 130141 1 Fall Black
kungfu 0 130251 1 Throw Rock
kungfu 0 130161 1 Decisive Throw
kungfu 0 130261 1 Head Buster
kungfu 0 130191 1 Throw Quicklime
kungfu 0 130211 1 Neutralizing Incese
kungfu 0 130281 1 Summon Hound
kungfu 0 130301 1 Thremor
kungfu 0 130801 1 Divine Flame Radiance
kungfu 0 130701 1 Flying Dragon In The Sky (Legend)
kungfu 0 130601 1 Leave No Stone Untouched
kungfu 0 130501 1 Cruel Crotch Kick
kungfu 0 130901 1 Blissful Ascen
kungfu 0 130511 1 Mountain Mover
kungfu 0 130521 1 Mountain Breaker
kungfu 0 130531 1 Life Replenishment
kungfu 0 130541 1 Water of Life (Legend)
kungfu 0 130551 1 Fluttering Butterfly 
kungfu 0 130561 1 Sword Shadow
kungfu 0 130571 1 Paintful Separation
kungfu 0 130581 1 Slaughtering Way
kungfu 0 130591 1 Seven Buddha Punishment word (Legend)
kungfu 0 130411 1 Drown In Riches
kungfu 0 130421 1 Over Bearing Stance
kungfu 0 130431 1 World Conqueror (Legend)
kungfu 0 130441 1 Devastating Spear
kungfu 0 130451 1 Wind Cyclone
kungfu 0 130471 1 Thunder Tribulation
kungfu 0 130461 1 Dragon Sword
kungfu 0 130491 1 Cloud Piercing Chopstick
kungfu 0 130311 1 Spear Blossom Essence
kungfu 0 130321 1 One Sword Anihilator
kungfu 0 130331 1 Infinity World (Legend)
kungfu 0 130341 1 Sword Qi Explotion
kungfu 0 130351 1 Friend n Bugs
kungfu 0 130361 1 Diamond Rush
kungfu 0 130371 1 Extermination Decree
kungfu 0 130391 1 Only One School (Legend)
kungfu 0 130611 1 Destruction Mines
kungfu 0 130621 1 Full Reversal (Legend)
kungfu 0 130631 1 Cruel World (Legend)
kungfu 0 130641 1 Overcoming Hardship (Legend)
kungfu 0 130651 1 Six Character Charm (Legend)
kungfu 0 130661 1 Tianlai Magic Sound (Legend)
kungfu 0 130671 1 The Silent Mountain
kungfu 0 130681 1 Nine Flow Unification (Legend)
kungfu 0 130691 1 Hidden Dragon, Dont Use (Legend)
kungfu 0 130711 1 Frozen Miles
kungfu 0 130721 1 Great Lai Slash (Legend)
kungfu 0 130731 1 Blood Demon Slash (Legend)
kungfu 0 130741 1 Falling Flower Petals
kungfu 0 130751 1 United Beast (Legend)
kungfu 0 130761 1 Diplomacy Before Violence
kungfu 0 130771 1 Phoenix Hairpin
kungfu 0 130791 1 Prism Light
kungfu 0 130811 1 Sword Of Storm
kungfu 0 130821 1 Devastating Strike
kungfu 0 130831 1 Air Breaking Blade
kungfu 0 130841 1 Violent Firestorm (Legend)
kungfu 0 130851 1 Thousand Hits
kungfu 0 130861 1 Heaven Breaker
kungfu 0 130871 1 Flame Toad Burst
kungfu 0 130891 1 Explosive Blast (Legend)
kungfu 0 130911 1 Chaos Of Jade Fragment (Legend)
kungfu 0 130921 1 Baidi Whirling Swordplay - Swan (Legend)
kungfu 0 130931 1 Baidi Whirling Swordplay - Agile (Legend)
```

## 8. FAMe - DANH TIẾNG THẾ LỰC

```
fame 3100 100   (Confucius - Nho gia)
fame 3200 100   (Taoist - Đạo gia)
fame 3300 100   (Shifa - Thích Pháp)
fame 3400 100   (Nine Faction - Cửu Lựu Môn)
fame 3500 100   (Melody - Miếu Âm Phường)
fame 3600 100   (Great Ant - Đại Nghĩa)
fame 3700 100   (Divine Flame - Thần Hỏa)
fame 3800 100   (Hidden Sword - Tàng Kiếm)
fame 3900 100   (Jiuli - Cửu Lê)
fame 4000 100   (Jiujang)
fame 4100 100   (Linlang)
fame 4200 100   (Ye Family)
fame 4300 100   (Chaiwang)
fame 4400 100   (Herobology)
fame 4600 100   (Beast Manor)
fame 4700 100   (Wanan Escort)
fame 4800 100   (Night Market)
fame 5100 100   (Cold Skin)
fame 5200 100   (Levitation)
fame 5600 100   (Bandit Chief)
fame 5700 100   (New Nine Faction)
fame 5800 100   (Swallow Nest)
fame 6000 100   (Yan Yun)
fame 6200 100   (General Mansion)
fame 6300 100   (Duke Kang)
fame 6400 100   (Duke Qi)
fame 6500 100   (Crime Investigation)
fame 6600 100   (Tomb Raider)
fame 6700 100   (Shamen)
fame 6800 100   (Tianjiu)
fame 6900 100   (Flying Eagle)
fame 7000 100   (Sea Jiao)
fame 7100 100   (Langya Sword)
fame 7200 100   (Black Robe)
fame 7300 100   (Baoguo)
fame 7400 100   (Glittering Artifact)
fame 7500 100   (Tower of Prosperity)
fame 7600 100   (Yunlin)
```

## 9. ITEM - VẬT PHẨM (mẫu)

```
item 32121,100    (Item ID, số lượng)
item 32121,1
```

### Mẫu Item ID thông dụng:
```
20001  Steamed Bun (Bánh hấp)
20002  Steamed Bread (Bánh mì hấp)
23001  Đan dược hồi máu
23801  Bear Soul Pill (Thể chất +1)
24401  Tam Tự Kinh (Nhân đức +1)
14001  Lime Powder (Ám khí)
14041-14065  Các loại ám khí
16001  Wooden Barrel (Thùng gỗ)
16003  Fishing Rod (Cần câu)
16005  Mining Pick (Cúp khai thác)
16102  Low-grade Incense (Hương cấp thấp)
16201  Medium-grade Incense (Hương cấp trung)
16301  High-grade Incense (Hương cấp cao)
16302  Gold Bean (Kim đậu - tiền)
18101-18407  Các loại độc dược
22501  Small Berries (Quả nhỏ)
22601  Orange (Cam)
24401-24499  Các loại sách/điển tịch
29501  Trang sức chưa giám định
29555  Đan dược chưa giám định
```

### Nguồn tham khảo ID đầy đủ:
1. **Fandom Wiki (EN)**: https://heros-adventure-road-to-passion.fandom.com/wiki/Items
2. **Wiki Trung (物品图鉴)**: https://heros-adventure-wiki.xd.cn/items
3. **18183 ID List**: https://www.18183.com/gonglue/202303/4504885.html

## 10. LỆNH MOD 5PLAY (bản MOD đặc biệt)

Nếu dùng bản MOD từ 5play.org:
- `5play-give-all` - Nhận tất cả vật phẩm trong game
- `5play-give-item ITEM_ID SỐ_LƯỢNG` - Nhận vật phẩm cụ thể

---

## VỀ THÀNH TỰU (ACHIEVEMENTS)

**Không có lệnh console để mở khóa toàn bộ thành tựu.** Thành tựu trong game yêu cầu hoàn thành điều kiện cụ thể (VD: đạt cấp 100, sống 100 ngày, chỉ số đạt 15, v.v.). Bạn có thể dùng các lệnh attr trên để set chỉ số và mở khóa một số thành tựu tương ứng.

---

## MẸO NHANH

Muốn set **tất cả chỉ số cơ bản + đạo đức = 25** cùng lúc, copy hết đoạn này paste vào console:

```
attr 100401 臂力 25
attr 100401 敏捷 25
attr 100401 悟性 25
attr 100401 福缘 25
attr 100401 体质 25
attr 100401 仁德 25
attr 100401 义气 25
attr 100401 礼节 25
attr 100401 智慧 25
attr 100401 信用 25
attr 100401 勇气 25
```
