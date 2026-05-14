# RECOVERY FILE — Hệ Thống Học 2 Giai Đoạn
*Tổng hợp toàn bộ thiết kế từ đầu đến hiện tại. Dùng để tiếp tục ở conversation mới.*
*Cập nhật lần cuối: 2026-05-14 — v2 (Q2/Q3/Q4 đã chốt)*

---

## 0. Mục Tiêu Tổng Thể

Xây dựng một **personal learning system** gồm 2 skill liên kết:

- **Stage 1 — Transcript Analysis Skill**: Lấy kiến thức từ sách/video → tổng hợp thành structured knowledge có thể học
- **Stage 2 — Socratic Teaching Skill**: Biến structured knowledge thành cuộc đối thoại với "người thầy Socrate" để internalize thực sự

Mục tiêu cuối: **"biến kiến thức thành của mình"** — hiểu ở cả 3 tầng (đứa trẻ 5 tuổi / sinh viên đại học / chuyên gia cùng ngành), có khả năng phản biện, và tự áp dụng được vào tình huống mới.

---

## 1. Kiến Trúc Tổng Thể

```
HỆ THỐNG 2 GIAI ĐOẠN

SOURCE (Book/YouTube transcript)
        ↓
┌───────────────────────────────────────┐
│  STAGE 1 — EXTRACTION SKILL           │
│  Input:  raw transcript               │
│  Output: nodes vào knowledge-graph    │
│          (source_content per concept) │
└───────────────────────────────────────┘
        ↓  (Prior Elicitation bootstrap belief_prior)
┌───────────────────────────────────────┐
│  STAGE 2 — SOCRATIC SKILL             │
│  Input:  knowledge-graph.json         │
│          (graduated context loading)  │
│  Output: learner_state updated        │
│          contradictions flagged       │
└───────────────────────────────────────┘
        ↓ (feedback loop — §6)
┌───────────────────────────────────────┐
│  knowledge-graph.json (unified)       │
│  Stage 1 writes: source_content       │
│  Stage 2 writes: learner_state        │
│  Hướng 10 writes: contradictions      │
│  Hướng 5 timestamps: last_reextracted │
└───────────────────────────────────────┘
```

---

## 2. File Structure Hoàn Chỉnh

```
transcript-analysis/
├── SKILL.md                    ← Stage 1 pedagogy engine
└── (output: writes nodes vào knowledge-graph.json)

socratic/
├── SKILL.md                    ← Stage 2 pedagogy engine
├── knowledge-graph.json        ← UNIFIED — thay thế preference.json + knowledge.md
├── misconception-types.json    ← Tier 1 universal types, read-only
├── scripts/
│   ├── update_graph.py         ← Chạy sau MỖI Q&A exchange (thay update_preference.py)
│   ├── diagnostic.py           ← Cold start, update sau từng câu
│   ├── review_scanner.py       ← Scan concepts đến hạn review
│   └── reextract_trigger.py    ← Monthly re-extraction với Stage 2 context
└── references/
    ├── cold-start.md
    ├── hint-protocol.md
    ├── context-loading.md      ← Graduated loading policy
    └── closing.md

math/SKILL.md                   ← Không thay đổi
mandarin/SKILL.md               ← Không thay đổi
code/SKILL.md                   ← Không thay đổi
```

---

## 3. STAGE 1 — Transcript Analysis Skill (Đã Quyết Định)

### 3.1 Source Typing
Skill tự detect và phân loại nguồn:

| Nguồn | Trust Level | Flag mặc định |
|---|---|---|
| Sách | EXTRACTED | Không flag thêm |
| YouTube/Opinion | INFERRED | [PERSONAL EXPERIENCE] [UNVERIFIED] |

### 3.2 Extraction Architecture

**Bước 1 — Source Classification**
Skill hỏi hoặc tự detect: "Đây là transcript từ nguồn nào?" → thay đổi extraction logic tương ứng.

