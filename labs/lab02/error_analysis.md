# Error Analysis

Phần này sử dụng trigram với Laplace smoothing trên test set.

## Hai prediction đúng

### 1. Context `year by`

- Model prediction: `the`
- Expected: `the`
- Probability: khoảng `0,000146`
- Context count trong train: 16
- Count của `year by the`: 6

Model dự đoán đúng vì `the` đã xuất hiện khá nhiều lần sau context `year by` trong training data. Vì vậy xác suất của `the` cao hơn các từ còn lại.

### 2. Context `is by`

- Model prediction: `far`
- Expected: `far`
- Probability: khoảng `0,000209`
- Context count trong train: 63
- Count của `is by far`: 9

Cụm `is by far` đã xuất hiện nhiều lần trong training data nên model có đủ dữ liệu để dự đoán đúng từ `far`.

## Hai prediction sai

### 3. Context `america s`

- Model prediction: `top`
- Expected: `best`
- Probability của prediction: khoảng `0,000084`
- Context count trong train: 28
- Count của `america s best`: 2

Ở trường hợp này `best` đã từng xuất hiện sau context nhưng ít hơn từ `top`, nên model chọn `top`.

Ngoài ra, context `america s` cũng cho thấy một hạn chế ở bước preprocessing. Tokenizer hiện tại nhận dấu nháy `'` nhưng không nhận dấu `’`, vì vậy một từ như `America’s` có thể bị tách thành `america` và `s`.

### 4. Context `s best`

- Model prediction: `to`
- Expected: `colleges`
- Probability của prediction: khoảng `0,000209`
- Context count trong train: 49
- Count của `s best colleges`: 0

Trigram `s best colleges` chưa từng xuất hiện trong training data. Laplace giúp xác suất của `colleges` không bằng 0, nhưng xác suất đó vẫn rất nhỏ. Trong khi đó `to` đã xuất hiện sau context này nhiều hơn nên model chọn `to`.

## Kết luận

Các prediction đúng thường là những trường hợp model đã thấy pattern đó đủ nhiều trong training data. Các prediction sai chủ yếu liên quan đến dữ liệu ít, unseen trigram và preprocessing. Laplace giúp tránh xác suất bằng 0 nhưng không đảm bảo model sẽ chọn đúng từ tiếp theo.
