# Bài tập tính toán

Nội dung dưới đây được chép lại từ [bản scan viết tay](./calculations%26prediction.pdf).

## Bài 1 — Unigram

1. Vocabulary:

```text
{the, cat, dog, eats, likes, fish, meat}
```

2. Tổng số token: `N = 12`.

3. Xác suất:

```text
P(the)   = 3/12 = 1/4
P(cat)   = 2/12 = 1/6
P(fish)  = 2/12 = 1/6
P(dog)   = 1/12
P(eats)  = 2/12 = 1/6
P(likes) = 1/12
P(meat)  = 1/12
```

4. Tổng xác suất:

```text
ΣP(w) = 1/4 + 1/6 + 1/6 + 1/12 + 1/6 + 1/12 + 1/12 = 1
```

## Bài 2 — Bigram

```text
P(cat | the)   = 2/3
P(dog | the)   = 1/3
P(eats | cat)  = 1/2
P(likes | cat) = 1/2
```

```text
P(cat | the) + P(dog | the) = 2/3 + 1/3 = 1
```

Trong corpus này, `the` chỉ đứng trước `cat` và `dog`. Cụ thể, `cat` xuất hiện hai lần và `dog` xuất hiện một lần sau `the`; `the` xuất hiện tổng cộng ba lần nên tổng hai xác suất bằng 1.

## Bài 3 — Xác suất câu

```text
P(the)         = 3/12 = 1/4
P(cat | the)   = 2/3
P(eats | cat)  = 1/2
P(fish | eats) = 1/2

P(the cat eats fish)
= P(the) × P(cat | the) × P(eats | cat) × P(fish | eats)
= 1/24
```

Nếu thêm một từ vào câu thì xác suất của cả câu không thể tăng, vì xác suất của từ mới nằm trong khoảng từ 0 đến 1. Trong trường hợp đặc biệt, nếu xác suất của từ mới bằng 1 thì xác suất giữ nguyên, không tăng.

## Bài 4 — Sentence ranking

Dự đoán: Tôi dự đoán `S1` sẽ cao hơn `S2`.

Khi dùng bigram thì hai câu đều có xác suất bằng nhau.

## Bài tập suy luận trước khi smoothing

1. Count của `study AI` là 0.
2. Xác suất MLE:

```text
P(AI | study) = 0/1 = 0
```

3. Khi tính xác suất câu có chứa bigram này thì xác suất của cả câu luôn bằng 0.
4. Điều này không có nghĩa câu đó chắc chắn không thể xảy ra. Nó chỉ có nghĩa bigram `study AI` chưa được quan sát thấy trong training corpus. Có thể một cụm từ không xuất hiện trong corpus không đồng nghĩa cụm đó không xuất hiện trong thực tế.

## Bài tập tính smoothing

```text
C(cat) = 10
C(cat eats) = 0
V = 5

P_Laplace(eats | cat) = (0 + 1) / (10 + 5) = 1/15
```

Với `C(cat eats) = 3`:

```text
P_Laplace(eats | cat) = (3 + 1) / (10 + 5) = 4/15
P_MLE(eats | cat) = 3/10 = 0,3
```

Smoothing làm xác suất của các n-gram thường bị giảm xuống, còn xác suất của các n-gram chưa xuất hiện tăng lên một phần từ các n-gram đã xuất hiện, khiến chúng khác 0 và nhận giá trị dương.

## Bài tập tính Perplexity

```text
P(w₁) = 0,5
P(w₂ | w₁) = 0,25
P(w₃ | w₂) = 0,5

P(W) = 0,5 × 0,25 × 0,5 = 0,0625
PP(W) = P(W)^(-1/3) = ∛16 ≈ 2,52
```

Với `P(w₂ | w₁) = 0,1`:

```text
P(W) = 0,025
PP(W) = 3,42
```

Khi giảm một xác suất nào đó thì `P(W)` cũng giảm. Mà `PP(W)` là tỉ lệ nghịch với `P(W)` nên nó sẽ tăng.
