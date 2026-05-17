---
name: transcript-analysis
description: >
  Stage 1 của hệ thống học 2 giai đoạn. Dùng khi người dùng muốn extract kiến thức có cấu trúc từ
  raw transcript — nội dung sách, video YouTube, bài báo, podcast — và lưu vào knowledge-graph.json
  để socratic skill có thể dạy sau đó.
  Trigger khi người dùng paste transcript, share link video, hoặc nói "extract", "phân tích transcript",
  "lưu kiến thức", "tạo node", "thêm vào knowledge graph", hay khi họ đề cập tên nguồn tài liệu cụ thể.
  KHÔNG trigger khi người dùng muốn học hoặc ôn tập — đó là socratic skill.
  KHÔNG trigger khi người dùng hỏi câu hỏi factual đơn giản về nội dung — trả lời thẳng.
  Output của skill này là input của socratic skill: các node trong knowledge-graph.json.
compatibility:
  - python3.10+ (scripts/check_setup.py, content_mapper.py, validate_node.py, write_node.py)
  - optional: yt-dlp (YouTube transcript download), faster-whisper (audio transcription)
---

## When to use

Dùng skill này khi:
- Người dùng muốn biến nội dung thô (transcript, bản tóm tắt, chapter) thành structured knowledge nodes
- Người dùng cần thêm kiến thức mới vào một domain hiện có (`mandarin`, `math-for-ai`, `ai-concept`, `skill-creator`, `book`)
- Người dùng muốn re-extract một node cũ vì `needs_restructure: true` hoặc source đã cũ

Không dùng khi:
- Người dùng chỉ muốn hiểu hoặc tóm tắt nội dung (không cần lưu vào graph)
- Người dùng muốn học từ kiến thức đã có → dùng socratic skill
- Người dùng hỏi câu hỏi quick factual

---

## Setup

Trước lần đầu tiên dùng skill trên một domain mới, chạy:

```
python scripts/check_setup.py
python scripts/check_setup.py --domain {domain}
```

Xem output. Fix mọi FAIL trước khi tiếp tục. WARN là optional tools (yt-dlp, faster-whisper) — không bắt buộc nếu transcript đã có sẵn dạng text.

---

## Inputs the skill needs

**Required:**
- Transcript text — paste trực tiếp, hoặc path đến `.txt` / `.md` file
- Domain — một trong: `mandarin`, `math-for-ai`, `ai-concept`, `skill-creator`, `book`
- Source type — `youtube` | `book` | `article` | `podcast` | `other`
- Source name — tên channel, tên sách, tên tác giả

**Optional:**
- Source section hint — "phút 0–45", "Chapter 3–5" (giúp content_mapper chính xác hơn)
- `--min-nodes N` — override minimum yield nếu biết trước nội dung dày/mỏng
- Existing node key — nếu re-extracting (`--mode update`)

**Graceful degradation:**
- Nếu domain chưa được confirm → assume domain từ context, nêu assumption rõ ràng, proceed
- Nếu source type không rõ → default `youtube`, note assumption
- Nếu transcript quá dài cho 1 session → propose splitting by section, extract section by section

---

## Process

### Step 1 — Setup Check

```
python scripts/check_setup.py --domain {domain}
```

Confirm: domain path exists, `knowledge-graph.json` valid JSON, Python ≥ 3.10.  
**Gate:** Nếu domain path FAIL → tạo folder và empty `knowledge-graph.json` trước khi tiếp tục.

---

### Step 1.5 — Preprocess (chỉ cần cho ASR transcripts)

Nếu transcript có format `[MM:SS]` (YouTube, podcast ASR output) — bắt buộc phải preprocess trước Step 2. Nếu transcript đã là structured text (markdown headers, book chapters) — bỏ qua step này.

```
python scripts/preprocess_transcript.py --input transcript.txt --output clean.txt
```

