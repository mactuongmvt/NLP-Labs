# Calculations

## Bài 1 — Binary classification

```text
z = w^T x + b
  = 0,5 × 1 + (-0,2) × 2 + 0,4 × 0 + 0,1
  = 0,2

σ(z) = 1 / (1 + e^(-z))

σ(0,2) = 1 / (1 + e^(-0,2)) ≈ 0,5498
```

Vậy `P(y = 1 | x) ≈ 0,5498`.

## Bài 2 — Prediction threshold

Trường hợp `τ = 0,5`:

```text
0,72 > 0,5
```

Model dự đoán class 1.

Trường hợp `τ = 0,8`:

```text
0,72 < 0,8
```

Model dự đoán class 0.

Nếu tăng threshold, model sẽ khó dự đoán positive hơn:

- Số dự đoán positive giảm.
- Precision thường tăng vì model chỉ chọn các mẫu có độ tin cậy cao.
- Recall có thể giảm vì nhiều positive thật bị bỏ sót.

Nếu giảm threshold, model dễ dự đoán positive hơn:

- Số dự đoán positive tăng.
- Recall thường tăng vì bắt được nhiều positive hơn.
- Precision có thể giảm vì dễ kéo theo nhiều false positive hơn.

## Bài 3 — Confusion matrix

```text
Precision = TP / (TP + FP)
          = 80 / (80 + 10)
          = 80 / 90
          ≈ 0,8889

Recall = TP / (TP + FN)
       = 80 / (80 + 20)
       = 0,8

F1 = 2PR / (P + R)
   = (2 × 0,8889 × 0,8) / (0,8889 + 0,8)
   ≈ 0,8421
   = 84,21%
```

Nếu đây là bài toán phát hiện spam:

- False positive là email bình thường nhưng bị dự đoán nhầm thành spam.
- False negative là email spam nhưng bị dự đoán nhầm thành email thường.

## Bài 4 — Accuracy trap

Model đạt accuracy 95% nhưng chưa thể kết luận là model tốt.

Nguyên nhân là dataset bị mất cân bằng: có 950 mẫu negative và chỉ 50 mẫu positive. Model dự đoán tất cả là negative nên chỉ đạt accuracy cao nhưng không phát hiện được bất kỳ mẫu positive nào.

Vì vậy cần xem thêm các metric như precision, recall và F1, đặc biệt là đối với class positive, thay vì chỉ dựa vào accuracy.
