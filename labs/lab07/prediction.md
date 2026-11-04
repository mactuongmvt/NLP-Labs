# Prediction

## Prediction 1

**Prediction:** Transformer có thể xử lý các vị trí trong sequence song song hơn RNN.

**Reason:** Self-attention tính tương tác bằng phép nhân ma trận; RNN phải cập nhật hidden state lần lượt theo timestep.

**Confidence:** Cao.

## Prediction 2

**Prediction:** Nếu bỏ positional information, model self-attention này không biết thứ tự token.

**Reason:** Các projection dùng cùng một phép biến đổi cho mọi vị trí và không được cung cấp chỉ số vị trí.

**Confidence:** Cao.

## Prediction 3

**Prediction:** Hai câu có cùng token nhưng đổi thứ tự sẽ có cùng mean-pooled representation khi không dùng positional information, trong điều kiện eval và không thay đổi phần bị truncation.

**Reason:** Đổi thứ tự input làm các output token đổi theo cùng thứ tự; mean pooling cho kết quả không đổi.

**Confidence:** Cao.

## Prediction 4

**Prediction:** Các head không nhất thiết học cùng một attention pattern.

**Reason:** Mỗi head sử dụng các projection riêng nên có thể tạo weight khác nhau trên cùng input.

**Confidence:** Cao.

## Prediction 5

**Prediction:** Tăng số head không chắc chắn làm accuracy tăng.

**Reason:** Khi d_model cố định, nhiều head hơn đồng thời làm dimension mỗi head nhỏ hơn. Kết quả còn phụ thuộc dữ liệu và training.

**Confidence:** Cao.

## Prediction 6

**Prediction:** Transformer không luôn nhanh hơn RNN ở mọi sequence length.

**Reason:** Transformer có thể song song hóa tốt hơn nhưng full attention có chi phí theo T². Thời gian còn phụ thuộc batch size và phần cứng.

**Confidence:** Trung bình.