Script sẽ:
- Strip timestamps `[00:00]`
- Merge fragmented ASR lines vào coherent paragraphs
- Detect topic pivots và tạo standalone title lines
- Output: clean text → feed vào content_mapper

Sau đó dùng `clean.txt` cho Step 2 thay vì `transcript.txt`.

---

### Step 2 — Content Mapping (GATE — phải confirm trước Step 3)

```
python scripts/content_mapper.py --input clean.txt --source-type {source_type}
```

Nếu có video title (recommended — giúp minimum yield chính xác hơn):
```
python scripts/content_mapper.py --input clean.txt --source-type youtube --video-title "3 sự thật về tình yêu"
```

Script sẽ:
- Detect section structure (headers, numbered lists, branch patterns)
- Classify sections as `branch` (container) hoặc `leaf` (extractable unit)
- Run minimum yield check (PASS / WARN)
- Parse video title for N-concept hint nếu có `--video-title`
- Output JSON tree + human-readable tree

**Sau khi chạy:**
1. Đọc tree output với người dùng
2. Adjust labels — script tạo key từ heuristic, không phải từ ngữ nghĩa
3. Confirm branch vs leaf — người dùng có thể disagree với classification
4. **Backbone verification**: Kiểm tra xem các load-bearing concepts có trong tree không:
   - Nếu title nói "N X" → N nodes tương ứng phải tồn tại
   - Mechanism/foundation concept (giải thích TẠI SAO cái gì đó works) → phải có node riêng
   - Main thesis → phải có depth-1 leaf
5. **Confirm yield** — nếu WARN, quyết định có split thêm không

**Không proceed đến Step 3 nếu người dùng chưa confirm tree.** Tree là contract cho phần còn lại của session.

#### Backbone Audit — hard gate trước Step 3

Sau khi người dùng confirm tree, liệt kê tất cả backbone (load-bearing) concepts đã xác định ở bước 4:

```
Backbone concepts: [concept_1], [concept_2], [concept_3], ...
```

Với mỗi backbone concept, kiểm tra nó có leaf node tương ứng trong confirmed tree không:
- **CÓ** → tiếp tục.
- **KHÔNG** → một trong hai:
  - Thêm leaf node mới vào tree và extract nó (nếu source có đủ nội dung)
  - Ghi rõ `[BACKBONE GAP: concept_name — source không cung cấp đủ để extract]` trong dossier

**Không được generate dossier khi còn backbone gap chưa xử lý.** Backbone gap chưa xử lý = thiếu xương sống = Socratic session sẽ thiếu nền tảng.

Đọc `references/granularity-guide.md` nếu không chắc về branch vs leaf.  
Đọc `references/source-types.md` để biết extraction rules theo từng source type.

---

### Step 3 — Per-Leaf Extraction

Với **mỗi leaf node** trong confirmed tree, thực hiện theo thứ tự:

**3a. Locate in transcript**
- Xác định `source_section` (timestamp, line range, chapter)

**3b. Map argument_flow**
- Trace rhetorical structure: hook → problem → mechanism → evidence → application
- Ghi dưới dạng arrow sequence

**3c. Extract vs Infer**

> **LANGUAGE RULE — bắt buộc:**
> - `extracted`: mirror source format. Nếu source không có dấu → OK, đây là verbatim quote. Ghi rõ trust_level.
> - Tất cả fields còn lại (`inferred`, `tiers.*`, `core_question`, `misconception_seeds`, `transfer_question`, `anchor_story`, `falsifiability`, `dig_deeper_questions`, `next_actions`): **viết tiếng Việt có dấu đầy đủ**, bất kể input có dấu hay không.
> - English technical terms (proper nouns, tên model, thuật ngữ chuyên ngành được dùng rộng rãi): **giữ nguyên tiếng Anh**. Không ép dịch khi dịch làm mất nghĩa hoặc mất thông tin domain.
> - Ví dụ giữ tiếng Anh: "negativity bias", "Deep Work", "Flow state", "neuroplasticity", "amygdala".
> - Ví dụ dịch: "cuốn sách" (không phải "book"), "chương" (không phải "chapter").

