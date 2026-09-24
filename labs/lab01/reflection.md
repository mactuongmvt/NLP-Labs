# Reflection

Dự đoán vocabulary khoảng 200.000 từ thấp hơn kết quả thực tế của Pipeline A là 473.388 từ. Số từ tăng nhiều do corpus có URL, tên riêng, lỗi chính tả, ký tự Unicode và các từ đi kèm dấu câu.

Dự đoán về sparsity phù hợp với kết quả thực nghiệm. Cả ba pipeline đều có hơn 99% số ô bằng 0. Mỗi tài liệu chỉ chứa một phần rất nhỏ vocabulary của toàn bộ corpus.

Một điểm đáng chú ý là các token có IDF cao nhất không phải lúc nào cũng có ích. Danh sách này có nhiều emoji, ký hiệu và chuỗi ký tự lỗi. Những token đó hiếm vì chỉ xuất hiện trong rất ít tài liệu, nhưng không mang nhiều ý nghĩa cho việc tìm kiếm.

Trên candidate pool và các nhãn relevance hiện có, Pipeline B cho kết quả tốt nhất với P@5 = 0,55, Recall@5 = 0,9375 và MRR = 0,6875. Pipeline C có cùng P@5 và Recall@5 nhưng MRR thấp hơn một chút, bằng 0,675. Các query không có document relevant trong candidate pool được dùng để chẩn đoán lỗi và không được đưa vào metric tổng hợp. Kết quả này phụ thuộc vào các nhãn relevance hiện có và cho thấy vocabulary nhỏ hơn không đồng nghĩa với tìm kiếm tốt hơn.

Query `transformer language model` thể hiện rõ giới hạn của TF-IDF. Kết quả đứng đầu nói về biến áp điện, trong khi query nói về mô hình ngôn ngữ. Hệ thống nhận ra các từ trùng nhau nhưng không hiểu nghĩa của từ trong ngữ cảnh.

Bài lab cho thấy preprocessing làm thay đổi vocabulary, vector TF-IDF và thứ tự kết quả tìm kiếm. TF-IDF hữu ích khi các tài liệu có từ trùng với query, nhưng còn hạn chế khi cần hiểu nghĩa và ngữ cảnh.

## Công cụ hỗ trợ

AI được sử dụng để hỗ trợ ban đầu về code, tổ chức thí nghiệm và gợi ý cách phân tích kết quả. Các kết quả, nhãn relevance và nội dung trình bày đã được đối chiếu với dữ liệu và yêu cầu của Lab 01.
