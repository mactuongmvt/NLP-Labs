# Error Analysis

Model được phân tích là GRU với `max_length = 100`, vì đây là model được chọn theo validation F1 trong phần so sánh architecture.

| Text (trích đoạn review) | True | Predicted | Analysis |
|---|---|---|---|
| Mẫu 1: “I found it hard to sit through.” | Negative | Negative | Tín hiệu chê phim nằm trong phần đầu được giữ lại. |
| Mẫu 2: “Great movie. I was laughing all time through.” | Positive | Positive | Dự đoán đúng nhưng xác suất rất sát ngưỡng 0.5. |
| Mẫu 3: “this is a *really* bad movie.” | Negative | Negative | Tín hiệu negative rõ ngay đầu review. |
| Mẫu 0: “The movie in a word is superlative.” | Positive | Negative | Có lời khen nhưng review cũng dùng từ tiêu cực khi phản bác ý kiến khác; phần sau bị cắt. |
| Mẫu 5: “the actors that were in this film did a good job” | Positive | Negative | Lời khen xen với các cụm ít tích cực; 57 token cuối bị cắt. |
| Mẫu 14: “his wife squeed over it.” | Negative | Positive | Đầu review nhắc phản ứng tích cực của người khác; phần lớn review bị cắt. |

## Ba prediction đúng

### Mẫu 1 — Negative → Negative

- P(positive) = 0.0169
- Sequence length = 159
- Review bị truncate ở 100 tokens.

Phần đầu review có nhiều tín hiệu negative nên model dự đoán Negative đúng.

Mặc dù review bị truncate, thông tin trong 100 tokens đầu vẫn đủ cho prediction này.

### Mẫu 2 — Positive → Positive

- P(positive) = 0.5043
- Sequence length = 84
- Không bị truncate.

Review có các tín hiệu positive khá rõ và model dự đoán đúng.

Tuy nhiên xác suất 0.5043 rất gần threshold 0.5 nên đây là một prediction đúng nhưng độ chắc chắn không cao.

### Mẫu 3 — Negative → Negative

- P(positive) = 0.0164
- Sequence length = 273
- Review bị truncate ở 100 tokens.

Phần đầu review chứa nhiều tín hiệu negative nên model dự đoán đúng dù không nhìn thấy toàn bộ review.

## Ba prediction sai

### Mẫu 0 — Positive → Negative

- P(positive) = 0.0226
- Sequence length = 565
- Review bị truncate ở 100 tokens.

Trong phần text quan sát được có cả tín hiệu positive và negative nên sentiment không hoàn toàn đơn giản.

Review dài hơn nhiều so với `max_length = 100`, vì vậy model không nhìn thấy phần lớn nội dung phía sau.

**Nguyên nhân có thể:** mixed sentiment và truncation.

**Có phải lỗi sequence modeling không?** Chưa thể kết luận. Truncation chắc chắn làm mất context, nhưng chỉ từ một sample này chưa đủ để nói RNN/GRU không xử lý được sequence.

### Mẫu 5 — Positive → Negative

- P(positive) = 0.0470
- Sequence length = 157
- Review bị truncate ở 100 tokens.

Phần đầu review có cả lời khen và một số cụm mang sắc thái không tích cực, nên model có thể nghiêng về Negative.

Vì sequence dài 157 tokens nên 57 tokens cuối không được đưa vào model.

**Nguyên nhân có thể:** ambiguous sentiment và truncation.

**Có phải lỗi sequence modeling không?** Chưa chắc. Việc mất phần cuối do truncation là một nguyên nhân hợp lý hơn để xem xét trước.

### Mẫu 14 — Negative → Positive

- P(positive) = 0.8560
- Sequence length = 787
- Review bị truncate ở 100 tokens.

Đây là review rất dài nhưng model chỉ được nhìn 100 tokens đầu. Phần đầu có một số tín hiệu có thể khiến model nghiêng về Positive.

**Nguyên nhân có thể:** truncation và context chưa đầy đủ.

**Có phải lỗi sequence modeling không?** Không thể kết luận chỉ từ prediction này. Model không được nhìn thấy phần lớn review nên lỗi có thể đến từ giới hạn input trước khi xét đến khả năng ghi nhớ của GRU.

## Confusion matrix

Confusion matrix trên test set:

- True Negative = 775
- False Positive = 225
- False Negative = 420
- True Positive = 580

False Negative nhiều hơn False Positive:

420 > 225

Nghĩa là model bỏ sót review Positive nhiều hơn số review Negative bị dự đoán nhầm thành Positive.

Điều này phù hợp với kết quả:

- Precision = 0.7205
- Recall = 0.5800

Recall thấp hơn precision vì số False Negative khá lớn.

## Kết luận

Các ví dụ trên cho thấy model có thể dự đoán tốt khi sentiment xuất hiện rõ trong phần context được giữ lại.

Trong các prediction sai, review dài và truncation xuất hiện ở cả ba trường hợp. Tuy nhiên ba sample là chưa đủ để kết luận truncation là nguyên nhân chung của mọi lỗi hoặc khẳng định lỗi đến từ sequence modeling.

Cần phân biệt giữa điều quan sát được từ experiment và nguyên nhân lý thuyết của lỗi.
