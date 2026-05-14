# AI CORE GUIDING FILE
### Đọc file này khi bắt đầu mỗi session học về AI Core

> **Mục đích duy nhất của file này:** Hiểu backbone về các concept về dữ liệu và trí tuệ nhân tạo
> Không phải thay thế tư duy — mà là nhắc nhở bạn TƯ DUY ĐÚNG CÁCH trước khi bắt đầu.
> Nếu sau 3 tháng bạn vẫn cần đọc file này, đó là tín hiệu bạn chưa internalize được framework.

---

## 0. ĐỌC CÁI NÀY TRƯỚC — 3 CÂU HỎI MỞ MỖI SESSION

Trước khi học bất cứ thứ gì hôm nay, trả lời 3 câu này trong đầu (hoặc viết ra):
1. **Mục tiêu hôm nay là học cái gì**


Nếu không trả lời được câu 1, **dừng lại** — bạn đang học không có đích.

---

## 1. MỤC TIÊU GỐC (ANCHOR)

Mục tiêu học AI Core của bạn không phải là "biết nhiều" — mà là:

- **Triển khai được** một AI pipeline thực sự (MCP, RAG, agent) trong một business context cụ thể
- **Tư duy được** về kiến trúc trước khi code — biết *tại sao* chọn giải pháp này, không phải chỉ *cách* làm
- **Nhìn thấy được** failure modes trước khi chúng xảy ra
- **Quyết định được** khi nào KHÔNG dùng AI

Nếu session hôm nay không đóng góp vào ít nhất một trong 4 điều trên — xem lại xem bạn đang đi đâu.

---

## 2. Tổ chức kiến thức

## 2.1 Tổ chức cây kiến thức

business-problem-framing
├── pain-point-identification
│   ├── cost-reduction
│   ├── revenue-increase
│   └── risk-mitigation
├── AI-vs-non-AI-decision
│   ├── automation-threshold
│   ├── complexity-ceiling
│   └── when-NOT-to-use-AI
├── ROI-framework
│   ├── baseline-measurement
│   ├── KPI-definition
│   └── attribution-model
└── stakeholder-alignment
    ├── executive-sponsorship
    ├── change-management
    └── success-criteria

2. USE CASE LAYER
use-case-prioritization
├── impact-feasibility-matrix
│   ├── impact-score
│   ├── feasibility-score
│   └── data-readiness-score
├── use-case-taxonomy
│   ├── classification
│   ├── generation
│   ├── extraction
│   ├── recommendation
│   ├── anomaly-detection
│   └── forecasting
├── anti-patterns
│   ├── AI-for-AI's-sake
│   ├── solution-looking-for-problem
│   └── premature-automation
└── industry-verticals
    ├── finance → fraud, credit, compliance
    ├── HR → screening, attrition, scheduling
    ├── supply-chain → demand, logistics, quality
    ├── customer-service → intent, routing, escalation
    └── legal → contract-review, clause-extraction

3. APPLICATION LAYER
AI-application-patterns
├── RAG (retrieval-augmented-generation)
│   ├── chunking-strategy
│   │   ├── fixed-size
│   │   ├── semantic
│   │   └── hierarchical
│   ├── embedding-model
│   │   ├── dense
│   │   └── sparse (BM25)
│   ├── vector-store
│   │   ├── Pinecone
│   │   ├── Weaviate
│   │   └── pgvector
│   ├── retrieval
│   │   ├── similarity-search
│   │   ├── hybrid-search
│   │   └── reranking
│   ├── generation
│   │   ├── prompt-template
│   │   ├── context-injection
│   │   └── citation-grounding
│   └── when-NOT-to-use-RAG
│       ├── data-too-dynamic
│       ├── latency-too-low
│       └── structured-data-better
├── fine-tuning
│   ├── full-fine-tune
│   ├── LoRA
│   ├── QLoRA
│   ├── instruction-tuning
│   ├── RLHF
│   └── when-NOT-to-fine-tune
│       ├── data-insufficient (<1K samples)
│       ├── task-solvable-with-prompting
│       └── cost-prohibitive
├── prompt-engineering
│   ├── zero-shot
│   ├── few-shot
│   ├── chain-of-thought
│   ├── system-prompt-design
│   ├── output-format-control
│   └── prompt-injection-defense
├── agentic-AI
│   ├── agent-loop
│   │   ├── perceive
│   │   ├── plan
│   │   ├── act
│   │   └── reflect
│   ├── tool-use
│   │   ├── function-calling
│   │   ├── MCP (Model Context Protocol)
│   │   └── API-integration
│   ├── memory
│   │   ├── in-context
│   │   ├── external (vector-DB)
│   │   └── episodic
│   ├── orchestration
│   │   ├── LangChain
│   │   ├── LangGraph
│   │   ├── CrewAI
│   │   └── Semantic-Kernel
│   ├── multi-agent
│   │   ├── supervisor-pattern
│   │   ├── peer-to-peer
│   │   └── hierarchical
│   └── human-in-the-loop
│       ├── approval-gate
│       ├── override-mechanism
│       └── audit-trail
└── trade-off-triangle
    ├── latency
    ├── accuracy
    └── cost

