# Reflection

Qua Lab 07, có thể thấy Transformer không chỉ gồm attention. Positional encoding bổ sung vị trí; multi-head attention tạo nhiều phép tương tác; FFN biến đổi từng token; residual và LayerNorm giúp giữ đường truyền thông tin và hỗ trợ training.

Permutation experiment cho thấy khi không có PE, mean-pooled representation gần như không đổi nếu đảo cùng một bộ token. Khi thêm PE, representation thay đổi. Đây là bằng chứng trực tiếp cho vai trò của positional information, nhưng không tự chứng minh model hiểu nghĩa câu.

Giữ d_model = 128 thì số head tăng không làm tổng representation dimension hay số tham số tăng trong implementation này. Các head có pattern khác nhau trên câu mẫu, nhưng không thể tự gán mỗi head một chức năng ngôn ngữ. Accuracy cũng không tăng đều khi đổi từ 1 lên 2, 4, 8 heads.

Ở length 64, Transformer đạt test F1 = 0.6795, LSTM đạt 0.6433. Transformer có accuracy cao hơn nhưng LSTM có recall cao hơn. Vì vậy kết quả không có nghĩa Transformer tốt hơn theo mọi metric. Latency forward ở length 256 cũng cho thấy Transformer chậm hơn LSTM trên máy đang chạy, phù hợp dự đoán rằng Transformer không luôn nhanh hơn.

Tăng length từ 32 lên 256 giúp giữ lại nhiều token hơn và F1 tăng từ 0.6750 lên 0.7903 trong thí nghiệm. Đổi lại, training time tăng từ 8.629 lên 107.005 giây. Attention matrix lớn theo T² nên không thể chỉ tăng chiều dài mà bỏ qua bộ nhớ và thời gian.

Mean pooling và CLS-style pooling cho kết quả F1 khá gần nhau: 0.6795 và 0.6765. CLS trong bài được học từ đầu, không có sẵn khả năng tổng hợp câu từ pretraining. Learning curves cũng cho thấy dấu hiệu overfitting, đặc biệt ở LSTM; dữ liệu nhỏ và một seed là giới hạn của kết quả.

Các review sai cho thấy phủ định, contrast và truncation vẫn gây khó khăn. Weight cao ở một token chỉ là quan sát về model, chưa đủ để xác định nguyên nhân prediction. Những dự đoán đầu lab nhìn chung phù hợp với phạm vi đã đo; chưa có quan sát phủ định chúng, nhưng không thể suy rộng thành quy luật chung.

Transformer đã bổ sung vị trí và ghép các thành phần thành một encoder hoàn chỉnh hơn Lab 06, nhưng vẫn cần dữ liệu và training đủ tốt. Đây là cơ sở để tiếp tục tìm hiểu việc dùng Transformer đã pretrained ở lab tiếp theo.
