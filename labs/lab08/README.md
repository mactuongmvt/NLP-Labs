# Lab 08 — Pretrained Transformers and ALBERT Fine-Tuning

Lab này dùng ALBERT để phân loại sentiment trên IMDb, so sánh pretrained với Transformer train từ đầu, frozen encoder với fine-tuning và ảnh hưởng của lượng dữ liệu, sequence length, domain shift và confidence.

## Thông tin

- Họ và tên: Mạc Văn Tường
- Mã sinh viên: 23001951
- Lớp học phần: MAT3561E 4

## Cấu trúc

- `calculations.md`: MLM loss và hướng dẫn xem kết quả tokenization
- `prediction.md`: ba prediction trước experiment
- `tokenization.ipynb`: tokenizer, special tokens, attention mask và MLM
- `pretrained_classification.py`: model, dữ liệu, training và evaluation
- `fine_tuning.ipynb`: các thí nghiệm theo mục của W8
- `results.csv`: kết quả định lượng
- `data_efficiency.png`: F1 ở 10/25/50/100% training data
- `confusion_matrix.png`: confusion matrix IMDb
- `confidence_analysis.png`: confidence và tỷ lệ dự đoán đúng
- `error_analysis.md`: false positive, false negative và các câu hỏi phân tích
- `reflection.md`: tổng kết 300–500 từ
- `data/amazon_cells_labelled.txt`: dữ liệu product reviews dùng cho domain shift

## Model và dữ liệu

Checkpoint và tokenizer: [`albert/albert-base-v2`](https://huggingface.co/albert/albert-base-v2), revision `8e2f239c5f8a2c0f253781ca60135db913e5c80c`. Đây là bản ALBERT base khoảng 12 triệu tham số, pretrained bằng MLM và SOP; dùng factorized embedding và chia sẻ tham số giữa các layer. Không dùng checkpoint đã fine-tune sentiment sẵn.

Dùng lại các file `imdb_train.csv.gz`, `imdb_validation.csv.gz`, `imdb_test.csv.gz` trong `labs/lab04/data`. Lấy tập con cân bằng 600 train, 200 validation, 200 test để chạy trên CPU. Giữ nguyên ranh giới split của Lab 04; không gộp rồi chia lại. Các tập train 10/25/50/100% là tập con lồng nhau; validation/test giữ cố định.

Model scratch dùng Transformer block của `labs/lab07`, khởi tạo ngẫu nhiên, 128 chiều, 4 heads, FFN 256. Cả hai pipeline dùng cùng tokenizer ALBERT với vocabulary 30.000 token và cùng giới hạn token. Vì kiến trúc và learning rate khác nhau, kết quả không tách riêng được hoàn toàn ảnh hưởng của pretraining. Không lấy trực tiếp số liệu Lab 07 để so sánh vì tokenizer, budget token và tập con đã thay đổi.

Domain B dùng Amazon product reviews thuộc [UCI Sentiment Labelled Sentences](https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences), Kotzias (2015), DOI: 10.24432/C57604, giấy phép CC BY 4.0. Dữ liệu này chỉ dùng đánh giá model đã train/chọn checkpoint trên IMDb. Code loại text trùng và loại overlap với IMDb subset trước đánh giá. Domain và style/độ dài cùng thay đổi nên không diễn giải chênh lệch chỉ do domain.

## Cấu hình

- Seed: 42; batch size: 8; epochs: 2; optimizer: AdamW, weight decay 0.01.
- Learning rate: full fine-tuning `2e-5`; frozen head và scratch `1e-3`.
- Max length chính: 64; thí nghiệm độ dài: 64, 128, 256. Length tính cả special tokens.
- Nhãn: `0 = negative`, `1 = positive`. Precision/recall/F1 tính cho positive.
- Best checkpoint chọn bằng validation F1; test chỉ dùng báo cáo.
- Domain shift, confusion matrix, error analysis và confidence analysis dùng cố định ALBERT full-train, length 64; không chọn cấu hình bằng test F1.
- Frozen encoder ở `eval()` và không cập nhật trọng số. Trích xuất train/validation features một lần rồi train head.
- Training time gồm train và validation; frozen tính cả thời gian trích xuất train/validation features. Không gồm download, tokenization hoặc test inference.
- CPU memory là peak RSS toàn tiến trình lấy mẫu trong training, gồm Python và allocator; không phải lượng memory riêng của model hay ma trận attention. Các run thực hiện tuần tự trong cùng kernel.
- Hardware, phiên bản PyTorch, hash của các split và cấu hình được in trong notebook; số liệu lưu trong `results.csv`.

## Cách chạy

Từ thư mục gốc repository:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

Chạy `tokenization.ipynb`, sau đó `fine_tuning.ipynb`. Cả hai chạy từ thư mục gốc repository hoặc `labs/lab08`. Cần giữ đủ dữ liệu Lab 04 và hai module Transformer của Lab 07.

Lần đầu cần Internet để tải model/tokenizer; cache đặt trong `models/huggingface`. Checkpoint được lưu trong `checkpoints/lab08`. Hai thư mục này được Git bỏ qua. Notebook mặc định dùng lại checkpoint cục bộ nếu có để tiếp tục sau gián đoạn; training time khi đó là số đo từ lần huấn luyện gốc. Đặt `REUSE_CHECKPOINTS = False` để huấn luyện lại toàn bộ. Khi tải repository mới chưa có checkpoint, các cấu hình sẽ được train; các cấu hình trùng nhau trong cùng lần chạy chỉ train một lần.

## AI assistance statement

- Hỗ trợ kiểm tra code, debugging, chỉnh một số phần trình bày và giải thích lỗi trong quá trình làm lab.
- Một phần code hỗ trợ thí nghiệm, kiểm tra implementation và một số nội dung trình bày.
- Chạy lại notebook, kiểm tra các phép tính cơ bản và đối chiếu kết quả với `results.csv`.