- `extracted`: Verbatim hoặc close-paraphrase từ source. Phải non-empty.
- `inferred`: Claude's synthesis — chỉ thêm nếu adds value, mark rõ là INFERRED
- Đọc `references/source-types.md` để biết khi nào dùng trust_level nào

**Fidelity calibration (bắt buộc tự check):**
- Nếu bạn cleaned up awkward phrasing → đó là INFERRED, không phải EXTRACTED
- Nếu `tiers.expert` chứa trade-offs/failure modes không có trong source (thường xảy ra với 10-min YouTube videos) → mark INFERRED, add field `"inferred"` riêng
- Short YouTube/podcast source → tier expert sẽ gần như luôn là INFERRED. Đó là OK — nhưng phải label đúng.

**3d. Preserve anchor_story**
- Tìm story, case study, hoặc ví dụ cụ thể trong section
- Lưu vào `anchor_story` — không subject to falsifiability check
- Nếu không có story → `anchor_story: ""`

**3e. Falsifiability check**
- Với main claim trong `extracted`: "Nếu claim này sai, evidence nào sẽ xuất hiện?"
- Ghi kết quả vào `falsifiability` — kể cả khi không tìm được evidence ngược chiều
- **Lý do:** Không check falsifiability → không biết claim là bold assertion hay supported fact → learner học với calibration sai

**3f. Write 3-tier explanation**
- `child`: Analogy-first, không jargon — viết như giải thích cho người 12 tuổi, không có background về topic
- `student`: Mechanism + context — viết như giải thích cho peer đang học cùng topic, biết basic terminology
- `expert`: Trade-offs, failure modes — viết như note cho chính mình sau 1 năm nghiên cứu, có thể dùng technical terms
- **Lý do:** Audience cụ thể tốt hơn instruction "văn phong tốt" — viết cho người 12 tuổi tự nhiên dẫn đến complete sentences và clear analogies.
- **Lý do:** 3 tiers không phải formatting — chúng là 3 different conceptual models. Viết `child` trước `expert` để tránh vocabulary contamination.

**3g. Misconception seeds (minimum 2)**
- Identify common wrong beliefs dựa trên structure của concept và argument_flow
- Dùng format: "[Wrong belief] — sai vì [correction hint]"
- **Lý do:** Socratic Layer 1 chỉ load misconception_seeds, không load full source_content. Nếu seeds không đủ → Layer 1 session không có target để challenge.

**3h. Transfer question**
- Một câu scenario-based, không thể trả lời bằng cách recall — phải apply trong new context
- Nếu câu hỏi có thể trả lời bằng "theo [concept] thì…" mà không cần suy nghĩ → viết lại

**3i. Dig deeper questions (4 Bloom levels)**
- apply, analyze, evaluate, create
- Mỗi câu phải target đúng level — "apply" không phải "describe"

**3j. Core question**
- Câu hỏi duy nhất mà concept này trả lời
- Đây là Socratic session entry point — phải specific và answerable

---

### Step 4 — Validate Node

```
python scripts/validate_node.py --node {concept_key}.json
```

Fix tất cả errors trước khi write. Không dùng `--skip-validate` trừ khi có lý do rõ ràng.

---

### Step 5 — Write Node

```
python scripts/write_node.py --domain {domain} --concept {concept_key} --node {concept_key}.json
```

Re-extraction (node đã tồn tại):
```
python scripts/write_node.py --domain {domain} --concept {concept_key} --node {concept_key}.json --mode update
```

`--mode update` giữ nguyên `learner_state` từ node cũ — không reset bloom_level hay mastery_probability.

Kiểm tra list sau mỗi batch:
```
python scripts/write_node.py --list --domain {domain}
```

---

### Step 6 — Relations Mapping

Sau khi tất cả leaves đã được extract và written:

