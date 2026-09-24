# Lab 01 — From Text Processing to Search

## Thông tin

- Họ và tên: Mạc Văn Tường
- Mã sinh viên: 23001951
- Lớp học phần: MAT3561E 4
- Chủ đề: Text Processing, TF-IDF Representation và Document Search
- Hạn nộp: 23:59, ngày 24/09/2026
- Trạng thái: Hoàn thành

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
├── data/
│   ├── README.md
│   └── c4-train.00000-of-01024-30K.json.gz
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
labs/lab01/data/c4-train.00000-of-01024-30K.json.gz
```

Dataset được lưu ngay trong thư mục của Lab 01 và được đưa lên repository theo yêu cầu của giảng viên. Notebook đọc trực tiếp file nén `.json.gz`, không cần giải nén.

## Chạy notebook

```powershell
.\.venv\Scripts\Activate.ps1
jupyter lab
```

Mở `labs/lab01/experiments.ipynb` và chọn **Run All Cells**. Notebook kiểm thử implementation, chạy ba pipeline, lưu retrieval cùng metric vào `results.csv`. Relevance labels đã được gán trong biến `reviewed_relevant` ở Part H sau khi đối chiếu nội dung các document trong candidate pool.

## Nội dung đã hoàn thành

1. Bài tính tay và prediction được đính kèm trong `Calculations&Prediction.pdf` và chép lại ở hai file Markdown tương ứng.
2. Sáu hàm TF-IDF cốt lõi được triển khai trong `implementation.py` và kiểm thử trong Part E.
3. Ba pipeline preprocessing được chạy trên đủ 30.000 documents.
4. Kết quả Top-5, nhãn relevance và các metric được lưu trong `results.csv`.
5. Phân tích lỗi, reflection và learning check được trình bày đầy đủ trong notebook và `reflection.md`.

## Khai báo công cụ hỗ trợ

AI được sử dụng để hỗ trợ về code, tổ chức thí nghiệm. Các kết quả, nhãn relevance và nội dung trình bày đã được đối chiếu với dữ liệu và yêu cầu của Lab 01.
