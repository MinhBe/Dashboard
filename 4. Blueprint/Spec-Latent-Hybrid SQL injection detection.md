---
aliases: []
created: 2026-04-29 09:57:01
progress: raw
blueprint: []
impact: 
urgency: 
tags: []
category: []
---
**Mục tiêu nghiên cứu:** Kiểm chứng thực nghiệm liệu các phương pháp sinh đơn giản có cạnh tranh được với mô hình deep generative phức tạp (VAE-GAN) trên bài toán sinh chuỗi rời rạc có ràng buộc cao — với SQL Injection là domain cụ thể để đo lường.

**Core Claim:** Khi *Constraint Density* δ\delta δ của domain cao, baseline có cấu trúc (n-gram LM + mutation) đạt WAF Evasion Rate tương đương hoặc cạnh tranh với VAE-GAN, với chi phí tính toán thấp hơn đáng kể.

---

### 🟩 Giai đoạn 1: Xác định Bài toán & Thu thập Dữ liệu

_Mục tiêu: Xây dựng nền tảng dữ liệu đủ chất lượng và định nghĩa chính xác không gian bài toán trước khi thiết kế kiến trúc._

- **Định nghĩa bài toán hình thức (Constrained Discrete Sequence Generation):**
    - Bài toán được cast là: sinh chuỗi token s∈Ss \in \mathcal{S} s∈S thỏa mãn tập ràng buộc cứng C\mathcal{C} C (cú pháp SQL hợp lệ) và tối đa hóa objective f(s)f(s) f(s) (WAF evasion rate).
    - Phân biệt rõ: đây là **generation under hard constraint**, không phải open-ended text generation.
- **Định nghĩa và đo Constraint Density δ\delta δ:**
    - δ(C,V)\delta(\mathcal{C}, \mathcal{V}) δ(C,V) = tỉ lệ vị trí token trong chuỗi phải conform to hard grammar constraint, normalized theo vocabulary size.
    - Tính δ\delta δ cho corpus SQLi và so sánh với một domain có δ\delta δ thấp (ví dụ: news headline) để establish rằng SQLi là high-constraint domain — đây là tiền đề của toàn bộ paper.
    - *Acceptance criteria:* δ\delta δ phải đo được reproducibly trên tập held-out; variance giữa các run < 5%.
