---
aliases: []
created: 2026-04-27 17:00:28
progress: raw
blueprint: []
impact: 
urgency: 
tags: []
category: []
---
## Xác suất thống kê

### Thống kê & Xác suất

**Mục tiêu:**

- mô tả **dữ liệu** (statistics — tóm tắt, phân tích cái đã quan sát)
- mô tả **sự bất định** (probability — mô hình hoá cái có thể xảy ra).

**Mục đích:**

- Hỗ trợ để **chọn đúng thuật toán** cho từng loại bài toán/dữ liệu
- **hiểu cơ chế tuning**
- **giải thích vai trò của hyperparameter**

**Nguyên nhân:**

- vì gần như mọi quyết định trong ML (loss, regularization, learning rate…) đều có gốc rễ thống kê/xác suất.

**Thành phần:** **Statistics**: phân tích dữ liệu đã quan sát:

- tóm tắt (descriptive)
- suy luận từ mẫu ra tổng thể (inferential)
- kiểm định giả thuyết.

**Probability**: mô hình hoá sự ngẫu nhiên

- định lượng khả năng xảy ra của các sự kiện -> làm cơ sở cho mọi mô hình sinh và mô hình dự đoán.

---

### Suy luận thống kê

**Populations & Sampling**

**Mục tiêu:**

- phân biệt giữa **toàn bộ đối tượng quan tâm** và **tập con quan sát được**
- làm cơ sở để suy luận từ phần ra toàn thể.

**Mục đích:**

- Cho phép rút kết luận về tổng thể lớn (thường không quan sát hết được) chỉ từ một mẫu nhỏ.

**Nguyên nhân:**

- cốt lõi của mọi bài toán ML, vì train set luôn là sample của distribution thật.

**Thành phần:**

- **Population** — toàn bộ tập hợp đối tượng/dữ liệu ta muốn hiểu.
- **Sample** — tập con hữu hạn được lấy từ population để phân tích.
- **Sampling** — quá trình chọn sample sao cho đại diện cho population; chất lượng sampling quyết định kết luận có generalize được hay không.

---

### Các thước đo xu hướng trung tâm

**Mean, Median, Mode & Expected Values** — _Measures of Central Tendency_

**Mục tiêu:**

- tóm tắt phân phối/dữ liệu bằng **một con số đại diện** cho "vị trí trung tâm".

**Mục đích:**

- Trả lời _"giá trị điển hình của dữ liệu là bao nhiêu?"_
- bước đầu tiên để hiểu dữ liệu trước khi phân tích sâu hơn.

**Nguyên nhân:**

- không thể nhìn từng điểm dữ liệu một, cần một đại diện để so sánh và mô tả.

**Thành phần:**

- **Mean** — trung bình cộng. Nhạy với outlier.
- **Median** — giá trị giữa khi sắp xếp. Bền với outlier.
- **Mode** — giá trị xuất hiện nhiều nhất. Dùng cho dữ liệu rời rạc/categorical.
- **Expected Value** — phiên bản lý thuyết của mean: E[X]=∑x⋅P(x)\mathbb{E}[X] = \sum x \cdot P(x) E[X]=∑x⋅P(x) — trung bình theo phân phối, không phải theo mẫu.

---

### Độ phân tán và mối quan hệ

**Variance & Covariance** — _Measures of Dispersion & Dependence_

**Mục tiêu:**

- mô tả **dữ liệu dao động quanh trung tâm thế nào**
- mô tả **các biến liên hệ với nhau ra sao**.

**Mục đích:**

- Định lượng sự bất định và quan hệ tuyến tính
- nền tảng cho chuẩn hoá, regression, PCA.

**Nguyên nhân:**

- chỉ biết "trung bình" là chưa đủ — cần biết dữ liệu trải rộng và liên kết ra sao.

**Thành phần:**

- **Variance** — đo độ phân tán của một biến quanh mean.
- **Covariance** — đo mức đồng biến tuyến tính giữa hai biến.

---

### Cơ sở xác suất

**Random Variables, Common Probability Distributions, Central Limit Theorem** — _Probability Foundations_

**Mục tiêu:**

- chuyển hiện tượng ngẫu nhiên thành đối tượng toán học có thể phân tích.

**Mục đích:**

- Cho phép **mô hình hoá, dự đoán và suy luận** trên dữ liệu có yếu tố bất định.

**Nguyên nhân:**

- dữ liệu thực tế luôn có nhiễu/ngẫu nhiên — cần khung toán học để xử lý.

**Thành phần:**

- **Random Variable** — biến nhận giá trị theo một phân phối xác suất; cầu nối giữa "sự kiện" và "con số".
- **Normal Distribution** — phân phối hình chuông, đặc trưng bởi mean và variance; xuất hiện tự nhiên khắp nơi.
- **Binomial Distribution** — phân phối số lần thành công trong nn n phép thử nhị phân độc lập.
- **Uniform Distribution** — mọi giá trị trong khoảng có xác suất bằng nhau.
- **Central Limit Theorem (CLT)** — trung bình của nhiều mẫu độc lập tiệm cận normal **bất kể phân phối gốc** — lý do normal có mặt khắp thống kê.

