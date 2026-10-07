# Dự đoán trước khi chạy thí nghiệm

## Prediction 1 — Những từ gần nhau

- Prediction: `doctor` và `physician` sẽ có similarity cao nhất. `hospital` cũng khá gần nghĩa với hai từ này.
- Reason: `doctor` và `physician` đều có nghĩa là bác sĩ, còn `hospital` liên quan vì bác sĩ thường làm việc ở bệnh viện.
- Confidence: cao.

## Prediction 2 — Context window

- Prediction: similarity có thể thay đổi khi context window tăng từ 2 lên 5.
- Reason: window lớn hơn làm mỗi từ được biểu diễn dựa trên nhiều từ xung quanh hơn. Điều này làm thay đổi vector context và có thể làm thay đổi cosine similarity. Window lớn hơn có thể thu được nhiều thông tin ngữ nghĩa hơn nhưng cũng có thể thêm những context ít liên quan.
- Confidence: cao.

## Prediction 3 — Embedding dimension

- Prediction: tăng dimension không chắc chắn làm chất lượng embedding tốt hơn.
- Reason: dimension lớn giúp model biểu diễn nhiều thông tin hơn nhưng cũng cần nhiều dữ liệu và chi phí tính toán hơn. Nếu corpus không đủ lớn, tăng dimension có thể không cải thiện chất lượng embedding.
- Confidence: cao.

## Prediction 4 — Corpus nhỏ

- Prediction: `doctor` và `physician` không chắc chắn có similarity cao nếu corpus chỉ có 100 câu.
- Reason: word embedding phụ thuộc vào ngữ cảnh xuất hiện của từ trong corpus. Với 100 câu, dữ liệu có thể không đủ để `doctor` và `physician` xuất hiện nhiều lần trong các context tương tự, nên model có thể chưa học được mối quan hệ ngữ nghĩa giữa hai từ một cách rõ ràng.
- Confidence: cao.