**Bước 2 — Falsifiability Check (Q2 Hướng 3 — đã chọn)**
Sau mỗi extracted claim, skill tự hỏi:
> "Nếu claim này sai, evidence nào trong transcript sẽ mâu thuẫn?"
- Tìm được evidence ngược chiều → ghi chú mâu thuẫn
- Không tìm được evidence để falsify → đánh dấu `[WEAK GROUNDING]`

**Bước 3 — Separation of Concerns**
Mọi output đều tách rõ:
- `EXTRACTED:` những gì speaker nói rõ ràng
- `INFERRED:` những gì skill suy ra từ context

### 3.3 Output Format — Learning Dossier

```markdown
## Concept: [Tên khái niệm]

**Source:** [Book | YouTube — tên kênh/sách]
**Trust level:** EXTRACTED | INFERRED
**Flags:** [PERSONAL EXPERIENCE] [UNVERIFIED] [WEAK GROUNDING] — nếu có

---

**EXTRACTED:** [Trích nguyên ý chính từ transcript]
**INFERRED:** [Suy luận của skill từ context]
**Falsifiability:** [Evidence ngược chiều nếu có, hoặc "Không tìm được"]

---

### 3 Tầng Giải Thích

**🧒 Tầng 1 — Đứa trẻ 5 tuổi**
[Analogy đơn giản, không dùng từ kỹ thuật]

**🎓 Tầng 2 — Sinh viên đại học**
[Mechanism + context, giải thích tại sao]

**🔬 Tầng 3 — Người cùng ngành**
[Concise, academic vocabulary, dense]

---

### ❓ Câu Hỏi Để Đào Sâu
- **Apply:** [Tình huống cụ thể để áp dụng]
- **Analyze:** [Câu hỏi phân tích cấu trúc]
- **Evaluate:** [Phản biện mạnh nhất chống lại concept này]
- **Create:** [Bạn sẽ thiết kế/làm gì dựa trên nguyên lý này?]

---

### ⚡ Next Action (làm trong 48h — chọn 1)
- [ ] [Action cụ thể 1]
- [ ] [Action cụ thể 2]
- [ ] [Action cụ thể 3]

### ⚠️ Open Questions
- [Điều không được giải thích trong transcript]
- [Điều cần verify từ nguồn khác]
```

### 3.4 Quyết Định Build: Stage 1 trước Stage 2
Stage 1 là epistemic foundation. Nếu extraction kém, Stage 2 sẽ produce *confident misunderstanding*. Thứ tự: Stage 1 v0.1 → test với 3 transcript thật → iterate cho đến khi output trông như "tôi muốn được hỏi về cái này."

---

## 4. The Handoff Problem (Điểm Yếu Kiến Trúc Quan Trọng Nhất)

### 4.1 Vấn đề
- Stage 1 biết: *"nguồn này nói gì"*
- Stage 2 cần: *"bạn đang tin gì — và tin sai ở đâu"*
- Không có cầu nối giữa hai thứ đó

### 4.2 Teacher's Paradox
Claude extract kiến thức trong Stage 1. Claude hỏi Socratic trong Stage 2. Claude biết đáp án vì vừa extract nó → Socratic trở thành *guided treasure hunt* thay vì genuine inquiry.

### 4.3 Giải Pháp: Prior Elicitation (Đã Chọn)
Trước khi bắt đầu Socratic loop, Stage 2 chạy:
```
"Trước khi chúng ta đi vào [concept], bạn nghĩ [concept] là gì?
Nói trong 1–2 câu, không cần đúng."
```
- Câu trả lời → `belief_prior` trong knowledge-graph.json
- Toàn bộ Socratic session challenge *belief đó*, không phải content trong source_content
- Claude có target để hỏi, thoát Teacher's Paradox

### 4.4 Content Loading — Graduated Loading Architecture (Đã Chọn: 4+5+7+8+10)

