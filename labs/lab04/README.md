# Lab 04 — Text Classification

Lab này xây dựng bài toán sentiment classification trên IMDb, so sánh TF-IDF và Average Word2Vec với Logistic Regression, sau đó đánh giá bằng accuracy, precision, recall, F1 và confusion matrix.

## Thông tin

- Họ và tên: Mạc Văn Tường
- Mã sinh viên: 23001951
- Lớp học phần: MAT3561E 4

## Cấu trúc

- `calculations.md`: bài tính toán
- `prediction.md`: dự đoán trước thí nghiệm
- `preprocessing.py`: hàm đọc dữ liệu, tokenize và tạo document vector
- `classification.ipynb`: các thí nghiệm classification
- `results.csv`: kết quả đánh giá các model
- `confusion_matrix.png`: confusion matrix của model được chọn trên validation set
- `error_analysis.md`: phân tích các prediction đúng và sai
- `reflection.md`: phần tổng kết
- `data/`: dữ liệu IMDb đã chia train/validation/test theo tỷ lệ 60/20/20

## Cách chạy

Từ thư mục gốc repository:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

Mở `labs/lab04/classification.ipynb` và chọn **Run All Cells**.

## AI assistance statement

- Hỗ trợ kiểm tra code, debugging, chỉnh một số phần trình bày và giải thích lỗi trong quá trình làm lab.
- Một phần code hỗ trợ thí nghiệm, kiểm tra implementation và một số nội dung trình bày.
- Chạy lại notebook, kiểm tra các phép tính cơ bản và đối chiếu kết quả với `results.csv`.