1. Với mỗi leaf, xác định `prerequisites` (concepts must be understood first)
2. Với branch children: set `examples_of` → parent branch key
3. Xác định `contrasts_with` pairs (concepts that highlight each other by difference)
4. Xác định `supports` (this concept provides evidence for)
5. Xác định `cross_domain` — dùng format `"domain:concept_key"`

Update mỗi node với relations:
```
python scripts/write_node.py --domain {domain} --concept {concept_key} --node {concept_key}_with_relations.json --mode update
```

Đọc `references/extraction-examples.md` (Deep Work walkthrough) để xem ví dụ relations mapping đầy đủ.

---

### Step 7 — Output Learning Dossier

Generate human-readable summary từ tất cả nodes vừa written, theo format `assets/dossier-template.md`.

**Bắt đầu dossier bằng 2 sections (TRƯỚC Concept Tree):**

1. **## Tổng hợp** — 2 phần:

   **Phần 1 — Đoạn mở đầu (1–3 câu, viết tự nhiên, không phải bullet):**
   Cung cấp ngữ cảnh tổng thể để người đọc hiểu nguồn tài liệu trước khi đi vào chi tiết:
   - Tác giả/kênh là ai, background của họ là gì
   - Nguồn này được tạo ra trong bối cảnh nào (năm xuất bản, mục đích, vấn đề muốn giải quyết)
   - Đối tượng nên học nguồn này và tại sao nó đáng học
   Ví dụ: "Cal Newport là giáo sư khoa học máy tính tại Georgetown, chuyên nghiên cứu về năng suất trong thời đại số. Cuốn *Deep Work* ra đời năm 2016 như một phản ứng trực tiếp với văn hóa làm việc phân tán của mạng xã hội và email liên tục. Đây là nguồn tài liệu nền tảng cho bất kỳ ai muốn xây dựng khả năng tập trung cao độ trong môi trường làm việc hiện đại."

   **Phần 2 — 4 câu cố định:**
   - Câu 1: "[Tên source] là [loại nội dung] về [topic] từ [author/channel]."
   - Câu 2: "Luận điểm cốt lõi là [1 câu thesis của toàn bộ nguồn]."
   - Câu 3: "Dossier này cover [N] concepts, trọng tâm là [tên 2–3 backbone nodes]."
   - Câu 4: "Sau khi học, bạn có thể [capability verb: phân tích / nhận diện / áp dụng] [specific thing]."

2. **## Mục lục** — numbered list format (không phải table):

   ```
   1. **concept_key** — [ý chính: 1 câu bài học / takeaway] _(bloom_target)_
   2. **concept_key** — [ý chính] _(bloom_target)_
   ```

   **Ý chính** ≠ câu hỏi cốt lõi. Ý chính là câu TRẢ LỜI — bài học mang về nhà, không phải câu hỏi để navigate.
   - Câu hỏi cốt lõi: "Tại sao não bộ ưu tiên ghi nhớ tiêu cực?" → dùng cho Socratic session
   - Ý chính: "Negativity bias là cơ chế tiến hóa, không phải điểm yếu — có thể tái lập trình" → dùng cho Mục lục

   **Luôn generate, kể cả khi chỉ có 1–5 nodes.** Mục lục là điều kiện bắt buộc, không phải optional.

   **Timing:** Viết Tổng hợp và Mục lục SAU KHI hoàn thành toàn bộ nodes — không viết trong lúc extraction vì chưa biết scope đầy đủ. Sau khi viết, đặt cả 2 sections ở ĐẦU dossier.

Dossier bao gồm (sau 2 sections trên):
- Confirmed tree (ASCII)
- Per-node summary (core_question + extracted + 3 tiers + misconception_seeds)
- Yield summary (leaf count vs minimum)
- Next steps checklist

Dossier là handoff document cho người dùng review trước session đầu tiên với socratic skill.

---

### Step 7.5 — Vietnamese Prose Review