```
SESSION BẮT ĐẦU
      ↓
Layer 1 (default) — Hướng 7 + 8 [SEMANTIC CHUNK + SEEDS]
  Load: metadata + misconception seeds của concept đang hỏi
  Claude biết: "lỗi nào thường gặp"
  Claude không biết: "đáp án đúng"
      ↓
[Hint #1 → Hint #2]
      ↓
hint_fails = 2 → Layer 2 — Hướng 5 [LOAD ON STUCK]
  Load: full source_content của concept
  Dùng để: tạo Direct Explanation
  Claude giờ biết đáp án — chỉ sau khi học viên đã struggle
      ↓
[Transfer Question fail] → Layer 3 — Hướng 10 [ADVERSARIAL]
  Mode: "Tìm mọi lý do học viên CÓ THỂ vẫn hiểu sai"
  Generate câu hỏi nhắm vào weak points cụ thể
      ↓
Tương lai — Hướng 4 [TWO-AGENT, khi có API access]
  Agent A (full content) generate câu hỏi
  Agent B (blind) conduct conversation
  Giải quyết Teacher's Paradox hoàn toàn
```

**Nguyên tắc:** Claude escalate knowledge access cùng lúc với học viên escalate struggle.

---

## 5. STAGE 2 — Socratic Teaching Skill (Đã Thiết Kế Chi Tiết)

### 5.1 preference.json — Final Schema

```json
{
  "version": "1.0",
  "last_updated": "2026-05-14T09:00:00",
  "learner": {
    "learning_rate": 0.61,
    "sessions_total": 12,
    "bloom_history": ["understand", "understand", "apply", "apply", "analyze"]
  },
  "skills": {
    "math": {
      "knowledge_ref": "/math/knowledge.md",
      "quality_score": 3.4,
      "session_delta": "Hiểu factoring cơ bản, hổng ở discriminant < 0",
      "concepts": {
        "quadratic_equation": {
          "bloom_level": "apply",
          "bloom_target": "apply",
          "mastery_probability": 0.72,
          "belief_prior": "phương trình có chứa x bình",
          "consecutive_correct": 1,
          "hint_fails_streak": 0,
          "hint_fails_total": 3,
          "needs_restructure": false,
          "last_reviewed": "2026-05-14T09:00:00",
          "next_review":   "2026-05-21T09:00:00"
        }
      },
      "personal_misconceptions": {
        "skips_edge_cases": {
          "count": 3,
          "confirmed": true,
          "first_seen": "2026-05-10T09:00:00",
          "last_seen":  "2026-05-14T09:00:00",
          "examples": ["bỏ qua ± khi sqrt x²", "không check n=0"]
        }
      }
    },
    "mandarin": { "knowledge_ref": "/mandarin/knowledge.md", "quality_score": null, "session_delta": "", "concepts": {}, "personal_misconceptions": {} },
    "code":     { "knowledge_ref": "/code/knowledge.md",     "quality_score": null, "session_delta": "", "concepts": {}, "personal_misconceptions": {} }
  }
}
```

### 5.2 knowledge.md — Template Chuẩn

```markdown
# [Domain] Knowledge Graph

<!-- ═══ STATIC SECTION — chỉ bạn edit ═══ -->
## Curriculum Sequence
1. linear_equation      | bloom_target: apply
2. factoring            | bloom_target: apply
3. quadratic_equation   | bloom_target: apply

## Concept Definitions
### quadratic_equation
prerequisites: [linear_equation, factoring]
bloom_target: apply
core_question: "Tại sao phương trình bậc 2 có thể có 0, 1, hoặc 2 nghiệm?"
diagnostic_question:
  remember:   "Công thức nghiệm tổng quát ax²+bx+c=0 là gì?"
  understand: "Tại sao discriminant quyết định số nghiệm?"
  apply:      "Giải x²-5x+6=0, giải thích từng bước."
  analyze:    "Khi nào factoring tốt hơn công thức nghiệm?"
  evaluate:   "Phương pháp nào hiệu quả hơn cho bài này và tại sao?"
transfer_question: "Giải x²+x-6=0 bằng hai phương pháp khác nhau và so sánh."

<!-- ═══ DYNAMIC SECTION — Claude maintain ═══ -->
## Misconception Seeds
### quadratic_equation
- [2026-05-10] "sqrt(x²)=x, bỏ qua ±" — confirmed (3 lần)
- [2026-05-14] "áp công thức bậc 2 cho bậc 3" — unconfirmed (1 lần)

## Session Notes
- [2026-05-14] Hiểu factoring, lúng túng khi b²-4ac < 0
```

