# Prediction trước experiment

## Prediction 1 — TF-IDF + Logistic Regression và RNN + Embedding

Prediction: RNN + Embedding có khả năng xử lý word order trực tiếp hơn TF-IDF + Logistic Regression.

Reason: RNN đọc các token theo thứ tự và hidden state ở mỗi bước phụ thuộc vào token hiện tại cùng hidden state trước đó. TF-IDF không mô hình hóa sequence theo cách này.

Confidence: Cao.

## Prediction 2 — RNN và LSTM

Prediction: LSTM có khả năng xử lý dependency dài tốt hơn Simple RNN.

Reason: LSTM có cell state và các gates để kiểm soát việc giữ hoặc loại bỏ thông tin, nên thông tin từ các timestep xa có khả năng được giữ tốt hơn so với Simple RNN.

Confidence: Khá cao.

## Prediction 3 — Sequence length 50 → 200

Prediction: Khi tăng max_length từ 50 lên 200, training sẽ chậm hơn và tốn nhiều tài nguyên hơn.

Reason: Mỗi review có nhiều timestep hơn nên recurrent model phải thực hiện nhiều bước tính toán hơn. Việc tăng sequence length không chắc chắn làm performance tăng.

Confidence: Cao.

## Prediction 4 — Truncation về 30 tokens

Prediction: Có, classification có thể bị ảnh hưởng nếu toàn bộ review bị truncate về 30 tokens.

Reason: Phần bị cắt có thể chứa từ sentiment quan trọng, negation, câu kết luận hoặc đoạn contrast xuất hiện ở cuối review.

Confidence: Khá cao.

## Prediction 5 — LSTM và RNN trên mọi dataset

Prediction: Không, LSTM không chắc chắn có accuracy cao hơn RNN trên mọi dataset.

Reason: Kết quả còn phụ thuộc vào dataset, sequence length, lượng dữ liệu, hyperparameters và cách training. LSTM có lợi thế về long dependency nhưng kiến trúc phức tạp hơn không đồng nghĩa luôn cho accuracy cao hơn.

Confidence: Cao.
