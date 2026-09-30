# Lab 02 — Language Models

Lab này xây dựng n-gram language model gồm unigram, bigram và trigram, sau đó thử nghiệm MLE, Laplace smoothing, perplexity, next-word prediction và sentence ranking.

## Thông tin

- Họ và tên: Mạc Văn Tường
- Mã sinh viên: 23001951

## Cấu trúc

- `calculations.md`: bài tính toán
- `prediction.md`: dự đoán trước thí nghiệm
- `calculations&prediction.pdf`: bản scan bài viết tay
- `ngram_lm.py`: cài đặt n-gram language model
- `experiments.ipynb`: các thí nghiệm
- `results.csv`: kết quả perplexity và prediction
- `error_analysis.md`: phân tích prediction đúng/sai
- `reflection.md`: câu hỏi tổng kết
- `data/`: dữ liệu C4 30K

## Cách chạy

Từ thư mục gốc repository:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

Mở `labs/lab02/experiments.ipynb` và chọn **Run All Cells**.

## AI assistance statement

- Hỗ trợ kiểm tra code, debugging, chỉnh một số phần trình bày và giải thích lỗi trong quá trình làm lab.
- Một phần code hỗ trợ thí nghiệm, kiểm tra implementation và một số nội dung trình bày.
- Nội dung được chỉnh lại để phù hợp với implementation và kết quả thực nghiệm của bài.
- Chạy lại notebook, kiểm tra các phép tính cơ bản và đối chiếu kết quả với `results.csv`.
