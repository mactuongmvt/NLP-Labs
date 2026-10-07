# Lab 03 — Word Representations and Embeddings

Lab này xây dựng word-context representation, huấn luyện Word2Vec và đánh giá embedding bằng similarity, analogy và semantic search.

## Thông tin

- Họ và tên: Mạc Văn Tường
- Mã sinh viên: 23001951

## Cấu trúc

- `calculations.md`: bài tính toán
- `prediction.md`: dự đoán trước thí nghiệm
- `calculations&prediction.pdf`: bản scan bài tính toán và prediction viết tay
- `cooccurrence.py`: cài đặt co-occurrence representation
- `word_embedding.ipynb`: các thí nghiệm
- `results.csv`: kết quả similarity, analogy và semantic search
- `error_analysis.md`: phân tích các trường hợp đúng và bất ngờ
- `reflection.md`: phần tổng kết
- `data/`: dữ liệu C4 30K

## Cách chạy

Từ thư mục gốc repository:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

Mở `labs/lab03/word_embedding.ipynb` và chọn **Run All Cells**.

## AI assistance statement

- Hỗ trợ kiểm tra code, debugging, chỉnh một số phần trình bày và giải thích lỗi trong quá trình làm lab.
- Một phần code hỗ trợ thí nghiệm, kiểm tra implementation và một số nội dung trình bày.
- Nội dung được chỉnh lại để phù hợp với implementation và kết quả thực nghiệm của bài.
- Chạy lại notebook, kiểm tra các phép tính cơ bản và đối chiếu kết quả với `results.csv`.
