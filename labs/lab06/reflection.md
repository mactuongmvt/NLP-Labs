# Reflection

Qua Lab 06, tôi hiểu Attention là cơ chế giúp model chọn và kết hợp thông tin từ các vị trí khác nhau trong sequence, thay vì chỉ phụ thuộc vào hidden state cuối như cách classification đơn giản với RNN/LSTM.

Trong Attention, Query được so sánh với các Key để tính scores. Các scores đi qua softmax để tạo attention weights, sau đó dùng các weights này kết hợp các Value thành context vector.

Phần scaling và temperature cho thấy việc thay đổi độ lớn của scores sẽ ảnh hưởng đến phân phối attention. Khi temperature tăng từ 0.5 lên 2.0, max weight giảm và entropy tăng, nghĩa là attention trở nên ít tập trung hơn.

Ở phần visualization, tôi thấy các token khác nhau có attention weights khác nhau và phân phối cũng thay đổi theo Query. Tuy nhiên, heatmap chỉ cho biết model đang phân phối attention như thế nào, chưa đủ để kết luận model thực sự hiểu ngữ pháp hoặc reasoning.

Trong thí nghiệm sentiment classification, Self-Attention đạt test F1 = 0.7226, cao hơn LSTM với F1 = 0.6548. Tuy nhiên LSTM lại có recall cao hơn. Vì vậy không thể kết luận Attention luôn tốt hơn LSTM chỉ từ một lần chạy.

Một hạn chế của full self-attention là attention matrix có kích thước T × T, nên số phần tử tăng theo T². Khi sequence dài, chi phí tính toán và bộ nhớ có thể tăng rất nhanh.

Như vậy, Attention giúp các token tương tác trực tiếp với nhau, giảm sự phụ thuộc vào việc truyền thông tin tuần tự qua nhiều hidden state. Tuy nhiên, Attention cũng có giới hạn về computational cost. Đây là cơ sở để tiếp tục học cách xây dựng mô hình Transformer ở Lab tiếp theo.