### 5.3 Socratic Loop — Policy (Hard Rules)

```
[Prior Elicitation: "Trước khi bắt đầu, bạn nghĩ X là gì?"]
        ↓
[Load belief_prior → target cho Socratic questions]
        ↓
[Câu hỏi Socratic — đúng Bloom level hiện tại]
        ↓
[Đúng?]
  YES → consecutive_correct += 1
        ≥ 2 → Bloom level up
        → update_preference.py correct
  NO  → Hint #1: Paul's CLARIFICATION question
        "Ý bạn là gì khi nói X? / Bạn đang giả định điều gì?"
        ↓
[Đúng sau Hint #1?]
  YES → update, tiếp tục
  NO  → Hint #2: Paul's IMPLICATION question + Edge case
        "Nếu điều đó đúng, điều gì xảy ra tiếp?"
        "Điều gì xảy ra nếu [boundary condition]?"
        ↓
[Đúng sau Hint #2?]
  YES → update, tiếp tục
  NO  → needs_restructure = true, FLAG
        → Offer choice: "(a) gợi ý thêm / (b) giải thích thẳng"
        ↓
      [Chọn direct]
        → "Bạn đang stuck ở điểm nào cụ thể?"
        → Direct Explanation
        → Transfer Question bắt buộc (xem §5.4)
```

**HARD RULES — không được vi phạm:**
- "Tôi không biết" → Hint #1, không skip
- Direct answer chỉ sau đúng 2 hint fails
- Không hỏi nhiều hơn 1 câu cùng lúc
- 2 hint fails = concept flagged `needs_restructure: true`

### 5.4 Transfer Question — 3 Loại

| Loại | Mô tả | Nguồn |
|---|---|---|
| Pre-defined | `transfer_question` field trong knowledge.md | Load file |
| Edge case | Boundary condition không nhắc trong explanation | Improvise |
| Teach-back | "Giải thích như đang dạy ai chưa biết gì" | Feynman |

Ưu tiên: pre-defined → edge case → teach-back.

### 5.5 Bloom Progression

```
remember → understand → apply → analyze → evaluate
```
- `consecutive_correct ≥ 2` tại level X → auto-upgrade X+1
- Bloom level trong knowledge.md là `bloom_target` (ceiling)

### 5.6 Spaced Review Schedule

| Bloom Level | Next Review | Timestamp Format |
|---|---|---|
| remember | +1 ngày | YYYY-MM-DDT09:00:00 |
| understand | +3 ngày | |
| apply | +7 ngày | |
| analyze / evaluate | +14 ngày | |
| needs_restructure | +1 ngày | |

### 5.7 Learning Rate & Quality Score

```
learning_rate = Σ(mastery × bloom_weight) / Σ(bloom_target_weight)
bloom_weights = {remember:1, understand:2, apply:3, analyze:4, evaluate:5}

quality_score = bloom_score    × 0.4
              + (1-hint_fail_rate) × 0.3
              + (1-misconception_density) × 0.3
```

- `quality_score`: LOG vào preference.json, không show học viên
- Trigger restructure alert nếu giảm 2 sessions liên tiếp
- Input vào learning_rate update

### 5.8 Misconception — 2 Tiers

- **Tier 1:** `misconception-types.json` — 6 universal types, read-only
  - overgeneralization, false_analogy, skips_edge_cases, confuses_correlation, incomplete_deduction, direction_reversal
- **Tier 2:** `preference.json → personal_misconceptions` per skill
  - count ≥ 2 → `confirmed: true` (auto via script)

### 5.9 Invoke Patterns

```bash
socratic review                    # review_scanner.py → list due concepts
socratic /math/knowledge.md        # load domain, detect concept
"ôn lại quadratic hôm qua sai"     # free-form → detect intent + load math
```

### 5.10 Cold Start — Diagnostic Protocol

