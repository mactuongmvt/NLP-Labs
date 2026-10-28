# Lab 06 — Attention Mechanism

Lab này tính và cài đặt scaled dot-product attention, khảo sát scaling và temperature, trực quan hóa self-attention, rồi so sánh classifier attention với LSTM trên dữ liệu IMDb.

## Thông tin

- Họ và tên: Mạc Văn Tường
- Mã sinh viên: 23001951
- Lớp học phần: MAT3561E 4

## Cấu trúc

- `calculations.md`: các bài tính attention, softmax, context và scaling
- `prediction.md`: dự đoán trước thí nghiệm
- `attention_numpy.py`: implementation scaled dot-product attention bằng NumPy
- `self_attention.ipynb`: thí nghiệm, classifier và phân tích
- `results.csv`: kết quả so sánh LSTM và attention
- `attention_heatmap.png`: attention matrix của hai câu mẫu
- `confusion_matrix.png`: confusion matrix của attention classifier
- `error_analysis.md`: phân tích prediction đúng và sai
- `reflection.md`: tổng kết những gì học được về Attention, kết quả thực nghiệm, các hạn chế và mối liên hệ với Transformer.

Dữ liệu IMDb được dùng lại từ `labs/lab04/data`. Thí nghiệm classifier dùng các tập con cân bằng với seed cố định để giảm thời gian chạy.

**Lưu ý về dữ liệu:** Lab 06 sử dụng lại các file `imdb_train.csv.gz`, `imdb_validation.csv.gz` và `imdb_test.csv.gz` từ thư mục `labs/lab04/data`. Vì vậy cần giữ nguyên cấu trúc repository và có đủ dữ liệu Lab 04 trước khi chạy notebook.

## Cách chạy

Từ thư mục gốc repository:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

Mở `labs/lab06/self_attention.ipynb` và chọn **Run All Cells**.

Notebook được thiết kế để chạy từ thư mục gốc repository hoặc từ thư mục `labs/lab06`. Không chạy riêng notebook trong một thư mục khác nếu chưa điều chỉnh đường dẫn dữ liệu.

## AI assistance statement

- Tool: OpenAI Codex.
- Purpose: hỗ trợ implementation, debugging và trình bày kết quả.
- Generated: một phần code và nội dung Markdown.
- Modified: nội dung được rà soát theo đề và kết quả thí nghiệm.
- Verified: chạy notebook, kiểm tra implementation NumPy và đối chiếu `results.csv`.