---

### Lập luận xác suất theo bằng chứng

**Conditional Probability & Bayes' Theorem** — _Probabilistic Reasoning under Evidence_

**Mục tiêu:**

- **cập nhật niềm tin** về một sự kiện khi biết thêm thông tin.

**Mục đích:**

- Trả lời _"xác suất A thay đổi thế nào khi biết B đã xảy ra?"_
- cốt lõi của inference, classification, decision-making.

**Nguyên nhân:**

- trong thực tế, thông tin đến dần — model phải biết cách tích hợp bằng chứng mới.

**Thành phần:**

- **Conditional Probability** — P(A∣B)P(A|B) P(A∣B): xác suất A xảy ra với điều kiện B đã xảy ra.
- **Bayes' Theorem** — công thức đảo ngược điều kiện: P(A∣B)=P(B∣A)P(A)P(B)P(A|B) = \frac{P(B|A)P(A)}{P(B)} P(A∣B)=P(B)P(B∣A)P(A)​. Cho phép suy nguyên nhân từ bằng chứng quan sát.

---

### Nguyên lý ước lượng tham số

**Maximum Likelihood Estimation (MLE)** — _Parameter Estimation Principle_

**Mục tiêu:**

- chọn tham số θ\theta θ sao cho **xác suất quan sát được dữ liệu thực tế là lớn nhất**: θ^=arg⁡max⁡θP(data∣θ)\hat{\theta} = \arg\max_\theta P(\text{data} \mid \theta) θ^=argmaxθ​P(data∣θ).

**Mục đích:**

- Cung cấp quy tắc **có cơ sở thống kê** để fit model với dữ liệu.

**Nguyên nhân:**

- nền móng của hầu hết loss function trong ML — cross-entropy, MSE đều xuất phát từ MLE dưới các giả định phân phối khác nhau.

---

### Mô hình học có giám sát cơ bản

**Linear & Logistic Regression** — _Supervised Learning Baselines_

**Mục tiêu:**

- ánh xạ input sang output bằng tổ hợp tuyến tính của feature, sau đó (tuỳ loại) đưa qua hàm phi tuyến.

**Mục đích:**

- Làm baseline đơn giản, dễ diễn giải
- viên gạch xây nên các mô hình phức tạp hơn (neural network = chồng nhiều lớp regression phi tuyến).

**Nguyên nhân:**

- trước khi dùng model phức tạp, cần baseline để so sánh và hiểu bản chất bài toán.

**Thành phần:**

- **Linear Regression** — dự đoán giá trị liên tục: y^=w⊤x+b\hat{y} = w^\top x + b y^​=w⊤x+b.
- **Logistic Regression** — dự đoán xác suất phân loại nhị phân: y^=σ(w⊤x+b)\hat{y} = \sigma(w^\top x + b) y^​=σ(w⊤x+b).

---

## Đại số tuyến tính

### Đại số tuyến tính

**Mục tiêu:**

- nghiên cứu **vector, ma trận và phép biến đổi tuyến tính**.

**Mục đích:**

- Cung cấp ngôn ngữ và công cụ để biểu diễn, xử lý dữ liệu đa chiều.

**Nguyên nhân:**

- mọi dữ liệu trong ML/DL đều biểu diễn dưới dạng vector/ma trận/tensor — không có linear algebra thì không làm được deep learning.

---

### Biểu diễn dữ liệu bằng vector

**Scalars, Vectors, Matrices & Tensors** — _Data Representation Objects_

**Mục tiêu:**

- **mã hoá dữ liệu** dưới dạng cấu trúc số nhiều chiều mà máy tính thao tác đồng loạt được.

**Mục đích:**

- Cho phép xử lý dữ liệu lớn bằng phép toán vector hoá
- nền tảng tính toán của toàn bộ ML/DL.

**Nguyên nhân:**

- xử lý từng phần tử quá chậm — phải gom thành cấu trúc đa chiều để tận dụng GPU/SIMD.

**Thành phần:**

- **Scalar** — một số đơn lẻ (0 chiều).
- **Vector** — danh sách số (1 chiều) — biểu diễn 1 sample hoặc 1 feature.
- **Matrix** — lưới số 2 chiều — biểu diễn dataset hoặc phép biến đổi tuyến tính.
- **Tensor** — tổng quát hoá cho nn n chiều — dùng cho ảnh (3D), video (4D), batch trong deep learning.

---

### Tính toán với ma trận

**Matrix Operations, Rank & Linear Independence** — _Linear Algebra Mechanics_

**Mục tiêu:**

- mô tả **cách ma trận biến đổi không gian**
- đo **lượng thông tin độc lập** ma trận chứa.

**Mục đích:**

- Giải hệ phương trình tuyến tính, tối ưu hoá
- phát hiện dữ liệu có dư thừa/suy biến.