1. Đọc knowledge.md của skill được gọi
2. Lấy 5 concept đầu trong Curriculum Sequence
3. Với mỗi concept: compose câu ở Bloom "understand" từ `diagnostic_question`
4. **Update preference.json sau từng câu** (không phải sau cả 5)
5. Script: `diagnostic.py --skill [math|mandarin|code]`

### 5.11 Mandarin — Đặc Thù

Scope: chỉ typing (không listening/speaking), mục tiêu apply và dùng tự nhiên.
Map theo Assimil lessons (Lesson 01–105).

| Level | Ý nghĩa thực tế |
|---|---|
| remember | Nhớ từ/cấu trúc khi nhìn |
| understand | Giải thích được khi nào dùng |
| apply | Viết câu đúng khi gợi ý topic |
| analyze | Nhận ra lỗi trong câu sai cho trước |
| evaluate | Viết tự nhiên không cần gợi ý |

### 5.12 SKILL.md Structure (Stage 2)

~200 lines, format: principles + IF/THEN + negative examples + pointers to references.

```markdown
## Role
Socratic Tutor. Mục tiêu: học viên hiểu conceptual, không nhớ đáp án.

## KHÔNG BAO GIỜ
- Give direct answer khi chưa qua 2 hint fails
- Accept "tôi không biết" làm lý do skip hint
- Hỏi nhiều hơn 1 câu cùng lúc
- Skip Prior Elicitation khi concept chưa có belief_prior

## Negative Examples
❌ "Đáp án là X vì..." (trước khi hint 2 lần)
❌ "OK, bạn chưa biết, vậy tôi giải thích..." (sau "tôi không biết")
✓  "Thử nghĩ theo hướng này: nếu X xảy ra, điều gì theo sau?"
```

---

## 6. Feedback Loop — Kiến Trúc Đã Chốt (Hướng 5 + 9 + 10)

Ba hướng tạo thành một kiến trúc coherent với 3 tầng:

### Tầng 1 — Hướng 9: Unified Knowledge Graph (xương sống)

Thay vì `knowledge.md` + `preference.json` riêng biệt, một file duy nhất:

```json
{
  "nodes": {
    "quadratic_equation": {
      "domain": "math",
      "bloom_target": "apply",
      "prerequisites": ["linear_equation", "factoring"],

      "source_content": {
        "core_question": "Tại sao bậc 2 có thể có 0, 1, hoặc 2 nghiệm?",
        "tiers": { "child": "...", "student": "...", "expert": "..." },
        "misconception_seeds": ["sqrt(x²)=x bỏ qua ±"],
        "transfer_question": "Giải x²+x-6=0 bằng hai phương pháp...",
        "last_reextracted": "2026-05-14"
      },

      "learner_state": {
        "belief_prior": "phương trình có chứa x bình",
        "bloom_level": "apply",
        "mastery_probability": 0.72,
        "consecutive_correct": 1,
        "hint_fails_total": 3,
        "needs_restructure": false,
        "next_review": "2026-05-21T09:00:00",
        "personal_misconceptions": {
          "skips_edge_cases": { "count": 3, "confirmed": true }
        }
      },

      "contradictions": [
        {
          "date": "2026-05-14",
          "source_says": "discriminant âm → vô nghiệm thực",
          "learner_believes": "discriminant âm → không giải được",
          "resolved": false
        }
      ]
    }
  }
}
```

### Tầng 2 — Hướng 10: Contradiction Flag (detection mechanism)

Mỗi khi Stage 2 phát hiện `learner_belief ≠ source_content`:
- Ghi vào `contradictions[]` của node
- Không auto-resolve — bạn quyết định cái nào đúng
- Stage 1 khi re-extract sẽ load contradictions list như context

### Tầng 3 — Hướng 5: Periodic Re-extraction (maintenance cycle)

Trigger thủ công hoặc `reextract_trigger.py` nhắc khi:
- `last_reextracted` > 30 ngày
- `contradictions` có unresolved items

Stage 1 re-extract với prompt bổ sung:
```
"Những contradiction này đã được ghi nhận: [list].
Re-extract với lens đó — nguồn gốc giải thích được mâu thuẫn không?"
```

