# Lab 05 — Sequence Models: RNN, LSTM and GRU

Lab này xây dựng sentiment classifier trên IMDb bằng RNN, LSTM và GRU, sau đó so sánh với TF-IDF + Logistic Regression và khảo sát ảnh hưởng của sequence length.

## Thông tin

- Họ và tên: Mạc Văn Tường
- Mã sinh viên: 23001951
- Lớp học phần: MAT3561E 4

## Cấu trúc

- `calculations.md`: lời giải một bước RNN, information flow, vanishing gradient và LSTM gates
- `prediction.md`: các dự đoán theo mẫu Prediction / Reason / Confidence
- `rnn_cell.py`: cài đặt Simple RNN cell
- `sequence_classification.ipynb`: các thí nghiệm sequence classification
- `results.csv`: metrics và chi phí tính toán
- `learning_curves.png`: training/validation loss
- `confusion_matrix.png`: confusion matrix của model được chọn
- `error_analysis.md`: sáu prediction đúng/sai và các giả thuyết nguyên nhân lỗi
- `reflection.md`: bài học, giới hạn thí nghiệm, hướng cải thiện và learning check

Dataset sử dụng lại ba split IMDb 60/20/20 tại `labs/lab04/data`. Phần thống kê dataset dùng toàn bộ dữ liệu; các recurrent experiment dùng tập con cân bằng có seed cố định để có thể chạy lại trên CPU. `results.csv` ghi riêng baseline Lab 04 gốc (29.749/9.916/9.917 mẫu train/validation/test; test F1 = 0,907229) và baseline train lại trên tập con Lab 05 (4.000/1.000/2.000 mẫu; test F1 = 0,871668). Chỉ baseline trên tập con được dùng để so sánh trực tiếp với RNN, LSTM và GRU.

## Cách chạy

Từ thư mục gốc repository:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

Mở `labs/lab05/sequence_classification.ipynb` và chọn **Run All Cells**.

## AI assistance statement

- Hỗ trợ kiểm tra code, debugging, chỉnh một số phần trình bày và giải thích lỗi trong quá trình làm lab.
- Một phần code hỗ trợ thí nghiệm, kiểm tra implementation và một số nội dung trình bày.
- Chạy lại notebook, kiểm tra các phép tính cơ bản và đối chiếu kết quả với `results.csv`.
đ