# Lab 01 — From Text Processing to Search

## Thông tin

- Chủ đề: Text Processing, TF-IDF Representation và Document Search
- Hạn nộp: 23:59, ngày 24/09/2026
- Trạng thái: Đang thực hiện

## Mục tiêu thực nghiệm

1. Khảo sát biểu diễn TF-IDF thưa trên corpus khoảng 30.000 documents.
2. Tự triển khai TF, IDF, TF-IDF và cosine similarity trên corpus nhỏ.
3. So sánh các lựa chọn preprocessing.
4. Xây dựng và đánh giá hệ thống tìm kiếm document bằng TF-IDF.

## Cấu trúc

```text
lab01/
├── README.md
├── calculations.md
├── Calculations&Prediction.pdf
├── prediction.md
├── implementation.py
├── experiments.ipynb
├── results.csv
└── reflection.md
```

`Calculations&Prediction.pdf` là bản scan bài tính và prediction viết tay, được liên kết từ `calculations.md` và `prediction.md`.

## Kiểm chứng core implementation

`implementation.py` chứa sáu hàm cốt lõi và các hàm hỗ trợ thí nghiệm. TF được chuẩn hóa theo tổng số term và `IDF = ln(N/DF)`. Phần E trong notebook kiểm thử từng hàm, sau đó chuyển kết quả scikit-learn về cùng convention để đối chiếu.

## Dữ liệu

Notebook sử dụng corpus 30K documents do giảng viên cung cấp tại:

```text
data/raw/c4-train.00000-of-01024-30K.json.gz
```

Dataset được `.gitignore` loại trừ và không được đưa lên GitHub.

## Chạy notebook

```powershell
.\.venv\Scripts\Activate.ps1
jupyter lab
```

Mở `labs/lab01/experiments.ipynb` và chọn **Run All Cells**. Notebook kiểm thử implementation, chạy ba pipeline, lưu retrieval cùng metric vào `results.csv`. Relevance labels nằm trong biến `reviewed_relevant` ở Part H và cần được kiểm tra lần cuối trước khi nộp.

## Việc cần kiểm tra trước khi nộp

1. Mở thử liên kết tới `Calculations&Prediction.pdf` trong `calculations.md` và `prediction.md`.
2. Đối chiếu nội dung trong `prediction.md` với dự đoán đã ghi trước khi chạy thí nghiệm.
3. Kiểm tra biến `reviewed_relevant` trong Part H của notebook.
4. Chạy lại toàn bộ `experiments.ipynb` sau khi sửa nhãn và kiểm tra `results.csv`.
5. Rà soát nhận xét kết quả, phần phân tích lỗi và `reflection.md`.
6. Kiểm tra lại mục khai báo công cụ hỗ trợ.

## Khai báo công cụ hỗ trợ

AI được sử dụng để hỗ trợ về code, tổ chức thí nghiệm và gợi ý phân tích. Các kết quả, nhãn relevance và nội dung trình bày cần được kiểm tra lại trước khi nộp.