4. MODEL LAYER
model-lifecycle
├── model-selection
│   ├── open-source vs proprietary
│   ├── size vs performance
│   └── benchmark-evaluation
├── training
│   ├── data-preparation
│   ├── hyperparameter-tuning
│   └── compute-planning
├── evaluation
│   ├── offline-metrics
│   │   ├── accuracy
│   │   ├── F1
│   │   ├── BLEU / ROUGE
│   │   └── perplexity
│   ├── online-metrics
│   │   ├── task-completion-rate
│   │   ├── user-satisfaction
│   │   └── click-through
│   └── business-metrics
│       ├── cost-reduction-%
│       ├── time-saved
│       └── revenue-impact
├── deployment
│   ├── batch-inference
│   ├── online-inference
│   ├── streaming-inference
│   └── edge-inference
├── monitoring
│   ├── model-drift
│   │   ├── data-drift
│   │   ├── concept-drift
│   │   └── prediction-drift
│   ├── performance-degradation
│   └── shadow-mode
└── versioning
    ├── model-registry
    │   ├── MLflow
    │   └── Weights-and-Biases
    ├── A/B-testing
    ├── canary-deployment
    └── rollback-strategy

5. DATA LAYER
data-engineering
├── data-contracts ← CRITICAL
│   ├── schema-definition
│   │   ├── field-types
│   │   ├── constraints
│   │   └── semantic-rules
│   ├── SLA
│   │   ├── freshness (latency)
│   │   ├── completeness (volume)
│   │   └── uptime %
│   ├── schema-evolution
│   │   ├── backward-compatible
│   │   ├── breaking-change
│   │   └── version-control
│   ├── ownership-stewardship
│   │   ├── producer
│   │   └── consumer
│   └── enforcement
│       ├── validation-gate
│       └── quarantine-on-violation
├── data-lineage ← CRITICAL
│   ├── column-level-lineage
│   ├── table-level-lineage
│   ├── blast-radius
│   └── tools
│       ├── OpenLineage
│       ├── DataHub
│       └── dbt-lineage
├── data-observability ← CRITICAL
│   ├── freshness-monitor
│   ├── volume-monitor
│   ├── schema-change-monitor
│   ├── distribution-monitor
│   └── tools
│       ├── Monte-Carlo
│       ├── Soda
│       └── Great-Expectations
├── data-quality
│   ├── completeness
│   ├── accuracy
│   ├── consistency
│   ├── timeliness
│   └── validity
├── ingestion
│   ├── batch
│   │   ├── ETL
│   │   └── ELT
│   ├── streaming
│   │   ├── Kafka
│   │   └── Pulsar
│   └── CDC (change-data-capture)
├── storage
│   ├── data-lake
│   │   ├── raw-zone
│   │   ├── curated-zone
│   │   └── consumption-zone
│   ├── data-warehouse
│   │   ├── Snowflake
│   │   ├── BigQuery
│   │   └── Redshift
│   └── lakehouse
│       ├── Delta-Lake
│       └── Apache-Iceberg
├── transformation
│   ├── dbt
│   │   ├── model
│   │   ├── test
│   │   └── source
│   └── Spark
├── feature-store
│   ├── online-store (low-latency)
│   ├── offline-store (training)
│   ├── feature-definition
│   ├── feature-reuse
│   └── tools
│       ├── Feast
│       └── Tecton
└── orchestration
    ├── Airflow
    ├── Prefect
    └── Dagster

