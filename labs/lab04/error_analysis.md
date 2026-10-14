# Error Analysis

Phần này phân tích model TF-IDF unigram + bigram + Logistic Regression vì model này có validation F1 cao nhất.

## Ba prediction đúng

### 1. Negative → Negative

Review có nhiều từ và cụm tiêu cực như `crap`, `no clue`, `worse` và `waste of time and money`.

Các feature này thể hiện sentiment negative khá rõ nên model dự đoán đúng.

### 2. Positive → Positive

Review có các cụm như `quite enjoyed`, `good actress` và `a decent film`.

Sentiment được thể hiện khá trực tiếp bằng từ vựng nên TF-IDF có thể bắt được các feature positive.

### 3. Positive → Positive

Review chứa các từ `delightful`, `wonderful`, `happy`, `inspirational` và cụm `highly recommend`.

Đây đều là những dấu hiệu positive rõ nên model dự đoán đúng.

## Ba prediction sai

### 4. Negative → Positive

Review có nhãn negative nhưng chứa cả những từ như `well`, `love` và `exciting`. Trong cùng review cũng có các ý negative như `boring` và `can't catch my attention`.

Review khá dài và có nhiều ý trái chiều nên các lexical feature positive và negative cùng xuất hiện. Model cuối cùng dự đoán thành positive.

### 5. Positive → Negative

Review có nhãn positive nhưng chứa nhiều từ negative như `shock`, `poor`, `terrible`, `horrendous` và `offensive`.

Người viết đang so sánh nhiều nội dung trong review, nên nếu chỉ nhìn các lexical feature riêng lẻ thì model dễ nghiêng về negative mặc dù nhãn cuối là positive.

### 6. Negative → Positive

Review có nhãn negative nhưng phần text lại chứa nhiều từ và cụm positive như `fair`, `enlightened`, `entertained`, `solid` và `cast is superb`.

Trong trường hợp này prediction positive khá phù hợp với phần text được quan sát. Có thể đây là một sample mà sentiment trong nội dung không khớp rõ với label.

## Confusion matrix

Trên test set:

- 4.422 negative được dự đoán đúng.
- 4.562 positive được dự đoán đúng.
- 518 negative bị dự đoán thành positive.
- 415 positive bị dự đoán thành negative.

False positive nhiều hơn false negative nên precision của class positive thấp hơn recall.

## Kết luận

Model làm tốt khi sentiment được thể hiện bằng các từ hoặc cụm từ rõ ràng. Các trường hợp khó hơn thường là review dài, có nhiều ý trái chiều hoặc khi các từ mang sentiment khác với label chung của review.
