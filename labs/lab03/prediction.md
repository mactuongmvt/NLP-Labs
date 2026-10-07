# Dự đoán trước khi chạy thí nghiệm

## Prediction 1 — Những từ gần nhau

- Prediction: `doctor` gần `physician` nhất, sau đó đến `hospital`. `banana` và `car` sẽ ở xa hơn.
- Reason: `doctor` và `physician` thường xuất hiện trong các context liên quan đến bệnh nhân và điều trị.
- Confidence: cao.

## Prediction 2 — Context window

- Prediction: similarity sẽ thay đổi khi window tăng từ 2 lên 5.
- Reason: window lớn hơn đưa thêm các từ xa vào context, nên vector chứa nhiều thông tin chủ đề hơn nhưng cũng có thể thêm nhiễu.
- Confidence: cao.

## Prediction 3 — Embedding dimension

- Prediction: tăng dimension từ 50 lên 100 có thể giúp model biểu diễn tốt hơn, nhưng 300 chiều không chắc chắn tốt nhất.
- Reason: dimension lớn cần nhiều dữ liệu và thời gian huấn luyện hơn; corpus không đủ lớn có thể làm các chiều bổ sung không hữu ích.
- Confidence: trung bình.

## Prediction 4 — Corpus nhỏ

- Prediction: `doctor` và `physician` không chắc chắn gần nhau nếu corpus chỉ có 100 câu.
- Reason: hai từ có thể xuất hiện quá ít hoặc không có đủ context chung để model học được quan hệ.
- Confidence: cao.