6. SYSTEM THINKING LAYER
system-thinking
├── abstraction-levels
│   ├── principle (không đổi)
│   ├── pattern (ít đổi)
│   ├── tool (đổi thường xuyên)
│   └── implementation
├── trade-off-analysis
│   ├── latency vs accuracy vs cost
│   ├── automation vs control
│   └── scale vs simplicity
├── failure-first-design
│   ├── failure-mode-taxonomy
│   │   ├── data-failure
│   │   │   ├── schema-mismatch
│   │   │   ├── data-drift
│   │   │   └── missing-data
│   │   ├── model-failure
│   │   │   ├── prediction-drift
│   │   │   ├── hallucination
│   │   │   └── version-regression
│   │   └── infra-failure
│   │       ├── timeout
│   │       ├── OOM
│   │       └── dependency-down
│   ├── fallback-policy
│   │   ├── graceful-degradation
│   │   ├── cache-last-good
│   │   └── rule-based-fallback
│   └── circuit-breaker
├── feedback-loops
│   ├── positive-loop
│   ├── negative-loop
│   └── delay-in-loop
├── bottleneck-identification
│   ├── Theory-of-Constraints
│   └── profiling
└── cost-model
    ├── compute-cost
    ├── inference-cost-per-request
    ├── storage-cost
    └── human-review-cost

7. INFRASTRUCTURE LAYER
MLOps-infra
├── CI/CD for ML
│   ├── unit-test (data + model)
│   ├── integration-test
│   └── deployment-pipeline
├── serving
│   ├── REST-API
│   ├── gRPC
│   ├── streaming
│   └── batch-job
├── scalability
│   ├── horizontal-scaling
│   ├── auto-scaling
│   └── load-balancing
├── caching
│   ├── semantic-cache
│   ├── prompt-cache
│   └── result-cache
└── cost-optimization
    ├── model-tiering
    ├── quantization
    └── distillation

8. GOVERNANCE LAYER
AI-governance
├── risk-management
│   ├── risk-taxonomy
│   │   ├── bias-risk
│   │   ├── hallucination-risk
│   │   ├── security-risk
│   │   └── regulatory-risk
│   └── risk-assessment
│       ├── impact-score
│       └── likelihood-score
├── compliance
│   ├── GDPR
│   ├── EU-AI-Act
│   └── industry-specific
├── access-control
│   ├── RBAC
│   └── data-classification
├── audit-trail
│   ├── model-decision-log
│   ├── data-access-log
│   └── human-override-log
└── model-cards
    ├── intended-use
    ├── limitations
    └── evaluation-results

9. EVALUATION LAYER (xuyên suốt mọi layer)
evaluation-framework
├── offline-evaluation
│   ├── benchmark-datasets
│   ├── held-out-test-set
│   └── adversarial-testing
├── online-evaluation
│   ├── A/B-test
│   ├── shadow-mode
│   └── canary-rollout
├── business-evaluation
│   ├── baseline-comparison
│   ├── counterfactual
│   └── attribution
└── anti-patterns
    ├── metric-gaming
    ├── data-leakage
    └── survivor-bias




## 2.2 Tổ chức cấp độ kiến thức