**Nguyên nhân:**

- mọi phép biến đổi trong ML (linear layer, projection, transformation) đều quy về phép toán ma trận.

**Thành phần:**

- **Addition/Subtraction** — cộng/trừ từng phần tử tương ứng.
- **Multiplication** — kết hợp hai phép biến đổi tuyến tính thành một.
- **Transpose** — đổi hàng thành cột; cần cho công thức như X⊤XX^\top X X⊤X.
- **Determinant** — số đo "thể tích" ma trận tạo ra; bằng 0 nghĩa là suy biến.
- **Inverse** — phép biến đổi ngược; chỉ tồn tại khi determinant ≠ 0.
- **Rank** — số chiều thực sự độc lập trong ma trận.
- **Linear Independence** — các vector không thể biểu diễn lẫn nhau qua tổ hợp tuyến tính.

---

### Phân tích phổ và giảm chiều

**Eigenvalues, Eigenvectors, Matrix Decompositions, PCA** — _Spectral Analysis & Dimensionality Reduction_

**Mục tiêu:**

- **phân rã ma trận** thành các thành phần cốt lõi để hiểu cấu trúc nội tại của dữ liệu.

**Mục đích:**

- Tìm "trục chính" của dữ liệu, nén dữ liệu, loại nhiễu
- giảm số feature mà vẫn giữ thông tin quan trọng.

**Nguyên nhân:**

- dữ liệu thực tế thường nằm trong không gian nhiều chiều nhưng có cấu trúc thấp chiều ẩn — phân rã giúp lộ ra cấu trúc đó.

**Thành phần:**

- **Eigenvector** — hướng mà ma trận chỉ kéo dãn/co lại, không xoay: Av=λvA v = \lambda v Av=λv.
- **Eigenvalue** (λ\lambda λ) — hệ số kéo dãn dọc theo eigenvector tương ứng.
- **SVD** — phân rã mọi ma trận thành UΣV⊤U\Sigma V^\top UΣV⊤; tổng quát hơn eigendecomposition.
- **PCA** — dùng eigenvectors của covariance matrix để xoay dữ liệu sang trục có variance lớn nhất, giữ lại kk k trục đầu để giảm chiều.

---

## Giải tích

### Giải tích

**Mục tiêu:**

- nghiên cứu **tốc độ thay đổi** và **tích luỹ** của hàm số.

**Mục đích:**

- Hiểu cơ chế **training model** — đặc biệt là gradient descent: làm thế nào điều chỉnh tham số để giảm loss function.

**Nguyên nhân:**

- training = tối ưu hoá; tối ưu hoá cần biết hàm thay đổi ra sao theo tham số — đó chính là calculus.

---

### Giải tích vi phân ứng dụng tối ưu hóa

**Derivatives, Gradients, Vector/Matrix Calculus, Chain Rule** — _Differential Calculus for Optimization_

**Mục tiêu:**

- đo **tốc độ thay đổi** của hàm số theo các biến đầu vào.

**Mục đích:**

- Cho phép **gradient descent** hoạt động — biết hàm loss thay đổi theo tham số ra sao để cập nhật đúng hướng giảm loss.

**Nguyên nhân:**

- không có đạo hàm thì không biết "đi hướng nào để giảm loss" — toàn bộ deep learning sẽ không hoạt động.

**Thành phần:**

- **Derivative** — tốc độ thay đổi của hàm 1 biến.
- **Gradient** — vector các đạo hàm riêng, chỉ hướng tăng nhanh nhất của hàm nhiều biến.
- **Jacobian** — ma trận đạo hàm bậc nhất của hàm vector → vector.
- **Hessian** — ma trận đạo hàm bậc hai; cho biết độ cong (dùng trong second-order optimization).
- **Chain Rule** — quy tắc đạo hàm hàm hợp; **cơ chế cốt lõi của backpropagation** trong neural network.

---

### Phân tích địa hình tối ưu hóa

**Fundamentals of Optimisation** — _Optimization Landscape Analysis_

**Mục tiêu:**

- mô tả **hình dạng của hàm loss** và lý do quá trình huấn luyện hội tụ tốt hay tệ.

**Mục đích:**

- Giải thích _vì sao_ model converge, stuck, hay overfit
- hướng dẫn thiết kế thuật toán/loss tốt hơn.

**Nguyên nhân:**

- deep learning thường non-convex — hiểu địa hình loss giúp chọn optimizer, learning rate, init đúng cách.

**Thành phần:**

- **Local Minimum** — điểm thấp nhất trong vùng lân cận, không phải toàn cục.
- **Global Minimum** — điểm thấp nhất trên toàn miền — đích lý tưởng.
- **Saddle Point** — điểm gradient = 0 nhưng không phải min/max; phổ biến trong không gian nhiều chiều, dễ làm optimizer "kẹt".
- **Convexity** — tính chất "lòng chảo": mọi local min đều là global min. Hàm convex dễ tối ưu; deep learning thường non-convex nên khó hơn.