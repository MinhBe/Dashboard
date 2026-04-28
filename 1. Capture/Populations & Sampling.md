---
aliases: []
created: 2026-04-28 10:39:28
progress: raw
blueprint: []
impact: 
urgency: 
tags: []
category: []
---
## Mục đích
- **Không bao giờ quan sát được toàn bộ population (data distribution)**  
    → mọi thứ bạn tính toán đều dựa trên **sample**
- **Loss trong training chỉ là một estimator (ước lượng)** của loss thật  
    → sai lệch (variance, bias) đến từ cách sampling
- **Mini-batch = sampling**  
    → batch size, shuffle, sampling strategy **trực tiếp ảnh hưởng gradient và hội tụ**
- Trong LLM:
    - **Pretraining**: token sampling từ distribution
    - **RLHF**: dùng **importance sampling** để hiệu chỉnh phân phối  
        → bản chất đều là **ước lượng kỳ vọng**
- Hiểu sai sampling  
    → hiểu sai vì sao:
    - batch size thay đổi kết quả
    - temperature làm output khác
    - model “unstable” hoặc “biased”

## Khái niệm cơ bản

**Population (tổng thể):** toàn bộ đối tượng trong phạm vi nghiên cứu. Các đặc trưng đo được trên tổng thể gọi là **parameter**.

**Sample (mẫu):** tập con của population được lựa chọn để khảo sát. Các đặc trưng đo được trên mẫu gọi là **statistic**.

Mục đích của thống kê suy diễn là sử dụng _statistic_ để ước lượng _parameter_.

---

## 1. Population

### 1.1. Định nghĩa

Tập hợp toàn bộ đơn vị quan sát thuộc phạm vi nghiên cứu.

### 1.2. Hạn chế thực tiễn

- Khó xác định đầy đủ ranh giới tổng thể.
- Việc thu thập toàn bộ dữ liệu thường bất khả thi do giới hạn về thời gian và chi phí.
- Dẫn tới yêu cầu sử dụng phương pháp lấy mẫu.

---

## 2. Sampling

### 2.1. Định nghĩa

Quá trình lựa chọn một tập con từ population nhằm suy diễn các đặc trưng của tổng thể.

### 2.2. Yêu cầu của một mẫu tốt

**Tính ngẫu nhiên (randomness):** mỗi cá thể trong tổng thể có xác suất được chọn xác định và bằng nhau.

**Tính đại diện (representativeness):** cấu trúc của mẫu phản ánh đúng cấu trúc của tổng thể.

---

## 3. Probability Sampling

### 3.1. Đặc điểm chung

- Lựa chọn dựa trên cơ chế ngẫu nhiên.
- Cho phép suy rộng kết quả ra tổng thể (generalization).
- Phù hợp với nghiên cứu định lượng (quantitative research).
- Yêu cầu danh sách tổng thể đầy đủ — đây là rào cản chính trong thực tế.

### 3.2. Simple Random Sampling

**Quy trình:** liệt kê toàn bộ population, gán định danh, lựa chọn ngẫu nhiên _k_ phần tử bằng công cụ thống kê.

**Ưu điểm:** thủ tục đơn giản, hạn chế thiên lệch chủ quan, khả năng suy rộng cao.

**Nhược điểm:** dễ bỏ sót các nhóm thiểu số; phụ thuộc vào danh sách tổng thể đầy đủ.

**Điều kiện áp dụng:** tổng thể tương đối đồng nhất và có khung mẫu (sampling frame) khả dụng.

### 3.3. Stratified Sampling

**Quy trình:** phân chia population thành các tầng (strata) theo tiêu chí định trước, sau đó lấy mẫu ngẫu nhiên trong mỗi tầng theo tỷ lệ hoặc cân bằng.

**Ưu điểm:** đảm bảo sự hiện diện của tất cả các nhóm; thuận lợi cho phân tích so sánh giữa các nhóm.

**Nhược điểm:** quy trình phức tạp; đòi hỏi hiểu biết về cấu trúc tổng thể.

**Điều kiện áp dụng:** tổng thể có tính đa dạng cao và nghiên cứu hướng tới phân tích theo subgroup.

### 3.4. Cluster Sampling

**Quy trình:** phân chia tổng thể thành các cụm (cluster) theo đơn vị địa lý hoặc tổ chức, lựa chọn ngẫu nhiên một số cụm, sau đó khảo sát toàn bộ hoặc một phần các đơn vị trong cụm được chọn.

**Ưu điểm:** tiết kiệm chi phí; thuận lợi triển khai trên phạm vi rộng.

**Nhược điểm:** sai số ước lượng cao hơn so với simple random sampling; rủi ro thiên lệch theo đặc điểm cụm.

**Điều kiện áp dụng:** tổng thể phân tán về mặt địa lý; khó tiếp cận từng cá thể.

---

## 4. Non-Probability Sampling

### 4.1. Đặc điểm chung

- Lựa chọn không dựa trên cơ chế ngẫu nhiên.
- Phù hợp với nghiên cứu định tính (qualitative research).
- Tiết kiệm thời gian và chi phí.
- Hạn chế chính: thiên lệch (bias) cao và khả năng suy rộng thấp.

### 4.2. Purposive Sampling

**Quy trình:** xác định tiêu chí lựa chọn (chuyên gia, đối tượng đặc thù…) và chủ động chọn các cá thể phù hợp.

**Ưu điểm:** thu được dữ liệu chuyên sâu, đúng đối tượng cần khảo sát.

**Nhược điểm:** mức độ thiên lệch cao; không thể suy rộng.

**Điều kiện áp dụng:** nghiên cứu định tính cần hiểu sâu một hiện tượng hoặc nhóm đặc thù.

### 4.3. Convenience Sampling

**Quy trình:** lựa chọn các đối tượng dễ tiếp cận nhất đối với người nghiên cứu.

**Ưu điểm:** nhanh, chi phí thấp.

**Nhược điểm:** thiên lệch rất cao; không đảm bảo tính đại diện.

**Điều kiện áp dụng:** nghiên cứu sơ bộ, thử nghiệm công cụ, hoặc khi nguồn lực hạn chế.

### 4.4. Snowball Sampling

**Quy trình:** bắt đầu từ một số đối tượng ban đầu, sau đó mở rộng mẫu thông qua giới thiệu từ chính các đối tượng này.

**Ưu điểm:** tiếp cận được các nhóm khó xác định hoặc khó tiếp cận trực tiếp.

**Nhược điểm:** thiên lệch theo mạng lưới quan hệ; tính đại diện thấp.

**Điều kiện áp dụng:** nghiên cứu trên các nhóm ẩn hoặc các chủ đề nhạy cảm.

---

## 5. Nguyên tắc chung

- Lựa chọn phương pháp lấy mẫu phải đi kèm với **luận cứ khoa học** rõ ràng.
- Mục tiêu cốt lõi: tối đa hóa tính đại diện và nhận diện đầy đủ các nguồn thiên lệch.
- Trong nghiên cứu định tính, có thể lựa chọn một case điển hình để phân tích chuyên sâu, hoặc nhiều case để so sánh — nhưng tiêu chí lựa chọn phải được biện luận minh bạch.