Tầng 0 — Nền tảng tư duy (học trước tiên)
📁 00_foundations/
├── 01_system_thinking/
│ ├── principles_vs_patterns_vs_tools.md nguyên lý
│ ├── graph_thinking_not_tree.md
│ ├── feedback_loops_and_delays.md
│ └── theory_of_constraints_applied.md
├── 02_decision_frameworks/
│ ├── WHEN_NOT_to_use_AI.md critical
│ ├── ai_vs_non_ai_decision_tree.md
│ └── context_collapse_by_company_size.md
└── 03_mental_models/
├── abstraction_levels_primer.md
├── tradeoff_triangles.md
└── failure_first_design.md
Tầng 1 — Case Studies thực chiến (học song song với lý thuyết)
📁 01_case_studies/ inductive
├── finance/
│ ├── jpmorgan_fraud_detection_postmortem.md
│ └── dbs_bank_1500_models_governance.md
├── supply_chain/
│ └── walmart_ai_lead_time_reduction.md
├── enterprise_automation/
│ ├── harness_mcp_pipeline_case.md MCP
│ └── morgan_stanley_gpt_advisor.md
└── _template/
└── case_study_template.md dùng mọi case
Tầng 2 — Cross-layer Knowledge (không học theo layer, học theo concern)
📁 02_cross_cutting_concerns/
├── evaluation/ xuyên suốt
│ ├── eval_at_business_layer.md
│ ├── eval_at_data_layer.md
│ ├── eval_at_model_layer.md
│ └── CLEAR_framework_enterprise.md
├── failure_taxonomy/ critical
│ ├── real_failures_catalogue.md
│ ├── postmortem_patterns.md
│ └── circuit_breaker_recipes.md
├── debt_model/
│ ├── data_debt.md
│ ├── model_debt.md
│ └── decision_debt.md
└── organizational_layer/ layer bị thiếu
├── change_management_playbook.md
├── stakeholder_failure_modes.md
└── culture_vs_technology.md
Tầng 3 — Domain Knowledge (theo layer gốc, đã tách principle/tool)
📁 03_domain_knowledge/
├── business_layer/
│ ├── principles/ → problem_framing, ROI_model
│ └── tools/ → canvas_templates, KPI_dashboards
├── data_layer/ foundation
│ ├── principles/ → contracts, lineage, observability
│ └── tools/ → dbt, airflow, monte_carlo [2025 state]
├── application_layer/
│ ├── principles/ → RAG_principles, agent_loop, tradeoffs
│ └── tools/ → langchain, MCP_protocol [dated: 2025-Q2]
├── model_layer/
│ ├── principles/ → selection_criteria, eval_frameworks
│ └── tools/ → mlflow, wandb [check for updates]
└── governance_layer/ mandatory
├── principles/ → risk_taxonomy, audit_trail
└── context/ → GDPR, EU_AI_Act, Vietnam_context
Tầng 4 — Practice & Build
📁 04_practice/
├── labs/ hands-on
│ ├── lab_01_data_contract_violation.md
│ ├── lab_02_rag_vs_finetuning_decision.md
│ └── lab_03_mcp_agent_harness.md
├── decision_checklists/
│ ├── pre_project_checklist.md
│ ├── data_readiness_scorecard.md
│ └── go_nogo_production_gate.md
└── maturity_model/
├── stage_1_experiment.md
├── stage_2_pilot.md
└── stage_3_scale.md
Meta — Quản lý kiến thức
📁 _meta/
├── LEARNING_SEQUENCE.md đọc đầu tiên
├── KNOWLEDGE_GRAPH.md → cross-refs giữa các node
├── TOOL_SHELF_LIFE.md → tools nào cần re-check 6 tháng/lần
└── OPEN_QUESTIONS.md → những gì bạn chưa biết

## 2.3 DEPENDENCY GRAPH (không phải tree)

> ⚠️ Đây là GRAPH, không phải hierarchy. Mỗi node phụ thuộc nhiều node khác.
> Đọc mũi tên là: "cần hiểu X trước khi Y có ý nghĩa"

```
BUSINESS PROBLEM
      │
      ▼
DATA REALITY ──────────────────────────────────────────┐
(contracts, quality, lineage, observability)           │
      │                                                 │
      ▼                                                 │
USE CASE SELECTION ◄───── WHEN NOT TO USE AI           │
      │                                                 │
      ▼                                                 │
APPLICATION PATTERN                                     │
(RAG / Fine-tune / Prompt / Agent)                     │
      │                                                 │
      ▼                                                 │
MODEL CHOICE                                            │
      │                                                 │
      ▼                                                 │
INFRA & DEPLOYMENT                                      │
      │                                                 │
      ▼                                                 │
EVALUATION ◄────────────────────────────────────────────┘
(đo từ đầu, không phải cuối)
      │
      ▼
GOVERNANCE & COST
      │
      ▼
FEEDBACK → quay lại BUSINESS PROBLEM

XUYÊN SUỐT TẤT CẢ: ORGANIZATIONAL & HUMAN FACTORS
(70% projects thất bại vì người, không phải kỹ thuật)
```

**Nguyên tắc đọc graph này:**
- Không node nào độc lập
- Data Reality ảnh hưởng mọi quyết định downstream
- Evaluation không phải bước cuối — nó là lens nhìn từ đầu
- Cost không chỉ là infrastructure — nó ảnh hưởng use case selection ngay từ layer 2

---

## 3. SYSTEM THINKING LENS — áp dụng vào MỌI thứ bạn học

> System thinking không phải một chương để học xong. Đây là cách nhìn bạn phải mang vào mọi session.

Khi gặp bất kỳ concept nào, hỏi:

