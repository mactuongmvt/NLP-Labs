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
├── prediction.md
├── implementation.py
├── experiments.ipynb       # bổ sung khi nhận starter notebook và corpus
├── results.csv
├── reflection.md
└── tests/
    └── test_implementation.py
```

## Chạy unit tests

Từ thư mục gốc của repository:

```bash
python -m pytest labs/lab01/tests -v
```

## Dữ liệu còn thiếu

Phần thực nghiệm trên 30K documents cần corpus và starter notebook do giảng viên cung cấp. Không thay thế bằng dataset khác để bảo đảm đúng yêu cầu đề bài.

## AI contribution

- AI generated the initial implementation of vocabulary construction, term counting, TF, IDF, TF-IDF, and cosine similarity.
- AI generated initial unit tests for the core implementation.
- The student will review the code, verify the formulas, run the experiments, and declare any later AI-assisted changes.
- AI was not used to answer the calculation exercises, make pre-experiment predictions, interpret numerical results, perform error analysis, or write the reflection.
