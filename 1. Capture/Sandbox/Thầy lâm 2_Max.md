### [MAX] Transcript: Unknown Video
- **Ngày:** 13/05/2026
- **Thời lượng:** 765s
- **Ngôn ngữ:** vi

---

#### Speaker Diarization & Confidence Tagging


**Nhân vật 1** [00:00 - 00:06]
> Datasect của em thì em lấy ở trên Kaggle với cả một số dataset về HTML cơ bản
> trong đó sẽ có một số cái liên quan tới OWAP
> Em lại đã truyền mất rồi nè
> Có 1 cái file...
> CSV hả?
> À, có
> Nghĩa là đây ạ
> Vâng vâng
> Thì đầu tiên là 2 trường đầu chắc cũng cơ bản đấy
> Trường đầu thì chỉ là ID ạ
> Còn trường tiếp theo sẽ là cái Dataset của em ạ
> Thì nó sẽ là Dataset đó
> Vâng, vâng
> Back payload ạ
> Tiếp theo là ở cái này ạ
> Bởi vì ở đây
> Nó sẽ cố gắng target vào một tăng nhân
> Sẽ có 1 nạn nhân
> Ở đấy nạn nhân thì có thể thay đổi cho thời gian
> Nhưng mà cấu trúc vẫn như thế
> Nên ở đây em đã có thay đổi
> Và em sẽ thêm vào
> Là ví dụ như là
> Tấn công chờ độ chẳng hạn
> nghĩa là người ta sẽ thử xem là mô hình nó sẽ phản được thế nào với câu lệnh
> thì ở đây người ta cố gắng điền lên thông tin về thời gian để xem là phản hồi như thế nào
> thì đem sẽ chuyển tất cả các thông số
> thì trở thể chuyển về dạng kiểu ghi dạng chữ đấy ạ
> Để tránh...
> Dạng má hoá của nó
> À vâng, dạng má hoá của nó
> Giải định tiếp theo
> Tiếp theo là dạng tấn công
> Vậy nhãn cái gì?
> Vâng ạ, nhãn tấn công
> Tiếp theo là tấn công vào cơ sở rượu nào
> Và cuối cùng là Confident
> Thì ở đây so với lần trước
> thì là em đánh nó hơi theo chủ quan
> nên lần này sau khi em đánh nhãn xong
> em sẽ đưa vào trong các mô hình học máy
> để em cho nó đánh lại
> và em sẽ có một bộ set
> Cái này là em thêm chứ không phải dựa gốc của nó đi
> Dạ, thế em xin phép ạ
> nghĩa là ở đây em có 2-3 sets
> cái này là em tự đánh bằng tay
> Ở đây thì em sẽ có 1 phần nữa
> thường reason là giải thích nguyên nhân
> nghĩa là em sẽ sửa chạy 1 script
> em đảm bảo là hạn chế dùng AI nhất có thể
> thì ở đây sau khi cái script thì nó sẽ tính toán xem là tỷ lệ bao nhiêu phần trăm
> là khả năng kiểu tấn công ở đây ạ
> reason là em, hồi trước em chỉ dùng thuần script thôi ạ
> nhưng mà bởi vì là em confident em đánh nó mở rộng quá
> và số lượng, bao nhiêu bản ghi, tỷ lệnh cấp nhãn như thế nào
> Vấn đề của em mất thân bán
> Chỉ 1 bộ này hay quá nhiều bộ
> Em đã cắt xuống rồi ạ
> Bây giờ em đảm bảo tất cả các bộ nó đều...
> Vâng chỉ một thôi
> Không nghĩa là em lấy từ khoảng 6 bộ
> Sau đó em sẽ x
> Những cái nào mà không rõ ràng thì em bỏ qua luôn
> Em phải nêu hết, em lấy từ xóa bộ về đưa vào 1 mẫu thôi
> Xóa bộ để lấy cả cái nguồn ở đâu chỉ cần hết nhé
> Có
> Thì em có trong dataset
> Chỉ có dataset tấn công thì có 17.821 mẫu
> Chỉ có tấn công sẽ không có
> Của người dùng
> Hiện tại là em đang nghiên cứu sử dụng sequence gan
> Như vậy của mình đây chỉ là tấn công
> Không đi vào hình ảnh cũng thế
> Mục tiêu của em ạ, đầu tiên là em sẽ chỉ tạo ra mạng tấn công
> Còn những cái mã của người dùng là em sẽ để vào thằng phản biện
> Thằng Dishminate để nó nhận diện
> Em sẽ tách hẳn ra
> Có 2 cái ạ. Đầu tiên là nhận diện có phải mạng tấn công không ạ
> Tiếp theo là em sẽ đưa hẳn cái mã này vào trong tường lửa
> Tường lửa mã nguồn mở
> sẽ nhận luôn cả cái grant gì
> Vâng ạ, nhưng mà nếu như nó vượt qua được tương lựa
> nghĩa là tấn công được
> Nó vượt qua được cái này tấn công hay không tấn công đấy
> Vâng ạ
> Xong khi vào thì cũng có thể tấn công gì
> Vâng ạ
> Ở đây có là cái mẫu của em ạ
> Cái đầu của đầu tiên là cái mẫu cũ của em
> Thì em mới làm nên là nó chưa được chỉ thu
> Thì đến bây giờ thì đến cột ngoài cùng
> Bây giờ em đã có là reward
> Là có cả tương lựa thực tế
> và có cả cái một số nhận định như là kiểu có phải mã SQL không
> Cái này là em cố gắng làm thật nhiều cái reward để tránh việc mô hình bị collab
> bởi vì hiện tại em vẫn bị collab bởi vì nó đang trở về 1
> So sánh với các mô hình ra từ đó, thầy hỏi mô hình gan nó nằm ở đâu?
> Em chỉ cần so sánh CityGan thôi đúng không?
> Vâng
> Chỉ cần so sánh CityGan thôi
> Ờ...em xin phát biểu ạ
> Nghĩa là mô hình Gan
> Nó khả năng nhận diện môn ngữ chữ rất là kém
> Bởi vì nó không đọc được cái gradient
> Khi mà em vào trong mô hình này
> Nó chỉ trả về phân phối về tech thôi ạ
> Nên là em không thể đưa mô hình ra
> Mô hình duy nhất mà có thể nhận được
> Là CTGAN
> Vì là
> Nó là CTGAN
> Với cả một mô hình nữa
> Là WasterGAN GP
> Thì hai cái mô hình đấy
> Nó sẽ biến cái phân phối của em
> thành một cái dạng để có thể nhận chuyển về dạng gradient lúc đấy mới tiếp tục làm được kiếp
> thế nên em mới hiểu được biến nổi
> Chúng chứng ở đây là có yêu cầu cả
> Nghĩa khói ngăn tốt, làm lót như thế nào rồi này
> Tại sao mô hình si quần gan cũ này
> Mô hình si quần gan cũ là em không đưa vào trong từng thực tế
> nên là em không làm quá sâu
> Em có cái sơ đồ lửa nào mà hả?
> Đây ạ, theo em hiểu thì...
> À không đây là cấu trúc mà khi mà em làm
> Mô hình cũ là em không có phần tường lửa
> Nên nó bị collab rất nhanh
> Khoảng chắc 1000 mùi
> Đây là tường lửa gì?
> Đúng rồi ạ
> Còn đây là G này
> Vâng ạ
> Đây là D này
> Và em có tương tác với tường lửa
> Tường lửa dùng để biệt xíu liệu
> Vâng
> Tường lửa là em cố gắng để mô hình không collab nhanh quá
> Không
> Tường lửa em dùng để cán nhãn cho cái xíu liệu này
> Vâng
> Đúng chưa
> Đúng không ạ?
> Xong dùng cái dữ liệu đấy để huấn luyện cái thằng...
> Em mới chỉ là, tương lai em mới dùng để reward cho thằng Generate thôi thưa thầy
> Không phải reward mà nó dùng để cắn nhắc ấy
> Vâng, em mới chỉ làm đến bước đó
> Ừ
> Nhưng mà em cần hướng điểm này
> Cho nên em phải huấn luyện cả dữ liệu CNB ở trong này
> Lẫn với dữ liệu gốc đúng không
> Em được thấy hiện tại là
> Em đang bị collab quá nặng
> Nên em đang phải cắt cái đấy ra
> Em đang sợ là nếu mà thằng D mà nó giỏi quá thì không tiếp tục sẽ phải có ra điền penalty
> Cái đấy chỉ cần tiến khắc phục thêm thôi
> Từ cái nào làm rõ mô hình nhé
> Cái solo này em phải làm rõ mối quan hệ của 3 ông này
> Được chưa?
> Đây là cái mô hình đề xuất của em đúng không?
> Vâng
> Thế thì thành muốn nói thế này
> Mối quan hệ của 3 ông hay là
> Rõ ràng với mối quan hệ này thì 2 con này xin lấu với nhau
> Ông này càng sinh ra thằng TV
> Ông này càng muốn được phát hiện vào TV đấy
> Đúng chứ
> Thì thêm cái thằng LV này vào để làm gì?
> LV này vào để hỗ trợ phân biệt các dữ liệu của mình
> Là tăng khả năng nhận của thầy
> Nhưng mà, dữ liệu sau khi đã được gắn nhận đấy
> thì nó lại đem vào đây cho thầy thông minh hơn
> Thông minh hơn để thầy thay cũng phải sỏi hơn
> Đúng không? Em sẽ suy nghĩ thêm cho nó nhé
> Không hiểu ý của thầy chưa?
> Nếu là lý tiết em có hiểu ý
> nhưng do ngôi hình đang bị lỗi vần nào đó
> nên là G đang không thắng nổi
> bao giờ anh vẽ được sơ đồ, mối quan hệ
> đến nay sơ đồ này chưa có bất kỳ cái mối quan hệ này
> 3 khối đại trả có thể liên quan đến nhau
> nó đã sơ đồ thì nó phải có được kết nối
> kết nối như thế nào
> coi lại cái...
> Chỉ là em đánh ngã lời thôi
> vì là em muốn nói
> là em sẽ chuyển các cái thông tin người dùng
> hành giác dạng
> Rồi
> Cái thích rõ
> còn kiến trúc mô hình
> Vâng đây là kiến trúc UG
> về phần đằng sau thì em chưa nắm vững về mặt lý thuyết lắm ạ
> vì là em đang cố gắng để G nó vượt qua D
> cho anh chị ơi thầy là em đang hơi màu cua đáy bể
> thầy chấm trước ạ
> có thể sao em thay lấy STM bằng 3LSTM
> cái môi nó mạnh hơn nữa
> như thế này được hả ạ
> 3LSTM, BBI
> đấy là phải xong thôi
> chiếc bắt mình kinh này đã
> thì này là đến phần vịt tương lửa của em ạ
> trong đó sẽ có 2 phần ạ
> 1 phần là xem kiến trúc xem có phải SQL không ạ
> còn bên dưới là em sẽ đưa thẳng vào trong database để xem có vượt qua được không ạ
> và nếu mà không vượt qua thì loại hơn bộ diệu này chứ
> không vượt qua
> đấy, nó nên failup gì vậy
> vâng đúng ạ
> không nghe em chỉ reward là điểm
> vâng, em chỉ đánh những điệp thấp để nó tự động hủy thôi
> còn nếu mà em đang hiểu là loại cái đấy ra khỏi database
> thì em chỉ đánh những điệp thấp thôi thưa thầy
> để nó tự động chủ động là nó không học lắm
> rồi em dùng từ này chúng ta không thấy gì hiểu
> hủy hay hay là tức
> nữa là loại nguồn gì thế
> đây là phần em nói ký ơn vào phần bên dưới
> là em sẽ dùng những cái gì
> vì đây là em sử dụng tương lượng thông dụng
> đây là mã nguồn mở
> sẽ kết hợp với những cái rule về tương lửa cơ bản để đưa vào cục chúc tương lửa của em
> Còn cái này là đề xuất rồi ạ
> Thì là...
> Em dùng cái WGAN nhé
> Vâng, Waterson GAN Gradient Penalty
> Vâng, em đang sử dụng thế đơn thầy
> Bởi vì nó đang có cái Gradient Penalty ấy
> Nó đang tránh
> Đang quá thằng
> Disqlimate xuống một tí
> Đây cũng là phương án em đang mò mẫm một tí
> Bây giờ em quay lại cái này
> Đây đây
> Dạ vâng
> Nếu không qua một cổng này
> Thấy máy thế mà em chỉ để dùng cái reward thôi đúng không?
> Vâng, em chỉ reward điểm thấp thôi đưa thầy
> Để nó tự động
> Điểm đấy sẽ được dùng ở đâu?
> Reward ấy sẽ được dùng ở đâu?
> Reward thì là
> Cái này là hỗ trợ thằng Generator vậy ạ
> Em không kết nối với thằng Dixing in Net
> Ủa nhưng hỗ trợ như thế nào
> Thì...
> Tôi hiểu câu hỏi
> Thì em đang theo gọi
> Em nói ra
> Dùng cái này để hỗ trợ thằng Generator đúng không?
> Đúng rồi ạ
> Thầy hỏi là hỗ trợ như thế nào?
> Thầy chưa hiểu được hỗ trợ như thế nào
> Cách em làm như thế nào
> Dạ sau khi mà đưa cái mô hình
> Em dựng một cái tượng lửa
> Sau khi mà tạo ra xong
> Em sẽ đưa thẳng cái câu lệnh mới
> Tạo ra, đưa thẳng vào trong tượng lửa
> Và nó sẽ trả về điểm quen hược lại
> Trần Generator
> Đúng, cái điểm quen hược lại
> Điểm đấy được cậu ở đâu
> Mình hiểu ý thầy không
> Vậy thì thầy cho em
> Thầy là tượng lửa
> Thầy cho em 5 điểm
> 5 điểm đấy em dùng phần gì
> Bây giờ mình cho thầy một cái quay lộn
> Thầy đánh giá xong, thấy hay
> Cho em 5 điểm
> 5 điểm để dùng làm gì?
> Thầy cho em không điểm
> Thầy cho em 10 điểm
> Và cái điểm đấy em dùng làm gì
> Dùng như thế nào
> Đúng không?
> Câu này thì em đang bị
> Nó đang cố gắng ra lận
> Trong câu SQL ạ
> Nếu mà ghi là 1 bằng 1
> Kiểu kiểu thức hoạt
> Thì nó đang cố gắng ra lận
> Em không cho phép là 1 bằng 1
> Nó ghi là 2 bằng 2
> 3 bằng 3
> Đang cố gái ra lận đến này
> Câu hỏi thầy lại được chung nhớ
> Em giữ tôi đúng không ạ?
> Vâng
> Cũng không bị gì đến này
> Đành giá như thế nào ta, chuyện tốt đấy
> Nhưng mà cần phải sâu dài
> Tháng mấy được bảo vệ nhỉ
> Thực thể là
> Bố em ạ
> Mong là
> Cố gắng
> Là
> Đọc bảo vệ sớm hơn
> Nên trong thời gian em sẽ cố gắng hoàn thiện nhất có thể
> Thì nếu mà
> Tuần sau em trả lời thầy
> Chắc chắn
> Mình nghĩ là em cố gắng
> Vâng tuần sau
> Chiều 2 giờ sau
> Tuần này
> Vâng
> Chị mời chi tiết nha
> Tất cả các slide
> Những gì thầy đã
> Cái này chắc cũng đưa ra thôi, em sẽ hãy sửa lại một lần nữa
> Trong tháng 5 này là anh sốt được?
> Em thưa thầy, em muốn bày đây một xíu
> Thì là em có đọc trong 1 bài báo
> Là người ta khi mà xử lý dữ liệu dặn tích
> Thì là 50 hay 4
> Thì là người ta sẽ có 3 xu hướng
> Nghĩa là 1 là sử dụng cái VIA này
> Một cái tiếp theo là cái sequence gan
> Sequence gan là em đang làm thì em cảm thấy nó có tỷ lệ cao nhất
> Một cái nữa là Rumble Shopmark
> Em muốn hỏi là em có nên tìm hiểu nốt 2 phương án này để phòng trường hợp suy nghĩ ra không thành công được
> Nếu mốt thời gian, trước mắt em chứ không hoàn hành vậy ạ?
> Vậy đây thì chưa phải mất mốt thời gian
> Thế thôi
> Chắc thầy cũng biết là em đang kiểu một cua đấy
> Bắt đầu cũng ngòi một số thứ
> Thầy không hỏi về trước nhưng nếu mà đoạn kiểu em chỉ hiểu mang máng ra làm gì để kiểu nhờ AI chạy hay là...
> Nghe anh nhớ thầy như tuần sau ấy, chẳng phải chia sẻ chi tiết nữa thì hỏi nhé
> Vâng
> Em chắc nhà thầy đã làm được
> Giao lộn. Lộ trình của thầy trong tháng 5 này em sẽ chạy tín nghiệm xong hết
> Thế là sửa biết có thể rồi đúng không ạ?
> Vâng đúng
> Rồi còn phải xem
> Khi phải tự tin em chứ
> Em cũng tự tin là thầy
> Ờ, chắc thầy cũng biết là nước em đang mỏng thì thấy không đào quá sâu
> Đang hơi lo kể đấy các bạn ạ
> Đấy! Một cái cô bảo chính bạn là dùng liquid như thế nào nhé
> Vâng, như vậy nhé
> Cảm ơn thầy, đây là thầy ạ

---
*Bản transcript này đã được xử lý Denoise & VAD để đạt chất lượng tốt nhất.*