| Câu hỏi | Tại sao quan trọng |
|---|---|
| Nó kết nối với node nào khác? | AI systems là graph, không phải island |
| Nếu thứ này fail, blast radius là gì? | Failure-first thinking |
| Trade-off là gì? (latency/accuracy/cost) | Không có free lunch |
| Feedback loop ở đây là gì? | Positive hay negative? Delay bao lâu? |
| Bottleneck thực sự nằm ở đâu? | Theory of Constraints — fix bottleneck, không fix noise |
| Tôi đang ở level nào? (principle / pattern / tool) | Tool thay đổi, principle ít thay đổi hơn |

---

## 4. ABSTRACTION LEVELS — đừng nhầm lẫn

```
PRINCIPLE  →  ít thay đổi (5-10 năm)
   │          VD: "data quality quyết định model quality"
   │              "evaluation phải đo business metric, không chỉ ML metric"
   ▼
PATTERN    →  thay đổi chậm (2-5 năm)
   │          VD: RAG pattern, Agent loop, Data Contract pattern
   │              Supervisor-worker multi-agent
   ▼
TOOL       →  thay đổi nhanh (6-18 tháng)
   │          VD: LangChain, LangGraph, CrewAI, Pinecone, dbt
   │          ⚠️ Học tool nhưng đừng confuse tool với pattern
   ▼
IMPLEMENTATION →  thay đổi rất nhanh (hàng tuần/tháng)
              VD: API version, config syntax, provider pricing
```

**Rule:** Khi đọc tutorial hay doc, luôn hỏi: *Cái này là principle, pattern, hay tool?*
- Nếu là tool → note shelf-life, có thể obsolete
- Nếu là principle → invest time hiểu sâu

---

## 5. MINIMUM VIABLE CORE — 20% tạo 80% giá trị

Học những thứ này trước. Phần còn lại có thể lookup khi cần.

### Tier 1 — CRITICAL (learn first, non-negotiable)

**Data:**
- Data quality dimensions (completeness, accuracy, consistency, timeliness)
- Data contracts: schema, SLA, ownership — *tại sao* chúng tồn tại
- Data lineage: blast radius khi có thay đổi
- What "data drift" looks like in production

**Decision Making:**
- When NOT to use AI (automation threshold, complexity ceiling)
- RAG vs Fine-tuning vs Prompting — decision criteria, không phải implementation
- Impact × Feasibility × Data Readiness matrix

**Evaluation:**
- Baseline-first mindset (bạn đang beat cái gì?)
- Offline metric ≠ Online metric ≠ Business metric
- A/B test design cơ bản

**Failure Modes:**
- Schema mismatch → pipeline fail
- Data drift → model decay
- Hallucination → trust erosion
- Premature automation → process collapse

### Tier 2 — IMPORTANT (learn in parallel with practice)

- RAG: chunking, embedding, retrieval, reranking
- Agent loop: perceive → plan → act → reflect
- MCP protocol: tool-use pattern, function calling
- MLOps: model registry, versioning, monitoring
- Cost model: inference cost per request, không chỉ training cost

### Tier 3 — REFERENCE (lookup when needed)

- Specific tool APIs (LangChain, dbt, Airflow, Pinecone)
- Fine-tuning implementations (LoRA, QLoRA)
- Advanced orchestration patterns (multi-agent hierarchical)
- Compliance specifics (GDPR, EU AI Act)

---

## 6. FAILURE TAXONOMY — học failure trước khi học success

> 60% thời gian production là debug failure. Biết failure modes = biết system.

### Data Failures
| Failure | Signal | Response |
|---|---|---|
| Schema mismatch | Pipeline đột ngột fail | Validation gate + quarantine |
| Data drift | Model accuracy giảm dần | Distribution monitor |
| Missing data | Null spike trong metrics | Freshness monitor + fallback |
| Volume anomaly | Đột ngột tăng/giảm record count | Volume monitor |

### Model Failures
| Failure | Signal | Response |
|---|---|---|
| Hallucination | Output confident nhưng sai | Grounding + citation + human review |
| Prediction drift | Metric drift không có data change | Retrain trigger |
| Version regression | Deploy mới làm metric xấu hơn | Canary + rollback strategy |
| Latency spike | P99 tăng đột ngột | Caching + model tiering |

### Infra Failures
| Failure | Signal | Response |
|---|---|---|
| OOM | Container crash | Quantization + batch size |
| Timeout | Request queue tăng | Circuit breaker + graceful degrade |
| Dependency down | Cascade fail | Fallback policy |