---

## 7. Exit Criterion — "Kiến Thức Đã Thành Của Mình" (Đã Chốt)

### Framework: 2 Tầng + 1 Ongoing Tracker

```
TẦNG 1 — MASTERED (bắt buộc cả 3):

  ✓ Hướng 1:  Transfer question 100% không hint
               Tình huống mới, reasoning rõ ràng
               → "Bạn có thể áp dụng không?"

  ✓ Hướng 8:  Edge case generation
               Tự nghĩ boundary condition Stage 1 không mention
               → "Bạn biết giới hạn của nó không?"

  ✓ Hướng 13: "What would break this?"
               Tự xác định điều kiện khiến concept sai hoàn toàn
               → "Bạn biết khi nào không nên dùng nó không?"

  Lý do 3 bắt buộc: 8 và 13 là hai mặt của boundary mapping.
  Pass 1+8: biết "khi nào đúng" nhưng không biết "khi nào sai."
  Pass 1+13: biết failure modes nhưng không biết boundary đúng.
  Cả 3 mới là complete boundary knowledge.

──────────────────────────────────────────

TẦNG 2 — INTERNALIZED (sau 7–14 ngày, chọn 1 trong 2):

  ✓ Hướng 11: Analogy mới tự tạo
               Không được dùng analogy của Stage 1
               → "Bạn hiểu structure, không phải nhớ example"

  OR

  ✓ Hướng 12: Compression test
               Giải thích trong 5 câu → 2 câu → 1 câu, vẫn coherent
               → "Bạn biết cái gì là cốt lõi"

  INTERNALIZED là prerequisite cho concept tiếp theo trong curriculum.
  MASTERED không đủ — chỉ mastered = có thể pass test.

──────────────────────────────────────────

ONGOING TRACKING (không phải exit gate):

  Hướng 15: Prediction accuracy
             Trước mỗi bài tập/ví dụ: dự đoán kết quả + lý do
             Log vào node: prediction_score (rolling)
             Khi prediction_score tăng đều → internalization đang xảy ra
             Không dùng để block progress — chỉ để calibrate
```

### Tất Cả Proxies (tham khảo)

| # | Proxy | Loại | Vai trò |
|---|---|---|---|
| 1 | Transfer question 100% | Generative | **Bắt buộc Tầng 1** |
| 8 | Edge case generation | Boundary-extend | **Bắt buộc Tầng 1** |
| 13 | "What would break this?" | Boundary-destroy | **Bắt buộc Tầng 1** |
| 11 | Analogy mới tự tạo | Structural | **Tầng 2 option A** |
| 12 | Compression test 1 câu | Essence | **Tầng 2 option B** |
| 15 | Prediction before answer | Calibration | **Ongoing tracker** |
| 14 | Spontaneous cross-domain connection | Emergent | Signal mạnh nhất, không thể fake |

---

## 8. Vấn Đề Kiến Trúc — Trạng Thái Hiện Tại

| # | Câu hỏi | Trạng thái |
|---|---|---|
| A | Content loading: Stage 2 load gì? | ✅ **ĐÃ CHỐT** — Graduated: seeds→full→adversarial |
| B | Feedback loop: Stage 1 ↔ Stage 2 sync | ✅ **ĐÃ CHỐT** — Unified graph + contradiction flags + monthly re-extract |
| C | Exit criterion | ✅ **ĐÃ CHỐT** — 2 tầng: mastered (transfer+edge) / internalized (analogy/compress) |
| D | Mandarin knowledge.md cụ thể | Thấp — sau Stage 1 done |
| E | Code skill đặc thù | Thấp — sau Stage 1 done |
| F | Re-entry protocol sau gap dài | Thấp |

---

## 9. Build Plan

### Phase 1 (Tiếp theo): Stage 1 — Transcript Analysis Skill
- [ ] Viết `transcript-analysis/SKILL.md`
- [ ] Định nghĩa schema node trong `knowledge-graph.json` (Stage 1 populates `source_content`)
- [ ] Test với 3 transcript thật (1 sách, 1 YouTube, 1 hỗn hợp)
- [ ] Iterate cho đến khi output trông như "tôi muốn được hỏi về cái này"

