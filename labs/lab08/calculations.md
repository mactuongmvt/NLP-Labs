# Calculations

## 9. Calculation Exercise 1 — MLM Loss

Chỉ có một vị trí bị mask. Token đúng là `eats`, xác suất model gán cho token này là 0.70.

$$
L=-\ln P(\text{eats}\mid x)=-\ln(0.70)\approx0.356675.
$$

**1. Nếu xác suất là 0.95:**

$$
L=-\ln(0.95)\approx0.051293.
$$

Loss giảm vì model gán xác suất cao hơn cho token đúng.

**2. Nếu xác suất là 0.01:**

$$
L=-\ln(0.01)\approx4.605170.
$$

Loss tăng mạnh vì model gán xác suất rất thấp cho token đúng.

**3. Vì sao cross-entropy phù hợp với MLM?**

Tại vị trí bị mask, model chọn token đúng trong vocabulary. Cross-entropy đo mức model gán xác suất cho token đó: xác suất càng cao thì loss càng thấp. Các phép tính trên dùng logarithm tự nhiên.

## 10. Calculation Exercise 2 — Tokenization

Câu `The cats are playing.` được tokenize bằng tokenizer của `albert/albert-base-v2`. Kết quả dưới đây lấy từ lần chạy thật trong `tokenization.ipynb`.

| Token | ID | Special token | Attention mask |
|---|---:|---:|---:|
| `[CLS]` | 2 | 1 | 1 |
| `▁the` | 14 | 0 | 1 |
| `▁cats` | 9471 | 0 | 1 |
| `▁are` | 50 | 0 | 1 |
| `▁playing` | 791 | 0 | 1 |
| `.` | 9 | 0 | 1 |
| `[SEP]` | 3 | 1 | 1 |

- Token sequence: `[CLS], ▁the, ▁cats, ▁are, ▁playing, ., [SEP]`.
- Token IDs: `[2, 14, 9471, 50, 791, 9, 3]`.
- Attention mask: `[1, 1, 1, 1, 1, 1, 1]`, vì không có padding.
- Có 4 words nếu đếm theo khoảng trắng, 7 tokens nếu tính special tokens, 5 content subword tokens nếu bỏ special tokens và tính cả dấu câu.
- Bốn từ đều được biểu diễn bằng một piece; dấu chấm là token riêng. Không có continuation piece bên trong từ trong ví dụ này.

Dấu `▁` thể hiện ranh giới từ trong tokenizer SentencePiece. ALBERT dùng `<pad>` và `<unk>` cho padding và unknown; tên token không hoàn toàn giống ví dụ BERT trong đề.
