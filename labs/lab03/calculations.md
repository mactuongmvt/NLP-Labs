# Bài tập tính toán

## Bài 1 — Co-occurrence

Với thứ tự context:

```text
[the, cat, dog, eats, likes, fish, milk, meat]
```

và `window = 1`, các vector là:

```text
cat   = [2, 0, 0, 1, 1, 0, 0, 0]
dog   = [2, 0, 0, 1, 1, 0, 0, 0]
eats  = [0, 1, 1, 0, 0, 2, 0, 0]
likes = [0, 1, 1, 0, 0, 0, 1, 1]
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
banana    = [-0,2; 0,9; -0,1]
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
doctor · banana = -0,14
||banana|| = √0,86

cos(doctor, banana)
= -0,14 / (√1,14 × √0,86)
≈ -0,1414
```

Kết quả đúng với dự đoán: `physician` gần `doctor` hơn.

## Bài 4 — Sparse và dense

1. Biểu diễn 10.000 chiều nhưng chỉ có 30 giá trị khác 0 là sparse representation vì phần lớn phần tử của vector bằng 0.
2. Embedding 300 chiều với hầu hết giá trị khác 0 là dense representation.
3. Dense representation có thể thuận lợi cho semantic similarity vì nó biểu diễn thông tin ngữ cảnh và ngữ nghĩa trong không gian có số chiều nhỏ hơn. Những từ xuất hiện trong các ngữ cảnh tương tự thường có vector gần nhau, nên cosine similarity có thể đo mức độ tương đồng ngữ nghĩa hiệu quả hơn biểu diễn sparse chỉ dựa trên tần suất xuất hiện.
4. Dense representation không chắc chắn tốt hơn trong mọi bài toán. Dense phù hợp với bài toán cần semantic similarity và giảm số chiều biểu diễn, còn sparse dễ giải thích hơn và phù hợp với bài toán cần thông tin về sự xuất hiện hoặc tần suất chính xác của từ. Việc lựa chọn phụ thuộc vào bài toán cụ thể.

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

Vector mới có thể đại diện cho một từ có quan hệ với `king` tương tự quan hệ giữa `woman` và `man`, chẳng hạn như `queen`. Đây là ví dụ về gender pattern có thể tồn tại trong không gian embedding.
