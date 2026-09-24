# Bài tập tính toán

Nội dung dưới đây được chép lại từ bài làm viết tay và đối chiếu theo công thức trong đề bài.

[Xem bản scan Calculations & Prediction](./Calculations%26Prediction.pdf)

## Exercise 1 — Count Vector

Vocabulary:

```text
[cat, dog, eats, fish, likes]
```

* D1 = `cat eats fish` → `[1, 0, 1, 1, 0]`
* D2 = `dog eats fish` → `[0, 1, 1, 1, 0]`
* D3 = `cat likes fish` → `[1, 0, 0, 1, 1]`

## Exercise 2 — TF

D1 có ba từ là `cat`, `eats` và `fish`. Mỗi từ xuất hiện một lần nên:

* `tf(cat, D1) = 1/3`
* `tf(eats, D1) = 1/3`
* `tf(fish, D1) = 1/3`

Tổng ba giá trị TF bằng 1.

## Exercise 3 — IDF

Với `N = 3` và công thức `idf(t) = ln(N/df(t))`:

| Từ    | DF |                  IDF |
| ----- | -: | -------------------: |
| cat   |  2 | `ln(3/2) ≈ 0.406` |
| dog   |  1 |   `ln(3) ≈ 1.099` |
| eats  |  2 | `ln(3/2) ≈ 0.406` |
| fish  |  3 |          `ln(1) = 0` |
| likes |  1 |   `ln(3) ≈ 1.099` |

`fish` có IDF thấp nhất vì xuất hiện trong cả ba tài liệu. Từ này không giúp phân biệt một tài liệu với các tài liệu còn lại.

## Exercise 4 — TF-IDF của D1

* `tfidf(cat, D1) = (1/3) × ln(3/2) ≈ 0.1352`
* `tfidf(eats, D1) = (1/3) × ln(3/2) ≈ 0.1352`
* `tfidf(fish, D1) = (1/3) × ln(1) = 0`

Dù `fish` xuất hiện trong D1, TF-IDF của từ này vẫn bằng 0 vì IDF bằng 0.

## Exercise 5 — Cosine Similarity

Với `x = [1, 1, 1]` và `y = [1, 1, 0]`:

```text
x · y = 2
||x|| = √3
||y|| = √2
cos(x, y) = 2 / √6 ≈ 0.816497
```

Cosine similarity không chỉ đếm số từ trùng nhau. Nó so sánh hướng của hai vector, nên kết quả không bằng `2/3`.

## Exercise 6 — Prediction

1. D1 có similarity cao nhất vì nội dung trùng hoàn toàn với query.
2. D3 có similarity thấp nhất vì không có từ nào chung với query.
3. `medical` và `image` có IDF thấp hơn `classification` vì chúng xuất hiện trong D1 và D2.
4. Nếu chỉ dùng count vector, thứ tự vẫn là D1, D2 rồi D3. D1 trùng tất cả từ với query, D2 chỉ trùng hai từ, còn D3 không có từ chung.
