# Reflection

Sau Lab 07, việc ghép được Transformer block chưa có nghĩa là đã có một model xử lý ngôn ngữ tốt. Khi train từ đầu, model phải học representation và cách phân loại cùng lúc từ dữ liệu IMDb. Với tập train nhỏ, hai epoch có thể chưa đủ để học các đặc điểm cần thiết. Đây là lý do trong thực tế thường bắt đầu bằng pretrained model thay vì luôn train từ đầu.

ALBERT đã học representation trong pretraining bằng MLM và SOP. Trong lab này, model tiếp tục học sentiment từ review phim qua một classification head. Với cùng 600 mẫu train và 200 mẫu test, ALBERT đạt F1 0.7902, còn Transformer nhỏ từ đầu đạt 0.5306. Kết quả cho thấy pretrained representation hữu ích trong cấu hình đang xét, nhưng hai kiến trúc khác nhau nên chưa thể quy mọi chênh lệch cho pretraining.

Frozen encoder giúp nhìn rõ vai trò của representation có sẵn. Khi chỉ train head, F1 là 0.6520; full fine-tuning đạt 0.7902. Fine-tuning cho phép điều chỉnh encoder theo downstream task, trong khi frozen giữ nguyên các feature. Tuy nhiên learning rate, số epoch và cách tối ưu cũng ảnh hưởng kết quả, nên không thể kết luận full fine-tuning luôn tốt hơn.

Thí nghiệm lượng dữ liệu cần đọc cả đường cong. Một model dự đoán gần như toàn positive vẫn có thể có F1 tương đối cao trên tập cân bằng, dù accuracy gần mức đoán ngẫu nhiên. Vì vậy không nên chọn một điểm rồi kết luận model sử dụng dữ liệu hiệu quả. Các kết quả mới có một seed nên còn cần kiểm tra thêm độ ổn định.

Pretraining giúp tận dụng công sức huấn luyện trước đó nhưng không loại bỏ computational cost. Training và validation của ALBERT mất khoảng 658 giây, scratch khoảng 17 giây. ALBERT chia sẻ trọng số nhưng vẫn tính qua nhiều layer. Sequence dài làm attention tốn thêm thời gian và memory. Các số đo CPU phụ thuộc tải hệ thống, nên không xem đây là benchmark phần cứng chính xác.

Cuối cùng, pretrained model vẫn có lỗi khi review bị cắt, sentiment trái chiều hoặc cách diễn đạt thay đổi. Đánh giá trên Amazon giúp quan sát việc chuyển domain, còn confidence analysis cho thấy xác suất softmax cao vẫn có thể sai. Lab chưa đo catastrophic forgetting hay hiệu chỉnh confidence. Với một downstream task mới, vẫn cần kiểm tra tokenizer, split, metric và lỗi cụ thể thay vì mặc định pretrained model đã giải quyết được mọi trường hợp.
