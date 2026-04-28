

---

## I. Statistics & Probability

### Populations & Sampling
![Populations & Sampling](../Populations%20&%20Sampling.md)
### Mean, Median, Mode & Expected Values
- **Expected Value** là thứ duy nhất matter: mọi loss DL đều viết dạng $\mathbb{E}_{x\sim p}[L(x)]$.
- Median/Mode hiếm khi đụng trong training, nhưng cần khi đọc paper về robust statistics.

### Variance & Covariance
- Variance = chỉ số chính của **mode collapse** (GAN), **vanishing/exploding** (RNN), **representation collapse** (LLM contrastive).
- Covariance matrix → nền tảng của BatchNorm, LayerNorm, whitening.

### Random Variables
- Input, weight, gradient đều là RV. Không hiểu RV → không hiểu nổi noise injection, dropout, stochastic gradient.

### Common Probability Distributions
- **Gaussian (multivariate)**: weight init, latent prior, attention weight analysis.
- **Categorical/Multinomial**: softmax output của classifier và LLM next-token.
- **Uniform**: dropout mask, latent prior cho GAN.
- *Cắt được*: Binomial (gần như không dùng trong DL).

### Central Limit Theorem
- Lý do batch gradient ≈ Gaussian quanh true gradient.
- *Để hiểu, không để dùng* — không tune hyperparam dựa vào CLT.

### Conditional Probability
- **Trung tâm của LLM**: $P(\text{token}_t | \text{token}_{<t})$ — language modeling = conditional probability.
- CWGAN, conditional diffusion, instruction-tuning đều là conditional modeling.

### Bayes' Theorem
- Discriminator = posterior estimator.
- Bayesian DL, calibration, uncertainty estimation cho LLM.

### Maximum Likelihood Estimation (MLE)
- **LLM training = MLE thuần túy** (cross-entropy = negative log-likelihood).
- GAN sinh ra để *thay thế* MLE bằng divergence minimization → biết MLE để hiểu khi nào dùng cái nào.

### Linear & Logistic Regression
- Logistic regression = neuron đơn lẻ + sigmoid. Toàn bộ DL chỉ là stack chúng lên.
- Cross-entropy loss của LLM = generalization của logistic regression sang multi-class.

### Information Theory (BỔ SUNG — list cũ thiếu)
- **Cross-entropy, KL divergence, perplexity**: metric chính của LLM.
- **Mutual information**: nền tảng của contrastive learning, InfoNCE.
- JS divergence, Wasserstein distance: GAN family.

---

## II. Linear Algebra

### Scalars, Vectors, Matrices & Tensors
- Mọi data trong DL là tensor: image $(B,C,H,W)$, text $(B,L,D)$, attention $(B,H,L,L)$.
- Hiểu **broadcasting + reshape semantics** → debug được 80% lỗi shape mismatch.

### Matrix Operations
- Mỗi linear layer là $Wx+b$. Conv = matmul có cấu trúc. **Attention = ba matmul nối tiếp**.
- Transpose, inverse, determinant: ít dùng trực tiếp nhưng cần khi đọc proof.

### Matrix Rank & Linear Independence
- **LoRA (LLM fine-tuning) = low-rank decomposition**. Không hiểu rank → không hiểu LoRA.
- Mode collapse (GAN) = rank của output covariance suy biến.

### Eigenvalues & Eigenvectors
- **Spectral normalization** (GAN), **gradient explosion analysis** (RNN), **attention rank collapse** (Transformer sâu) đều phân tích bằng eigenvalue.
- Lipschitz constant của linear layer = singular value lớn nhất.

### Matrix Decompositions (SVD, QR, Cholesky)
- SVD: nền tảng của LoRA, model compression, low-rank approximation.
- QR/Cholesky: solver trong second-order optimizer (K-FAC, Shampoo).

### Principal Component Analysis (PCA)
- *Cắt khỏi top priority*. Hữu ích để **visualize embedding** (LLM, GAN latent) chứ không phải training tool.

### Norms & Inner Products (BỔ SUNG)
- L1/L2/L∞ norm: weight decay, gradient clipping, attention scaling.
- Cosine similarity: retrieval, embedding evaluation cho LLM.

---

## III. Calculus

### Derivatives & Gradients
- Toàn bộ training = gradient descent. Không có gradient = không có DL.
- Hiểu vì sao gradient có thể vanish (sigmoid, tanh, RNN sâu) hoặc explode (RNN, GAN không có spectral norm).

### Vector/Matrix Calculus (Jacobian, Hessian)
- **Jacobian**: gradient penalty (WGAN-GP), influence functions, Jacobian regularization.
- **Hessian**: second-order optimizer, sharpness-aware minimization (SAM), loss landscape analysis.
- Khi backprop qua một gradient (như GP) → bậc hai → cần `create_graph=True`.

### Chain Rule
- **Backpropagation chính là chain rule**. Không hơn không kém.
- Truncated BPTT (RNN), gradient checkpointing (LLM training) đều là kỹ thuật xoay quanh chain rule.

### Fundamentals of Optimization
- **Local vs global minima**: DL hiếm khi đạt global, nhưng local thường đủ tốt — hiểu vì sao.
- **Saddle points**: phổ biến hơn local minima trong high-dim → adam, momentum sinh ra để thoát saddle.
- **Convexity**: DL loss **không** convex, nhưng nhiều kỹ thuật giả định convex locally.
- **GAN/RLHF là minimax** → không phải minimization, mà tìm saddle point.

### Lipschitz Continuity (BỔ SUNG)
- Ổn định training: WGAN-GP, spectral norm, gradient clipping đều enforce Lipschitz.
- Attention không Lipschitz tự nhiên → lý do cần normalization trong Transformer.

---

## IV. Topic riêng cần thêm cho LLM (ngoài 3 nhóm trên)

### Optimization nâng cao
- **Adam, AdamW, Lion**: hiểu moment estimation (bậc 1, bậc 2).
- **Learning rate schedule**: cosine, warmup — toán đằng sau sao chọn.

### Sequence & Attention math
- **Softmax + temperature**: tại sao chia $\sqrt{d_k}$, vì sao softmax saturate khi logits lớn.
- **Positional encoding**: Fourier features, RoPE — đều là linear algebra trên đường tròn đơn vị.

### Sampling & Decoding
- **Top-k, top-p (nucleus), temperature sampling**: probability theory + tail behavior của distribution.
- **Beam search**: dynamic programming + log-probability.

### RLHF / DPO
- **Policy gradient, KL constraint**: probability + optimization.
- **Bradley-Terry model**: pairwise preference → logistic regression nâng cao.

---

## Priority học theo thứ tự

1. **Tier 1 (must, học trước):** Expected value · Conditional probability · Gradient/Chain rule · Matrix ops · Cross-entropy/KL · Logistic regression · Saddle-point optimization
2. **Tier 2 (đụng paper là cần):** Jacobian/Hessian · Eigenvalue/SVD · Lipschitz · Information theory · MLE
3. **Tier 3 (chuyên sâu):** PCA · CLT · Bayesian DL · Game theory · Kantorovich-Rubinstein duality

---

*Reference khuyên đọc: "Mathematics for Machine Learning" (Deisenroth) cho nền; "Deep Learning" (Goodfellow) Phần I cho góc DL; "The Matrix Cookbook" để tra cứu identity.*
