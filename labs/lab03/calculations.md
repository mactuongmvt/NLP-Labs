# Bài tập tính toán

## Bài 1 — Co-occurrence

Với thứ tự context:

```text
[cat, dog, eats, likes, fish, milk, meat]
```

và `window = 1`, các vector là:

```text
cat   = [0, 0, 1, 1, 0, 0, 0]
dog   = [0, 0, 1, 1, 0, 0, 0]
eats  = [1, 1, 0, 0, 2, 0, 0]
likes = [1, 1, 0, 0, 0, 1, 1]
```

`cat` và `dog` có cùng vector vì chúng xuất hiện cạnh các context giống nhau trong corpus này.

## Bài 2 — Cosine similarity

Cho:

```text
x = [1, 2, 1]
y = [2, 4, 2]
```

Ta có:

```text
x · y = 1×2 + 2×4 + 1×2 = 12
||x|| = √6
||y|| = √24 = 2√6

cos(x, y) = 12 / (√6 × 2√6) = 1
```

Hai vector có độ lớn khác nhau nhưng cùng hướng vì `y = 2x`. Điều này cho thấy cosine similarity quan tâm đến hướng và tỉ lệ giữa các thành phần, không phụ thuộc trực tiếp vào độ lớn vector.

## Bài 3 — Semantic similarity

```text
doctor    = [0,8; 0,1; 0,7]
physician = [0,7; 0,2; 0,8]
nurse     = [-0,2; 0,9; -0,1]
```

Dự đoán trước khi tính: `physician` gần `doctor` hơn.

```text
doctor · physician = 1,14
||doctor|| = √1,14
||physician|| = √1,17

cos(doctor, physician)
= 1,14 / (√1,14 × √1,17)
≈ 0,9871
```

```text
doctor · nurse = -0,14
||nurse|| = √0,86

cos(doctor, nurse)
= -0,14 / (√1,14 × √0,86)
≈ -0,1414
```

Kết quả đúng với dự đoán: `physician` gần `doctor` hơn.

## Bài 4 — Sparse và dense

1. Word-context representation 10.000 chiều với 30 giá trị khác 0 là sparse.
2. Embedding 300 chiều với hầu hết thành phần khác 0 là dense.
3. Dense representation có số chiều nhỏ hơn và có thể đặt các từ dùng trong context tương tự ở gần nhau, nên thuận lợi hơn khi tính semantic similarity.
4. Dense representation không chắc chắn tốt hơn trong mọi bài toán. Count hoặc TF-IDF vẫn hữu ích khi cần thông tin từ xuất hiện chính xác và dễ giải thích.

## CBOW và Skip-gram

CBOW dùng các từ context để dự đoán target. Skip-gram làm ngược lại: dùng target để dự đoán các từ context.

Với câu `the cat eats fish` và `window = 1`:

### CBOW

```text
[cat]       → the
[the, eats] → cat
[cat, fish] → eats
[eats]      → fish
```

### Skip-gram

```text
the  → cat
cat  → the
cat  → eats
eats → cat
eats → fish
fish → eats
```

## Bài tập analogy

```text
king  = [8, 2, 7]
man   = [5, 1, 5]
woman = [5, 3, 5]

king - man + woman
= [8, 2, 7] - [5, 1, 5] + [5, 3, 5]
= [8, 4, 7]
```

Vector mới có thể biểu diễn quan hệ từ một người nam thuộc hoàng gia sang một người nữ thuộc hoàng gia, nên từ được kỳ vọng là `queen`.
