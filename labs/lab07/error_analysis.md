# Error Analysis

Phân tích dùng Transformer 4 heads, length 64 và mean pooling trên 600 review test. Đây là cấu hình cố định cho analysis, không phải model được chọn theo test F1. Nhãn `0 = negative`, `1 = positive`; xác suất bên dưới luôn là `P(positive)`. `row_id` là chỉ số của review trong test subset.

Các top attention token được tính trung bình trên các head và query hợp lệ; không liệt kê key CLS. Đây là quan sát về phân phối weight, không phải bằng chứng về nguyên nhân prediction.

## Ba prediction đúng

### 1. Positive → Positive — row_id 1

- P(positive): `0.736641`
- Độ dài: 112 token; giữ 64 token đầu, có truncation.
- Top attention: `b`, `full`, `style`, `produced`, `its`.

Review gọi phim là một `gem` với các ý `refreshing`, `inventive` và `innovative` ngay trong phần được giữ lại. Các dấu hiệu positive khá rõ nên prediction phù hợp với nội dung. Top attention không chỉ gồm từ sentiment; không thể suy ra model chỉ dựa vào các từ đã liệt kê.

### 2. Positive → Positive — row_id 2

- P(positive): `0.927876`
- Độ dài: 87 token; có truncation.
- Top attention: `liked`, `colors`, `well`, `ways`, `action`.

Review mở đầu bằng “I liked the film” và nhắc nhiều cảnh `interesting`, `tense`, `well done`. Các cụm positive đã xuất hiện trước vị trí 64. Token `liked` và `well` cũng nhận attention cao, phù hợp với dấu hiệu sentiment được quan sát.

### 3. Negative → Negative — row_id 3

- P(positive): `0.041327`
- Độ dài: 141 token; có truncation.
- Top attention: `next`, `back`, `waste`, `just`, `give`.

Phần đầu có “Give me my money back”, `useless`, `waste` và `pointless`. Những dấu hiệu negative này có trong input được giữ lại. Model dự đoán đúng dù review bị cắt; `waste` nằm trong nhóm token nhận attention cao.

## Ba prediction sai

### 4. Negative → Positive — row_id 0

- P(positive): `0.505602`
- Độ dài: 44 token; không truncation.
- Top attention: `at`, `although`, `twenty`, `love`, `comedy`.
- Nhóm lỗi: negation, contrast, mixed sentiment.

Review có “difficult to follow”, “not very good” và “I have seen better”, nhưng cũng có `harmless`, `comedy`, `funny`. Model dự đoán positive rất sát ngưỡng 0.5. Toàn bộ câu đã được đưa vào model nên lỗi không đến từ truncation. Một giả thuyết là model chưa kết hợp tốt các ý trái chiều và phủ định; top attention chứa nhiều token chưa thể hiện rõ đánh giá negative.

### 5. Negative → Positive — row_id 5

- P(positive): `0.778497`
- Độ dài: 316 token; có truncation.
- Top attention: `think`, `show`, `could`, `those`, `fans`.
- Nhóm lỗi: contrast/sarcasm, long sequence, truncation.

Review phê bình Family Guy. Phần đầu nhắc cách người hâm mộ đánh giá phim là `witty`, `edgy`, `poignant`, rồi phủ nhận bằng “it's none of these”. Các từ `dull`, `repetitive`, `insulting`, `uninspired` nằm ngay sau phần 64 token được giữ lại và không đến được model. Truncation có thể góp phần vào lỗi, nhưng input vẫn có `crummy nonsense`, nên không đủ để xem đây là nguyên nhân duy nhất.

Các token attention cao chủ yếu nói về chương trình và người xem, chưa thể hiện trực tiếp ý phê bình. Đây là quan sát, không chứng minh model sai vì chú ý tới các từ này.

### 6. Negative → Positive — row_id 6

- P(positive): `0.792749`
- Độ dài: 274 token; có truncation.
- Top attention: `do`, `movies`, `do`, `pop`, `type`.
- Nhóm lỗi: long sequence, truncation, mixed sentiment.

Review phàn nàn về nhạc phim với `really tired`, `generic music`, `cheesy pop tune` và `diluting the suspense`. Input cũng có cụm `genuine tension` trong một ý bị phê bình. Các tín hiệu negative đã có trước khi cắt, nên model có thể chưa kết hợp tốt ý của các cụm này; phần chê chi tiết phía sau cũng bị mất. Top attention chủ yếu gồm từ trung tính, nhưng riêng phân phối này không xác định được nguyên nhân prediction sai.

## Application

Model dự đoán đúng câu ngắn, câu dài và câu “I do not like this movie”. Câu contrast có `bad` ở đầu và `excellent` ở cuối bị dự đoán negative với P(positive) `0.028625`. Câu ambiguous bị dự đoán positive với xác suất `0.972602`, khác kỳ vọng thủ công negative; trường hợp này không có nhãn chuẩn IMDb để xem là một lỗi benchmark.

## Confusion matrix

- TN = 188, FP = 112.
- FN = 88, TP = 212.

Accuracy là `0.666667`, precision `0.654321`, recall `0.706667`, F1 `0.679487`. False positive nhiều hơn false negative 24 review.

## Kết luận

Ba prediction đúng đều bị truncation nhưng vẫn có tín hiệu sentiment rõ trong phần đầu. Một prediction sai không bị truncation. Vì vậy việc cắt review chỉ là một yếu tố cần xem xét, không giải thích được mọi lỗi.

Các trường hợp sai cho thấy model còn khó với phủ định, contrast, sentiment trái chiều và review dài. Attention hỗ trợ mô tả model behavior, nhưng không thể đồng nhất attention với explanation.
