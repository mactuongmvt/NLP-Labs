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

- Tool: OpenAI Codex.
- Purpose: hỗ trợ implementation, debugging và trình bày kết quả.
- Generated content: một phần code và Markdown trong notebook.
- Modified content: tôi kiểm tra và chỉnh lại nội dung theo kết quả chạy thực tế.
- Verification: chạy lại toàn bộ notebook và đối chiếu kết quả với `results.csv`.
