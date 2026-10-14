# Prediction trước experiment

## Prediction 1 — TF-IDF + Logistic Regression

- **Prediction:** Theo tôi, TF-IDF + Logistic Regression có khả năng hoạt động tốt, nhưng phụ thuộc vào dataset và bài toán.
- **Reason:** TF-IDF giữ được thông tin về các từ đặc trưng trong văn bản. Với những bài toán mà một số từ hoặc cụm từ có khả năng phân biệt class rõ, Logistic Regression có thể học được các feature này để classification.
- **Confidence:** Khá cao.

## Prediction 2 — Average Word2Vec so với TF-IDF

- **Prediction:** Average Word2Vec không chắc chắn tốt hơn TF-IDF.
- **Reason:** Average Word2Vec có thể biểu diễn quan hệ ngữ nghĩa giữa các từ, nhưng việc lấy trung bình các word embedding có thể làm mất word order và một số từ quan trọng trong câu. TF-IDF giữ thông tin từ và term rõ hơn, nên representation nào tốt hơn còn phụ thuộc vào dataset và bài toán.
- **Confidence:** Cao.

## Prediction 3 — Tăng vocabulary size

- **Prediction:** Tăng vocabulary size không chắc làm accuracy tăng.
- **Reason:** Vocabulary lớn hơn giúp giữ được nhiều từ hơn, nhưng cũng có thể thêm các từ hiếm hoặc ít liên quan. Điều này làm feature space lớn hơn nhưng không đảm bảo các feature mới đều hữu ích cho classification.
- **Confidence:** Cao.

## Prediction 4 — Bỏ stopwords

- **Prediction:** Bỏ stopwords không chắc chắn làm performance tăng.
- **Reason:** Một số stopwords có thể không mang nhiều thông tin phân loại, nhưng một số từ như `not` có thể ảnh hưởng nhiều đến nghĩa của câu. Nếu loại bỏ những từ như vậy, model có thể mất thông tin quan trọng.
- **Confidence:** Cao.

## Prediction 5 — Accuracy và F1

- **Prediction:** Accuracy và F1 có thể cho kết luận khác nhau.
- **Reason:** Với dataset mất cân bằng, model có thể đạt accuracy cao bằng cách dự đoán tốt các class chiếm đa số nhưng lại bỏ sót nhiều mẫu class thiểu số. F1 kết hợp precision và recall nên phản ánh tốt hơn khả năng dự đoán của model trong trường hợp này.
- **Confidence:** Cao.