### Phase 2: Stage 2 — Socratic Teaching Skill
- [ ] Viết `socratic/SKILL.md` (Prior Elicitation + Graduated Loading + Hard Rules)
- [ ] Viết `misconception-types.json`
- [ ] Viết `scripts/update_graph.py` (unified graph writer)
- [ ] Viết `scripts/diagnostic.py`
- [ ] Viết `scripts/review_scanner.py`
- [ ] Viết `scripts/reextract_trigger.py`
- [ ] Viết `references/hint-protocol.md` (Hint #1 Clarification / Hint #2 Implication)
- [ ] Viết `references/context-loading.md` (Graduated loading policy)
- [ ] Test integrated pipeline với Stage 1 output

### Phase 3: Domain Seed Files
- [ ] Seed initial nodes trong `knowledge-graph.json` cho math
- [ ] Seed nodes cho mandarin (map Assimil)
- [ ] Seed nodes cho code

---

## 10. Nguyên Tắc Thiết Kế Cốt Lõi

1. **Stage 1 extract "what source says." Stage 2 challenges "what you believe."** Hai thứ khác nhau — không substitute.
2. **Prior Elicitation trước mọi Socratic session.** Không có belief_prior = không có target = Socratic là theater.
3. **Falsifiability check là quality gate của extraction.** Không có falsifiability = extraction là paraphrase đẹp.
4. **3 tầng giải thích là output của Stage 1, exit signal của Stage 2.** Stage 1 tạo tầng 1. Stage 2 verify bằng teach-back tầng 1.
5. **2 hint fails = direct explanation.** Không có shortcut.
6. **Claude escalate knowledge access cùng lúc với học viên escalate struggle.** Seeds → full content → adversarial, không bao giờ ngược lại.
7. **Mastered ≠ Internalized.** Mastered = pass test. Internalized = tự tạo được analogy mới / edge case mới.
8. **Contradiction là data, không phải lỗi.** Khi learner belief khác source, đừng auto-correct — flag và để bạn quyết định.
9. **Kiến thức "thành của mình" xảy ra ngoài skill, không phải trong.** Skill là scaffold — learning xảy ra khi bạn dùng kiến thức trong tình huống thật.
10. **Knowledge graph là living document.** Stage 1 seeds, Stage 2 challenges, contradiction flags memory, re-extraction refreshes. Không có file nào là final.

---

*File này được generate từ quá trình thiết kế trong 2 conversations. Tiếp tục từ §8 — Vấn Đề Kiến Trúc Chưa Giải Quyết.*



Q4 — Hướng 1 + 8 + Ý Tưởng Mới
Bạn đã chọn hai proxy mạnh nhất — cả hai đều generative, không phải recall. Tinh thần đó đúng. Bổ sung thêm theo cùng hướng:
Hướng 11 — Analogy Generation (tự tạo, không dùng analogy của Stage 1)
Bạn phải tạo ra một analogy hoàn toàn mới mà Stage 1 output không dùng, để giải thích concept cho người khác. Nếu Stage 1 dùng ví dụ "cục pin", bạn phải dùng ví dụ khác. Tự tạo được analogy mới = hiểu cấu trúc sâu bên dưới, không phải nhớ example. Đây là Feynman Technique nhưng với constraint chống parroting.
Hướng 12 — Compression Test: giải thích trong ít từ hơn mỗi lần
Vòng 1: giải thích concept trong 5 câu. Vòng 2: 2 câu. Vòng 3: 1 câu. Mỗi lần cắt bỏ buộc bạn quyết định "cái gì là cốt lõi thực sự." Nếu câu 1-câu của bạn vẫn đúng và người khác hiểu được — bạn đã đạt tầng 3 (chuyên gia). Signal: người không thực sự hiểu sẽ không thể cắt dưới 3 câu mà vẫn coherent.
Hướng 13 — "What Would Break This?" Test
Stage 2 hỏi: "Điều kiện nào khiến concept này không còn đúng nữa?" Bạn phải tự xác định boundary của khái niệm — không phải chỉ biết nó hoạt động khi nào, mà biết nó thất bại khi nào. Đây là complement của Hướng 8 (edge case generation) nhưng theo chiều phá hủy thay vì mở rộng. Người chỉ nhớ công thức không thể trả lời câu này.
Hướng 15 — Prediction Before Answer
Trước khi làm một bài tập hoặc xem một ví dụ, bạn phải dự đoán kết quả và giải thích tại sao. Stage 2 record cả prediction lẫn actual outcome. Accuracy của prediction theo thời gian = calibration score. Người thực sự hiểu predict đúng ngay cả với variation mới; người chỉ nhớ công thức predict đúng cho familiar cases nhưng fail với novel variation.


Tốt. Bốn hướng này chưa conflict — chúng có thể tích hợp vào framework hiện tại nếu phân đúng vai trò. Để tôi map chúng trước khi cập nhật.

Vị Trí Của Từng Hướng
Hướng 13 và 8 là một cặp, không phải hai thứ riêng
Nhìn kỹ lại:

Hướng 8: "Concept này còn đúng ở đâu?" → boundary extension
Hướng 13: "Concept này bắt đầu sai ở đâu?" → boundary destruction

Hai câu hỏi này là hai mặt của cùng một thứ: boundary mapping. Người chỉ biết một trong hai chưa hiểu đầy đủ. Vì vậy 13 thuộc Tầng 1 cùng với 8, không phải tầng riêng.
Hướng 11 và 12 là hai cách đo cùng một thứ ở Tầng 2
Cả hai đều test structural understanding — bạn có hiểu bản chất của concept hay chỉ nhớ form. Đã được confirm ở Tầng 2, không thay đổi.
Hướng 15 là thứ khác hoàn toàn — không phải exit gate
Prediction before answer không phải là test một lần mà là calibration metric liên tục. Nó đo độ chính xác của mental model theo thời gian, không báo hiệu "xong" hay "chưa xong." Nếu đặt vào exit gate, bạn sẽ bị delay vô thời hạn vì calibration cần nhiều data points. Đúng vị trí của nó là ongoing tracking trong knowledge-graph.json.

Framework Đã Được Revise
TẦNG 1 — MASTERED (bắt buộc cả 3):

  ✓ Hướng 1:  Transfer question 100% không hint
               Tình huống mới, reasoning rõ ràng
               → "Bạn có thể áp dụng không?"

  ✓ Hướng 8:  Edge case generation
               Tự nghĩ boundary condition Stage 1 không mention
               → "Bạn biết giới hạn của nó không?"

  ✓ Hướng 13: "What would break this?"
               Tự xác định điều kiện khiến concept sai hoàn toàn
               → "Bạn biết khi nào không nên dùng nó không?"

  Lý do 3 bắt buộc, không phải 2 trong 3:
  Người chỉ pass 1+8 biết "khi nào đúng" nhưng không biết "khi nào sai."
  Người chỉ pass 1+13 biết failure modes nhưng không biết boundary đúng.
  Cả 3 mới là complete boundary knowledge.

──────────────────────────────────────────────

TẦNG 2 — INTERNALIZED (sau 7–14 ngày, chọn 1 trong 2):

  ✓ Hướng 11: Analogy mới tự tạo
               Không được dùng analogy của Stage 1
               → "Bạn hiểu structure, không phải example"

  OR

  ✓ Hướng 12: Compression test
               Giải thích trong 5 câu → 2 câu → 1 câu, vẫn coherent
               → "Bạn biết cái gì là cốt lõi"

──────────────────────────────────────────────

ONGOING TRACKING — không phải exit gate:

  Hướng 15: Prediction accuracy
             Trước mỗi bài tập/ví dụ: dự đoán kết quả + lý do
             Log: đúng/sai, cộng dồn thành prediction_score
             Dùng để: track calibration của mental model theo thời gian
             Khi prediction_score tăng đều → internalization đang xảy ra
             Không dùng để block progress