Re-read mọi Claude-generated field trong dossier vừa viết. Thực hiện theo 3 substep sau:

#### 7.5a — Diacritic Sweep

Scan toàn bộ fields do Claude tạo ra (`inferred`, `tiers.*`, `core_question`, `misconception_seeds`, `transfer_question`, `anchor_story`, `falsifiability`, `dig_deeper_questions`, `next_actions`, phần Tổng hợp, Mục lục):

- [ ] Mọi từ tiếng Việt phải có đầy đủ dấu thanh và dấu phụ
- [ ] Kiểm tra đặc biệt các từ hay bị mất dấu khi mirroring nguồn ASR không dấu:
  - `nao bo` → `não bộ`, `toan bo` → `toàn bộ`, `cam xuc` → `cảm xúc`
  - `hoc tap` → `học tập`, `tu duy` → `tư duy`, `ky nang` → `kỹ năng`
  - `phuong phap` → `phương pháp`, `khai niem` → `khái niệm`
- [ ] Âm tiết không dấu trong câu tiếng Việt = lỗi — sửa hết, không để sót

**KHÔNG sửa `extracted` fields** — đây là source quotes, phải faithful với original kể cả khi source thiếu dấu.

#### 7.5b — English Retention Decision

Với mỗi thuật ngữ tiếng Anh xuất hiện trong Claude-generated fields, áp dụng rule sau:

**Giữ tiếng Anh** nếu dịch sang tiếng Việt sẽ (a) nghe không tự nhiên HOẶC (b) phá vỡ nhận diện của thuật ngữ trong cộng đồng:

| Ở lại tiếng Anh | Phải dịch sang tiếng Việt |
|---|---|
| Proper nouns: "Deep Work", "HEAL method", "Flow state" | book → cuốn sách |
| Thuật ngữ khoa học: "neuroplasticity", "amygdala", "HPA axis" | chapter → chương |
| Tên mô hình: "negativity bias", "monastic model" | concept → khái niệm |
| Domain standards không có tương đương tốt | method → phương pháp |

**Nếu giữ tiếng Anh** → bắt buộc thêm vào bảng **Thuật ngữ** trong dossier (lý do giữ + tương đương tiếng Việt nếu có).

Không được dịch gượng ép — nếu dịch làm hỏng ngữ nghĩa hoặc nghe buồn cười, đó là tín hiệu rõ rằng nên giữ tiếng Anh.

#### 7.5c — Văn phong & Cấu trúc câu

- [ ] Câu phải hoàn chỉnh (có subject + verb — không để fragments)
- [ ] Logical connectives giữa các ý ("Do đó...", "Cụ thể là...", "Điều này có nghĩa là...")
- [ ] Không có trailing fragments (câu bị cắt giữa chừng do context limit)
- [ ] Văn phong: giọng giải thích (explain) chứ không phải hướng dẫn (instruct)
- [ ] `tiers.child` phải dùng analogy, không dùng jargon — test: người 12 tuổi có hiểu không?

---

## Output

**Primary output:**  
Nodes written to `C:\Projects\Dashboard\5. Exhibit\{domain}\knowledge-graph.json`

**Secondary output:**  
Learning dossier (Markdown) — per-source summary for human review

**Contract with socratic skill:**  
Each node in `nodes{}` must have:
- `source_content.misconception_seeds` (≥2) — socratic Layer 1
- `source_content.transfer_question` — mastery gate
- `learner_state` với correct initial values (bloom_level=remember, mastery_probability=0.0, etc.)
- `bloom_target` — socratic uses this as progression ceiling

---

## References

- `references/granularity-guide.md` — when to split vs keep, minimum yield table
- `references/source-types.md` — extraction rules by source type, trust level decisions
- `references/extraction-examples.md` — Deep Work full walkthrough (12 nodes)
- `assets/node-schema.json` — JSON schema with all required fields and types
- `assets/dossier-template.md` — output format template