### Organizational Failures (thường bị bỏ qua)
| Failure | Signal | Response |
|---|---|---|
| No executive sponsor | Project bị deprioritize | Align trước khi build |
| No success criteria | "AI không hiệu quả" mà không đo được | Define KPI trước sprint 1 |
| Change resistance | User không dùng model | Change management song song |
| Metric gaming | Team optimize metric, không optimize outcome | Business metric > ML metric |

---

## 7. WHEN NOT TO USE AI — câu hỏi đầu tiên, không phải cuối cùng

Hỏi câu này ở mỗi layer, không chỉ một lần ở đầu:

**When NOT to build AI:**
- Rule-based logic giải quyết được → dùng rule
- Data không đủ, không sạch, không label → fix data trước
- Latency requirement < 50ms và accuracy quan trọng → rethink
- Không có baseline để compare → đo baseline trước
- Không có owner/operator sau deploy → đừng deploy

**When NOT to use RAG:**
- Data thay đổi real-time (< 1 phút freshness) → streaming pipeline
- Data có structure rõ ràng → SQL/traditional query
- Latency requirement quá thấp → cache hoặc precompute

**When NOT to fine-tune:**
- Chưa thử prompting → thử prompting trước
- Dưới 1K samples chất lượng cao → chưa đủ
- Cost prohibitive cho use case → dùng smaller model + prompting

**When NOT to build agent:**
- Task có thể giải bằng single LLM call → đừng thêm complexity
- Không có human-in-the-loop mechanism → quá rủi ro
- Latency không chấp nhận được với multi-step → redesign

---

## 8. TRADE-OFF TRIANGLE — không có free lunch

```
        ACCURACY
           /\
          /  \
         /    \
        /  ⚠️  \
       /        \
      /____________\
  LATENCY        COST
```

**Mỗi khi chọn giải pháp, explicitly articulate:**
- Bạn đang optimize cái nào?
- Bạn đang sacrifice cái nào?
- Business context nào justifies trade-off này?

VD: Fraud detection → optimize Accuracy (false negative cost cao), sacrifice Latency.
VD: Chatbot → optimize Latency, accept Accuracy thấp hơn một chút.

---

## 9. EVALUATION FRAMEWORK — đo từ ngày 1

> Nếu bạn chưa định nghĩa "thành công trông như thế nào" trước khi build, bạn không thể biết mình có thành công không.

### Hierarchy đo lường (từ quan trọng nhất đến ít nhất)

```
Business Metric      (revenue impact, cost saved, time reduced)
      ↑ drives
Online Metric        (task completion rate, user satisfaction, click-through)
      ↑ proxied by
Offline Metric       (F1, BLEU, accuracy trên held-out test set)
```

**Anti-pattern:** Optimize offline metric mà không check online/business metric.

### Baseline-first rule
Luôn hỏi: *"Model của tôi đang beat cái gì?"*
- Random baseline?
- Rule-based system hiện tại?
- Human performance?
- Previous model version?

Không có baseline = không có evaluation.

---

## 10. MCP & AGENTIC AI — focus area của bạn

Vì đây là mục tiêu học cụ thể, elevated lên đây:

### Agent Loop (principle, không thay đổi)
```
PERCEIVE → thu thập context, tools available, state hiện tại
    ↓
PLAN    → decompose task thành steps, chọn tools
    ↓
ACT     → call tools, execute
    ↓
REFLECT → kết quả có match expected không? Next step?
    ↓
(loop hoặc terminate)
```

### MCP (Model Context Protocol) — pattern level
- MCP là standardized interface để LLM giao tiếp với external tools/data
- Không phải magic — nó là function calling với schema chuẩn hóa
- Key question khi design: "Tool này có idempotent không? Nếu gọi 2 lần thì sao?"

### Human-in-the-loop — mandatory cho production
- Approval gate: human approve trước khi action irreversible
- Override mechanism: human có thể cancel mid-execution
- Audit trail: log mọi decision + input + output
- Không có HITL = không nên deploy agent vào production

### Harness Pattern (cho testing agent)
- Viết test case như test software: input → expected output
- Test failure modes explicitly (tool fail, context overflow, loop không terminate)
- Shadow mode trước: agent chạy song song, không thực sự execute

---

## 11. DATA LAYER — nền tảng của mọi thứ

