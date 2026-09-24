# Dự đoán trước khi chạy thí nghiệm

Nội dung dưới đây được chép lại từ phần prediction trong [bản scan viết tay](./Calculations%26Prediction.pdf).

## Prediction 1 — Vocabulary

Vocabulary được dự đoán có khoảng 200.000 từ khác nhau. Corpus có 30.000 tài liệu thuộc nhiều chủ đề nên có thể chứa tên riêng, URL, từ viết tắt, lỗi chính tả và nhiều dạng khác nhau của cùng một từ.

## Prediction 2 — Sparsity

Ma trận TF-IDF được dự đoán là sparse, nghĩa là phần lớn các ô bằng 0. Mỗi tài liệu chỉ chứa một số nhỏ từ trong khi vocabulary của cả corpus có thể rất lớn. Tỷ lệ ô bằng 0 có thể lớn hơn 90%.

## Prediction 3 — Search

Các tài liệu đứng đầu chưa chắc có nghĩa gần nhất với query. TF-IDF chủ yếu dựa vào các từ xuất hiện giống nhau. Một tài liệu có nhiều từ trùng nhưng sai chủ đề vẫn có thể được xếp cao, còn tài liệu cùng nghĩa nhưng dùng từ khác có thể bị xếp thấp.
