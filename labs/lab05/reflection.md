# Reflection

Trong lần chạy này, TF-IDF + Logistic Regression có F1 cao hơn RNN, LSTM và GRU. Điều này cho thấy model phức tạp hơn không chắc chắn cho kết quả classification tốt hơn trong mọi trường hợp. Baseline đơn giản vẫn cần thiết để so sánh.

So với Average Word2Vec ở Lab 04, các recurrent model có ưu điểm là đọc token theo thứ tự và duy trì hidden state qua các timestep. Vì vậy model có khả năng sử dụng word order và context trước đó thay vì gộp toàn bộ câu thành một vector trung bình ngay từ đầu.

Trong ba recurrent model, Simple RNN có F1 thấp nhất. LSTM và GRU cho kết quả tốt hơn Simple RNN trong thí nghiệm này, phù hợp với ý tưởng rằng các cơ chế gate giúp kiểm soát information flow tốt hơn.

Experiment về sequence length cho thấy tăng max_length có thể giữ thêm context nhưng cũng làm training time tăng nhiều. Trong kết quả hiện tại, tăng từ 50 lên 100 không làm F1 tăng, còn max_length = 200 mới cho F1 tốt hơn. Vì vậy sequence length cần được chọn dựa trên cả performance và computational cost.

Learning curves cũng cho thấy RNN, LSTM và GRU đều có dấu hiệu overfitting khi training loss tiếp tục giảm nhưng validation loss tăng ở các epoch sau.

Một hạn chế còn lại là recurrent model vẫn xử lý sequence theo từng bước. Với sequence dài, thông tin phải đi qua nhiều timestep và training cũng tốn thời gian hơn. LSTM và GRU giúp cải thiện việc giữ thông tin dài hơn Simple RNN nhưng không loại bỏ hoàn toàn giới hạn của recurrent processing.

Đây là lý do cần nghiên cứu các cơ chế cho phép model truy cập trực tiếp các phần quan trọng khác trong sequence, dẫn tới Attention ở lab tiếp theo.