### Data Contract Checklist (trước khi trust bất kỳ data source nào)
- [ ] Schema được document không? Field types, constraints, semantic rules?
- [ ] SLA: freshness bao nhiêu? Uptime %? Volume expected?
- [ ] Ai là producer? Ai là consumer? Ai chịu trách nhiệm khi break?
- [ ] Breaking change được thông báo như thế nào?
- [ ] Có validation gate không? Nếu violate thì data đi đâu?

### Data Observability — 5 signals cần monitor
1. **Freshness:** Data có đến đúng giờ không?
2. **Volume:** Số records có trong expected range không?
3. **Schema:** Schema có thay đổi không?
4. **Distribution:** Distribution của key fields có drift không?
5. **Referential integrity:** Foreign keys có valid không?

### Feature Store — khi nào cần?
Cần khi: cùng feature được compute bởi nhiều team, hoặc training/serving skew là vấn đề.
Không cần khi: còn đang experiment, chưa có 2+ model dùng chung feature.

---

## 12. ORGANIZATIONAL LAYER — thường bị bỏ qua, hay giết project

> 70% AI project failures là organizational, không phải technical. (McKinsey, Gartner)

### Pre-project checklist (trước khi code một dòng)
- [ ] Ai là executive sponsor? Họ có skin in the game không?
- [ ] Success criteria được define và đo được chưa?
- [ ] End user có được consult chưa? Họ có muốn dùng không?
- [ ] Ai sẽ maintain model sau khi team deploy xong?
- [ ] Nếu model wrong, business impact là gì? Ai chịu trách nhiệm?
- [ ] Change management plan có chưa?

### Stakeholder failure modes
- **HiPPO effect:** Highest Paid Person's Opinion override data → document và escalate
- **Scope creep:** "AI cũng có thể làm X, Y, Z" → scope lock trước
- **Success theater:** Report metric tốt nhưng không ai dùng → đo adoption, không chỉ accuracy

---

## 13. COST MODEL — ảnh hưởng mọi quyết định

| Cost Type | Ảnh hưởng đến | Cần estimate trước |
|---|---|---|
| Inference cost/request | Use case viability | Luôn luôn |
| Training cost | Build vs buy decision | Nếu xem xét fine-tune |
| Storage cost | Data retention policy | Nếu lưu nhiều data |
| Human review cost | Automation threshold | Nếu có human-in-the-loop |
| Monitoring cost | Observability investment | Production deployment |

**Rule of thumb:** Nếu inference cost > business value của một decision → reconsider.

---

## 14. FEEDBACK LOOPS — học từ production

### Positive loops (accelerating)
- Nhiều user → nhiều data → model tốt hơn → nhiều user (ví dụ: recommendation)
- ⚠️ Nguy hiểm: có thể amplify bias

### Negative loops (stabilizing)
- Model error → human correction → retrain → ít error hơn
- Tốt cho quality, nhưng cần monitoring để detect

### Delay trong loop
- Khoảng cách giữa deploy model và thấy business impact có thể là 2-4 tuần
- Đừng panic change model nếu chưa đủ observation window

---

## 15. SESSION ANTI-PATTERNS — những thứ hay làm chệch hướng

❌ **Tutorial chasing:** Học tutorial mà không build gì thực sự
→ Mỗi tutorial phải kết thúc bằng: "Tôi apply điều này vào problem X như thế nào?"

❌ **Tool collecting:** Cài LangChain, LangGraph, CrewAI, Semantic Kernel... nhưng chưa deploy một cái
→ Pick one, build something real, ship it

❌ **Architecture astronaut:** Design 7 layer trước khi có data
→ Start simple, add complexity khi simple fails

❌ **Metric confusion:** Optimize F1 score, không ai dùng model
→ Luôn map ML metric → business metric trước khi optimize

❌ **Premature scaling:** Infrastructure production-grade cho experiment
→ Experiment fast → validate → then productionize

❌ **Learning without teaching back:** Đọc nhiều nhưng không explain được
→ Sau mỗi concept, explain lại bằng lời của mình (không copy)

---

## 16. KNOWLEDGE DECAY — những gì cần re-check định kỳ

| Thứ | Review frequency | Lý do |
|---|---|---|
| Tool APIs (LangChain, dbt...) | Mỗi 3 tháng | Breaking changes, deprecation |
| Model benchmarks | Mỗi 3 tháng | New models thay đổi landscape |
| Cloud pricing | Mỗi 6 tháng | Cost model thay đổi |
| Governance/compliance | Mỗi 6 tháng | EU AI Act evolving |
| Orchestration patterns | Mỗi 6 tháng | MCP, agent patterns mature nhanh |
| Principles | Không cần — nhưng verify khi thực tế contradicts | |

