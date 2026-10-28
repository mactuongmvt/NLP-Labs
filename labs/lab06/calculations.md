# Calculations

## Bài 1 — Attention scores

Với `q = [1, 2]`, các key là `[1, 0]`, `[0, 1]`, `[1, 1]`.

```text
s1 = q · k1 = 1×1 + 2×0 = 1
s2 = q · k2 = 1×0 + 2×1 = 2
s3 = q · k3 = 1×1 + 2×1 = 3

s = [1, 2, 3]
```

## Bài 2 — Softmax

Cho score vector:

$$
s=[1,2,3]
$$

Công thức:

$$
\alpha_i=\frac{e^{s_i}}{\sum_j e^{s_j}}
$$

Ta có:

$$
e^1\approx2.7183,\quad e^2\approx7.3891,\quad e^3\approx20.0855
$$

Mẫu số:

$$
D=2.7183+7.3891+20.0855=30.1929
$$

Tính từng attention weight:

$$
\alpha_1=\frac{2.7183}{30.1929}\approx0.0900
$$

$$
\alpha_2=\frac{7.3891}{30.1929}\approx0.2447
$$

$$
\alpha_3=\frac{20.0855}{30.1929}\approx0.6652
$$

Vậy:

$$
\boxed{\alpha\approx[0.0900,0.2447,0.6652]}
$$

Tổng các weight bằng 1 (sai số nhỏ do làm tròn).

Phần tử thứ ba có score lớn nhất nên nhận attention weight lớn nhất. Vì hàm mũ tăng theo score và các phần tử có cùng mẫu số.

## Bài 3 — Context vector

Với `α = [0,1; 0,2; 0,7]`, `v1 = [1, 0]`, `v2 = [0, 1]`, `v3 = [2, 2]`:

```text
c = 0,1[1, 0] + 0,2[0, 1] + 0,7[2, 2]
  = [0,1 + 1,4; 0,2 + 1,4]
  = [1,5; 1,6]
```

`v3` đóng góp nhiều nhất vì có attention weight lớn nhất.

## Bài 4 — Toàn bộ attention computation

Cho:

$$
q=\begin{bmatrix}1\\0\end{bmatrix}
$$

$$
k_1=\begin{bmatrix}1\\0\end{bmatrix},\quad
k_2=\begin{bmatrix}0\\1\end{bmatrix},\quad
k_3=\begin{bmatrix}1\\1\end{bmatrix}
$$

$$
v_1=\begin{bmatrix}1\\0\end{bmatrix},\quad
v_2=\begin{bmatrix}0\\2\end{bmatrix},\quad
v_3=\begin{bmatrix}2\\1\end{bmatrix}
$$

**Bước 1: Tính scores**

$$
s_1=q^Tk_1=1\times1+0\times0=1
$$

$$
s_2=q^Tk_2=1\times0+0\times1=0
$$

$$
s_3=q^Tk_3=1\times1+0\times1=1
$$

Vậy:

$$
s=[1,0,1]
$$

**Bước 2: Tính softmax**

Mẫu số:

$$
D=e^1+e^0+e^1=2.7183+1+2.7183=6.4366
$$

$$
\alpha_1=\frac{2.7183}{6.4366}\approx0.4223
$$

$$
\alpha_2=\frac{1}{6.4366}\approx0.1554
$$

$$
\alpha_3=\frac{2.7183}{6.4366}\approx0.4223
$$

Vậy:

$$
\alpha\approx[0.4223,0.1554,0.4223]
$$

**Bước 3: Tính Context Vector**

$$
c=\alpha_1v_1+\alpha_2v_2+\alpha_3v_3
$$

$$
c\approx
0.4223\begin{bmatrix}1\\0\end{bmatrix}
+
0.1554\begin{bmatrix}0\\2\end{bmatrix}
+
0.4223\begin{bmatrix}2\\1\end{bmatrix}
$$

$$
c\approx
\begin{bmatrix}0.4223\\0\end{bmatrix}
+
\begin{bmatrix}0\\0.3108\end{bmatrix}
+
\begin{bmatrix}0.8446\\0.4223\end{bmatrix}
$$

Vậy:

$$
\boxed{c\approx\begin{bmatrix}1.2670\\0.7330\end{bmatrix}}
$$

Kết quả cuối dùng các weight chưa làm tròn. Nếu cộng trực tiếp các vector trung gian đã làm tròn ở trên thì được `[1.2669, 0.7331]`, chênh lệch nhỏ do làm tròn.

Hai Key thứ nhất và thứ ba có score bằng nhau và cao nhất nên nhận attention weight lớn nhất.

## Bài tập — Scaling

Với `dk = 4`, `QKᵀ = [4, 2, 0]`:

```text
scaled scores = [4, 2, 0] / √4 = [2, 1, 0]
softmax(scaled scores) ≈ [0,6652; 0,2447; 0,0900]
softmax([4, 2, 0])     ≈ [0,8668; 0,1173; 0,0159]
```

Khi không scaling, phân phối tập trung hơn vào score lớn nhất. Chia cho `√dk` làm chênh lệch score nhỏ hơn trước softmax.

## Temperature

Dùng `s = [1, 2, 3]` và `softmax(s/T)`; entropy tính theo nat.

| T | Attention weights | Max weight | Entropy |
|---:|---|---:|---:|
| 0,5 | [0,0159; 0,1173; 0,8668] | 0,8668 | 0,4411 |
| 1,0 | [0,0900; 0,2447; 0,6652] | 0,6652 | 0,8324 |
| 2,0 | [0,1863; 0,3072; 0,5065] | 0,5065 | 1,0202 |

Temperature thấp làm phân phối tập trung hơn; temperature cao làm phân phối phẳng hơn.

## Numerical stability

Trừ cùng một hằng số `m = max(x)` không làm đổi softmax vì:

```text
exp(xi - m) / Σj exp(xj - m)
= exp(xi)exp(-m) / (exp(-m)Σj exp(xj))
= exp(xi) / Σj exp(xj)
```

Phép trừ này giữ nguyên kết quả nhưng tránh tính `exp` của các số quá lớn.

## Bài tập self-attention — Ví dụ minh họa

Đề không cho giá trị cụ thể của `X`, `WQ`, `WK`, `WV`. Để minh họa phép tính, chọn:

```text
X = [[1, 0], [0, 1], [1, 1]]
WQ = WK = WV = [[1, 0], [0, 1]]
```

Khi đó `Q = K = V = X`, `dk = 2`:

```text
QKᵀ / √2 = [[0,7071, 0,0000, 0,7071],
             [0,0000, 0,7071, 0,7071],
             [0,7071, 0,7071, 1,4142]]

attention weights ≈ [[0,4011, 0,1978, 0,4011],
                     [0,1978, 0,4011, 0,4011],
                     [0,2483, 0,2483, 0,5035]]

context ≈ [[0,8022, 0,5989],
           [0,5989, 0,8022],
           [0,7517, 0,7517]]
```

## Sequence length và số phần tử attention matrix

| T | Kích thước matrix | Số phần tử |
|---:|---:|---:|
| 10 | 10 × 10 | 100 |
| 100 | 100 × 100 | 10.000 |
| 500 | 500 × 500 | 250.000 |
| 1.000 | 1.000 × 1.000 | 1.000.000 |

Số phần tử tăng theo `T²`. Vì vậy sequence dài làm tăng bộ nhớ và phép tính của full self-attention nhanh hơn tuyến tính.