- **Thu thập dữ liệu hai tầng:**
    - _Tầng 1 — Generation corpus:_ ~50k SQLi payload từ nguồn công khai (SQLMap test suite, PayloadsAllTheThings, SecLists). Gán nhãn attack type: `union_based`, `blind_boolean`, `blind_time`, `error_based`, `stacked_queries`.
    - _Tầng 2 — SQL sạch:_ ~50k câu SQL hợp lệ từ query log ứng dụng mã nguồn mở. Discriminator cần học phân biệt payload độc hại với SQL hợp lệ thông thường, không chỉ phân biệt SQL với chuỗi vô nghĩa.
    - _Acceptance criteria:_ Inter-annotator agreement trên attack type labels ≥ 0.80 (Cohen's kappa). Dataset reproducible qua Docker container.
- **Xây dựng Vocabulary V\mathcal{V} V:**
    - Trích xuất toàn bộ SQL keywords, operators, ký tự đặc biệt, và known bypass patterns (comment sequences, encoding variants).
    - Tính entropy của corpus để đánh giá độ đa dạng ban đầu — nếu entropy quá thấp, corpus bị dominated bởi một vài template và cần bổ sung.

---

### 🟨 Giai đoạn 2: Tiền xử lý & Feature Engineering

_Mục tiêu: Chuyển dữ liệu về dạng tensor mà không mất thông tin cấu trúc ngữ nghĩa quan trọng cho bài toán evasion._

- **SQL-Aware Tokenization:**
    - Dùng regex-based tokenizer nhận biết các token nhạy cảm: `'`, `--`, `/**/`, `UNION`, `SELECT`, `SLEEP()`, encoding sequences (`%27`, `&#39;`).
    - _Không dùng_ whitespace tokenization đơn thuần — sẽ tách sai các multi-character operators.
    - _Không dùng_ BPE hay WordPiece mặc định — chúng được train trên natural language và sẽ phân tách sai SQL keywords. Nếu dùng subword tokenization, phải train from scratch trên SQL corpus.
- **Partial De-lexicalization (không anonymize hoàn toàn):**
    - Thay thế tên bảng/cột cụ thể bằng `<TABLE>`, `<COL>`, số literal bằng `<NUM>`.
    - _Giữ nguyên_ các keyword tấn công (`UNION`, `SLEEP`, `BENCHMARK`) và ký tự đặc biệt — đây là tín hiệu quan trọng mà encoder phải học, không phải nhiễu cần loại bỏ.
    - _Lý do kỹ thuật:_ Anonymize hoàn toàn sẽ làm mất thông tin phân biệt giữa các attack type, dẫn đến latent space không có cấu trúc.
- **Xác định độ dài chuỗi tối đa LL L:**
    - Vẽ phân phối độ dài corpus, chọn LL L = percentile 95 để tránh truncation quá nhiều.
    - Dùng `<PAD>` và `<EOS>` theo convention chuẩn. Padding mask phải được pass vào encoder để tránh attend vào padding tokens.
- **EDA — Phân tích cấu trúc corpus:**
    - Cluster corpus theo attack type, tính pairwise cosine similarity giữa các cluster để xác định "modes" trong dữ liệu.
    - Nếu các cluster overlap nhiều → corpus thiếu diversity, cần augmentation trước khi train.

---

### 🟧 Giai đoạn 3: Thiết kế Kiến trúc Hybrid VAE-GAN

_Mục tiêu: Thiết kế kiến trúc giải quyết đúng bài toán discrete sequence generation — không phải copy kiến trúc từ image generation._

- **Giải quyết vấn đề cốt lõi: Discrete Sampling không differentiable:**
    - Bước `argmax` khi decode token từ distribution không có gradient. Phải chọn một trong hai hướng trước khi code bất cứ thứ gì:
    - *Hướng A — Gumbel-Softmax Relaxation:* Thay `argmax` bằng Gumbel-Softmax với temperature τ\tau τ, lập lịch giảm τ\tau τ từ 1.0 xuống 0.1 trong quá trình training. Gradient flow được nhưng output ở giai đoạn đầu là "soft tokens", không phải discrete.
    - _Hướng B — REINFORCE / Policy Gradient:_ Coi decoder là policy, dùng reward từ Discriminator làm training signal. Gradient flow qua sampling được nhưng high-variance — cần baseline variance reduction.
    - _Quyết định:_ Chọn Gumbel-Softmax cho giai đoạn đầu vì ổn định hơn. Ghi chú rõ trong paper đây là design choice với trade-off.
- **Encoder EE E:**
    - Nén câu SQL thực tế thành phân phối q(z∣x)=N(μ,σ2)q(z|x) = \mathcal{N}(\mu, \sigma^2) q(z∣x)=N(μ,σ2) trong latent space R256\mathbb{R}^{256} R256.
    - Dùng Transformer encoder (không phải LSTM) để capture long-range dependency giữa các token SQL.
    - _Lưu ý:_ Encoder phải nhận padding mask, không attend vào `<PAD>` tokens.
- **Generator/Decoder GG G:**
    - Giải mã vector ẩn zz z thành chuỗi token SQL autoregressively.
    - Dùng Transformer decoder với cross-attention vào zz z.
- **Discriminator DD D:**
    - Dùng 1D-CNN với nhiều kích thước filter (3, 4, 5 tokens) để bắt n-gram patterns đặc trưng của attack payload.
    - **Feature Matching:** Lấy output từ layer **trước penultimate** (không phải layer cuối) để tính feature matching loss. Layer quá cuối → generator học copy surface statistics. Layer quá đầu → signal quá yếu. Cụ thể: layer L−2L-2 L−2 của CNN stack.
- **Hybrid Loss với trọng số tường minh:**
    - L=Lrecon+β⋅LKL+λ⋅Ladv+γ⋅Lfm\mathcal{L} = \mathcal{L}_{recon} + \beta \cdot \mathcal{L}_{KL} + \lambda \cdot \mathcal{L}_{adv} + \gamma \cdot \mathcal{L}_{fm} L=Lrecon​+β⋅LKL​+λ⋅Ladv​+γ⋅Lfm​
    - Khởi đầu: β=1.0\beta = 1.0 β=1.0, λ=0.1\lambda = 0.1 λ=0.1, γ=10.0\gamma = 10.0 γ=10.0 — adversarial loss scale nhỏ ban đầu để tránh destabilize VAE.
    - Dùng **KL annealing** (tăng β\beta β từ 0 lên 1 trong 10k steps đầu) để tránh KL collapse — vấn đề nổi tiếng nhất của VAE trên text, hoàn toàn không đề cập trong spec gốc.
    - Dùng **free bits** (λfb=2\lambda_{fb} = 2 λfb​=2 nats per dimension) như backstop phòng posterior collapse.

---

### 🟥 Giai đoạn 4: Huấn luyện & Giám sát Ổn định

_Mục tiêu: Train đến hội tụ ổn định mà không bị mode collapse hay posterior collapse — hai failure mode chính của VAE-GAN trên discrete data._

- **Warm-up Phase (VAE only, không có Discriminator):**
    - Train encoder-decoder như VAE thuần túy cho đến khi: reconstruction accuracy ≥ 70% trên held-out set **VÀ** KL divergence nằm trong khoảng [5, 50] nats.
    - *Đây là acceptance criteria cụ thể* — không phải "train cho đến khi ổn định" chung chung. Nếu KL → 0: posterior collapse đang xảy ra, tăng λfb\lambda_{fb} λfb​. Nếu reconstruction < 50% sau 20k steps: learning rate hoặc architecture cần review.
- **Adversarial Training Phase:**
    - Thêm Discriminator sau khi VAE đã qua warm-up gate.
    - Tỉ lệ training $D:G = 5:1$ (train D 5 lần cho mỗi lần train G).
    - Dùng **WGAN-GP** (Gradient Penalty) thay vì vanilla GAN loss để đảm bảo Lipschitz continuity của D, tránh exploding gradient.
    - Monitor gradient norm của G liên tục — nếu gradient norm của G đột ngột tăng > 10x: dừng, kiểm tra balance giữa λ\lambda λ và γ\gamma γ.
- **Phát hiện và xử lý Mode Collapse:**
    - Sau mỗi 1000 steps, sample 500 sequences, tính pairwise edit distance. Nếu median edit distance < 5 tokens: mode collapse đang xảy ra.
    - Xử lý: tăng dropout trong G (0.1 → 0.3), thêm noise vào latent vector zz z khi train G.
- **Temperature Schedule (Gumbel-Softmax):**
    - τ\tau τ: 1.0 → 0.1, giảm theo exponential decay mỗi 5000 steps. Không giảm quá nhanh — nếu τ\tau τ < 0.3 quá sớm, gradient sẽ bão hòa.

---

### 🟦 Giai đoạn 5: Đánh giá Thực nghiệm

_Mục tiêu: Đo lường định lượng để trả lời core claim của paper — không phải đánh giá định tính._

- **Primary Metric — WAF Evasion Rate (WER):**
    - Sinh 1000 payload từ mỗi method, chạy qua 3 WAF targets: ModSecurity CRS default, ModSecurity CRS paranoia level 3, Cloudflare-equivalent ruleset.
    - WER = (số payload bypass WAF VÀ syntactically valid) / 1000.
    - _Đây là metric duy nhất map trực tiếp vào claim._ Mọi metric khác là secondary.
- **Secondary Metrics (để explain tại sao WER cao hay thấp):**
    - _Syntax Validity Rate:_ Parse bằng `sqlparse`. Ngưỡng tối thiểu ≥ 85% — nếu model không đạt ngưỡng này, WER vô nghĩa vì payload invalid không thể execute.
    - _Structural Diversity:_ Phân phối pairwise edit distance — cần report cả mean lẫn variance, không chỉ một số.
    - *Constraint Density δ\delta δ:* Đo trên output của mỗi method để kiểm tra model có học được cấu trúc SQL hay không.
- **Experiment 1 — Main Comparison:**
    - So sánh WER của tất cả methods: KN-5 + Mutation (baseline đề xuất), Template + Random Fill (baseline hiện có), LSTM LM, VAE, VAE-GAN.
    - _Statistical significance:_ Dùng bootstrap resampling (n=10,000) để tính confidence interval cho WER. Không claim "tốt hơn" nếu CI overlap.
- **Experiment 2 — δ\delta δ Correlation:**
    - Tạo synthetic CDSG domains với δ\delta δ khác nhau (từ 0.1 đến 0.9) bằng cách vary grammar strictness.
    - Plot δ\delta δ vs WER gap (baseline WER − best deep model WER). *Expected finding:* gap tiến về 0 khi δ\delta δ tăng.
    - Đây là experiment quan trọng nhất để argue claim có tính **generalizability** vượt ra ngoài SQLi.
- **Experiment 3 — Sample Efficiency:**
    - Train tất cả methods trên {1k, 5k, 10k, 50k} samples. Plot learning curve (WER vs. training size).
    - _Expected finding:_ Baseline converges với < 5k samples; deep models cần > 10k để competitive.
- **KHÔNG dùng Latent Space Walk như metric chính:**
    - Latent interpolation là visualization định tính, không thể dùng để so sánh models hay track improvement. Có thể dùng như supplementary material để visualize latent structure, không phải evidence cho claim.

---

### 🟪 Giai đoạn 6: Đóng gói Thực nghiệm & Tái hiện

_Mục tiêu: Đảm bảo toàn bộ thực nghiệm reproducible — tiêu chuẩn bắt buộc của academic publication._

- **Reproducibility Package:**
    - Toàn bộ experiments chạy được qua một lệnh duy nhất từ Docker image.
    - Seed cố định cho tất cả random operations. Report kết quả dưới dạng mean ± std trên ít nhất 3 random seeds.
    - WAF evaluation environment được containerize — không phụ thuộc vào external production systems.
- **Benchmark Suite (đóng gói để community dùng):**
    - Dataset + evaluation script + WAF Docker setup được release dưới license rõ ràng.
    - Leaderboard format: mỗi entry cần report WER trên cả 3 WAF targets, Syntax Validity Rate, và Structural Diversity.
    - Đây biến paper từ "analysis của một model" thành "benchmark cho cả field" — tăng citation impact đáng kể.
- **API Service (phạm vi hạn chế — research only):**
    - Flask/FastAPI nhận seed và attack type label, trả về danh sách payload.
    - _Không phải_ production deployment. Access control: token-based, chỉ dành cho verified researchers.
    - Latency target: < 500ms cho batch 100 payload. Throughput: không phải priority cho research tool.
    - _Failure mode:_ Nếu model chưa converge (syntax validity < 85%), API trả về error thay vì payload invalid.

---

### 🔗 Mapping Toán học → Thực nghiệm

|Khái niệm|Vai trò trong paper|
|---|---|
|Constraint Density δ\delta δ|Independent variable trong Exp 2 — predict khi nào baseline wins|
|KL Divergence|Monitor metric trong training — detect posterior collapse|
|Gumbel-Softmax / REINFORCE|Giải pháp cho non-differentiable sampling — phải chọn và justify|
|WGAN-GP (Lipschitz)|Stabilize adversarial training — không phải optional|
|Bootstrap CI|Statistical rigor cho WER comparison — không claim significance nếu CI overlap|
|KL Annealing + Free Bits|Prevent posterior collapse — thiếu trong spec gốc, bổ sung bắt buộc|