---

## 17. OPEN QUESTIONS — honest về những gì chưa biết

> Thêm vào đây khi session tạo ra câu hỏi mới chưa có answer.

```
[ ] Vietnam context: AI deployment trong doanh nghiệp VN khác gì với case Western?
[ ] MCP maturity: Production-ready chưa, hay vẫn còn experimental?
[ ] Agent reliability: Làm thế nào đo reliability của agent trong production?
[ ] Data contract tooling: Trong small team (<50 người), implement data contract ở mức nào là đủ?
[ ] Fine-tune vs RAG: Threshold thực sự ở đâu ngoài lý thuyết?
```

---

## 18. QUICK REFERENCE — khi cần quyết định nhanh

### "Tôi nên dùng RAG hay Fine-tune?"
```
Bạn muốn model biết về domain knowledge mới?
├── Có → Dữ liệu thay đổi thường xuyên không?
│   ├── Có → RAG
│   └── Không → Đủ >1K high-quality samples không?
│       ├── Có → Fine-tune
│       └── Không → RAG + few-shot prompting
└── Không → Prompt engineering trước, đừng complex hóa
```

### "Tôi có nên build agent không?"
```
Task có thể solve bằng 1 LLM call không?
├── Có → Đừng build agent
└── Không → Task cần multi-step với dynamic tool selection không?
    ├── Có → Latency acceptable với multi-step không?
    │   ├── Có → Human-in-the-loop feasible không?
    │   │   ├── Có → Build agent
    │   │   └── Không → Cần thêm safety layer trước
    │   └── Không → Reconsider approach
    └── Không → Pipeline cố định là đủ
```

### "Data của tôi có sẵn sàng chưa?"
```
Score 0-3 cho mỗi tiêu chí (0 = không có, 3 = production-grade):
[ ] Completeness: Data có đủ không? Score: __
[ ] Accuracy: Data có đúng không? Score: __
[ ] Freshness: Data có mới không? Score: __
[ ] Volume: Đủ samples không? Score: __
[ ] Labels: Đủ labeled data không? (nếu supervised) Score: __

Tổng < 8: Fix data trước, đừng train model
Tổng 8-12: Proceed với expectation thấp, iterate
Tổng > 12: Ready to proceed
```

---

## 19. KẾT NỐI VỚI THỰC TẾ VIỆT NAM

> Framework Western enterprise không apply 1:1 vào context VN. Những điều cần calibrate:

**Talent:** Data engineering mature hơn ML Engineering tại VN → invest data layer trước
**Scale:** Hầu hết doanh nghiệp VN chưa có 100+ data producers → formal data contracts có thể overkill
**Tools:** Cloud adoption đang tăng nhanh, nhưng on-premise vẫn phổ biến → edge/batch inference quan trọng hơn streaming
**Governance:** Quy định AI VN đang hình thành → monitor, nhưng chưa cần GDPR-level compliance cho hầu hết cases
**Culture:** Change management khó hơn ở hierarchical culture → executive buy-in là must-have, không optional

---

## 20. DAILY SESSION CHECKLIST

```
BẮT ĐẦU SESSION:
[ ] Tôi học hôm nay để làm gì cụ thể? (một câu, không phải paragraph)
[ ] Tôi đang ở node nào trong dependency graph?
[ ] Hôm nay tôi sẽ build/làm gì thực sự?

TRONG SESSION:
[ ] Concept này là principle, pattern, hay tool?
[ ] Nó kết nối với node nào tôi đã biết?
[ ] Trade-off là gì?
[ ] Failure mode là gì?

KẾT THÚC SESSION:
[ ] Tôi có thể explain điều này bằng lời của mình không?
[ ] Tôi đã build/apply được gì thực sự?
[ ] Câu hỏi mới nào xuất hiện? (thêm vào section 17)
[ ] Mental model của tôi có thay đổi không? Nếu có, update gì?
```

---

*File này được tạo dựa trên framework kiến trúc kiến thức của bạn, đã được cập nhật với 20 phản biện xây dựng.*
*Version: 1.0 | Ngày tạo: 2026-05 | Review lại sau: 3 tháng hoặc khi framework feels wrong*
*Nếu bạn không còn cần đọc file này → bạn đã internalize thành công. Đó là mục tiêu.*