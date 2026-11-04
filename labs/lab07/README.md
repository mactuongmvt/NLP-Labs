# Lab 07 — Transformer Architecture

Lab này ghép một Transformer Encoder block từ multi-head self-attention, positional encoding, residual, LayerNorm và FFN. Các thí nghiệm dùng IMDb để khảo sát số head, sequence length, pooling và so sánh với LSTM.

## Thông tin

- Họ và tên: Mạc Văn Tường
- Mã sinh viên: 23001951
- Lớp học phần: MAT3561E 4

## Cấu trúc

- `calculations.md`: attention head, positional encoding, FFN, residual và shape
- `prediction.md`: sáu prediction trước experiment
- `transformer_block.py`: multi-head attention và Transformer block tự ghép
- `positional_encoding.py`: sinusoidal positional encoding
- `transformer_classification.ipynb`: các thí nghiệm theo mục của đề
- `results.csv`: kết quả heads, architecture, length và pooling
- `positional_encoding.png`: trực quan hóa positional encoding
- `attention_heads.png`: attention matrix của bốn head
- `learning_curves.png`: training/validation loss theo epoch
- `confusion_matrix.png`: kết quả Transformer trên test set
- `error_analysis.md`: ba prediction đúng và ba prediction sai
- `reflection.md`: tổng kết và đối chiếu prediction

## Dữ liệu và cấu hình

Dùng lại `imdb_train.csv.gz`, `imdb_validation.csv.gz`, `imdb_test.csv.gz` trong `labs/lab04/data`. Cần giữ nguyên cấu trúc repository và có đủ ba file dữ liệu trước khi chạy.

Tập con cân bằng gồm 1.800 train, 600 validation và 600 test review (60/20/20), seed 42. Vocabulary chỉ xây từ train, tối đa 8.000 token. Các model dùng embedding dimension 128, batch size 32, Adam với learning rate 0.001 và 5 epoch. Checkpoint được chọn theo validation F1.

Training time gồm 5 epoch và validation sau mỗi epoch, không gồm đánh giá test. Latency forward ở mục prediction verification là phép đo riêng trên batch 8.

Transformer được học từ đầu và tự ghép bằng primitive PyTorch, không dùng pretrained model hoặc `TransformerEncoderLayer`. Model 4 heads, length 64, mean pooling là cấu hình cố định cho visualization, application và error analysis. Các thí nghiệm dùng chung split; cấu hình trùng được dùng lại cùng một lần training trong `results.csv`.

`max_length` là số token văn bản được giữ lại. Transformer thêm một CLS token học từ đầu; mean pooling bỏ CLS và padding, còn CLS-style pooling lấy output của CLS. Hai cấu hình pooling có cùng input và số tham số.

Nhãn `0 = negative`, `1 = positive`. `tokens_retained_percent` được tính trên toàn bộ tập con train/validation/test. Attention memory trong notebook là ước lượng kích thước một score matrix, không phải tổng bộ nhớ training.

## Cách chạy

Từ thư mục gốc repository:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

Mở `labs/lab07/transformer_classification.ipynb` và chọn **Run All Cells**. Notebook chạy được từ thư mục gốc repository hoặc `labs/lab07`. Training time phụ thuộc phần cứng; output được lưu từ lần chạy trên CPU.

## AI assistance statement

- Hỗ trợ kiểm tra code, debugging, chỉnh một số phần trình bày và giải thích lỗi trong quá trình làm lab.
- Một phần code hỗ trợ thí nghiệm, kiểm tra implementation và một số nội dung trình bày.
- Chạy lại notebook, kiểm tra các phép tính cơ bản và đối chiếu kết quả với `results.csv`.
