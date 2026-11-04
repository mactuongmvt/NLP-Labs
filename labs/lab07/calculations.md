# Calculations

## 6. Một attention head

Theo kích thước được điều chỉnh trên lớp, dùng $X\in\mathbb{R}^{3\times5}$ và $d_k=2$. Các ma trận dưới đây theo bài viết tay.

$$
X=\begin{bmatrix}
0&1&0&0&0\\
1&0&0&0&0\\
0&0&0&0&1
\end{bmatrix}.
$$

$$
W_Q=\begin{bmatrix}1&0\\0&0\\0&1\\0&0\\1&0\end{bmatrix},\quad
W_K=\begin{bmatrix}1&1\\1&1\\0&0\\1&0\\0&1\end{bmatrix},\quad
W_V=\begin{bmatrix}1&1\\0&0\\0&0\\1&1\\0&1\end{bmatrix}.
$$

**Bước 1: Tính Q, K, V**

Các hàng của X lần lượt chọn hàng 2, hàng 1 và hàng 5 của mỗi ma trận W:

$$
Q=XW_Q=\begin{bmatrix}0&0\\1&0\\1&0\end{bmatrix},\quad
K=XW_K=\begin{bmatrix}1&1\\1&1\\0&1\end{bmatrix},\quad
V=XW_V=\begin{bmatrix}0&0\\1&1\\0&1\end{bmatrix}.
$$

Cả Q, K và V đều có kích thước $3\times2$.

**Bước 2: Tính attention scores**

$$
S=\frac{QK^T}{\sqrt{2}}
=\frac{1}{\sqrt{2}}
\begin{bmatrix}0&0\\1&0\\1&0\end{bmatrix}
\begin{bmatrix}1&1&0\\1&1&1\end{bmatrix}
=\begin{bmatrix}
0&0&0\\
1/\sqrt{2}&1/\sqrt{2}&0\\
1/\sqrt{2}&1/\sqrt{2}&0
\end{bmatrix}.
$$

**Bước 3: Softmax theo từng hàng**

Hàng đầu có ba score bằng 0 nên mỗi weight bằng $1/3$.

Với hàng thứ hai và thứ ba:

$$
D=2e^{1/\sqrt{2}}+e^0\approx5.0562,
$$

$$
a=\frac{e^{1/\sqrt{2}}}{D}\approx0.4011,\qquad
b=\frac{1}{D}\approx0.1978.
$$

Vậy:

$$
A=\operatorname{softmax}(S)\approx
\begin{bmatrix}
1/3&1/3&1/3\\
0.4011&0.4011&0.1978\\
0.4011&0.4011&0.1978
\end{bmatrix}.
$$

**Bước 4: Tính context Z**

$$
Z=AV\approx
\begin{bmatrix}
1/3&1/3&1/3\\
0.4011&0.4011&0.1978\\
0.4011&0.4011&0.1978
\end{bmatrix}
\begin{bmatrix}0&0\\1&1\\0&1\end{bmatrix}
=\begin{bmatrix}
1/3&2/3\\
0.4011&0.5989\\
0.4011&0.5989
\end{bmatrix}.
$$

Kết quả Z có kích thước $3\times2$.

## 7. Multi-head

Ví dụ minh họa với các ma trận tự chọn, không phải số liệu được cho trong đề. Với $T=3$, giả sử output của hai head là:

$$
head_1=\begin{bmatrix}1&0\\0&1\\1&1\end{bmatrix},\quad
head_2=\begin{bmatrix}0&1\\1&0\\2&1\end{bmatrix}.
$$

Mỗi head có kích thước $3\times2$.

**Bước 1: Ghép theo chiều feature**

$$
H=\operatorname{Concat}(head_1,head_2)
=\begin{bmatrix}
1&0&0&1\\
0&1&1&0\\
1&1&2&1
\end{bmatrix}\in\mathbb{R}^{3\times4}.
$$

**Bước 2: Nhân output projection**

Để đưa kết quả về 5 chiều như X ở phần 6, chọn $W_O\in\mathbb{R}^{4\times5}$:

$$
W_O=\begin{bmatrix}
1&0&0&0&1\\
0&1&0&0&1\\
0&0&1&0&1\\
0&0&0&1&1
\end{bmatrix}.
$$

$$
Y=HW_O,\qquad (3\times4)(4\times5)=3\times5.
$$

Với một hàng $[h_1,h_2,h_3,h_4]$, phép nhân với $W_O$ cho:

$$
[h_1,h_2,h_3,h_4]W_O
=[h_1,h_2,h_3,h_4,h_1+h_2+h_3+h_4].
$$

Tính từng hàng:

$$
[1,0,0,1]W_O=[1,0,0,1,2],
$$

$$
[0,1,1,0]W_O=[0,1,1,0,2],
$$

$$
[1,1,2,1]W_O=[1,1,2,1,5].
$$

Vậy:

$$
\boxed{Y=\begin{bmatrix}
1&0&0&1&2\\
0&1&1&0&2\\
1&1&2&1&5
\end{bmatrix}}.
$$

Output có kích thước $3\times5$, cùng kích thước với X ở phần 6.

Cần concatenation để giữ riêng các feature của từng head trước khi $W_O$ trộn chúng. Nếu cộng hai head ngay, các feature cùng vị trí bị gộp lại và không còn được giữ riêng.

## 10. Positional encoding

Theo bài viết tay, dùng $d=5$ và ma trận X ở phần 6, với ba vị trí $pos=0,1,2$.

**Bước 1: Công thức**

$$
PE(pos,2i)=\sin\left(\frac{pos}{10000^{2i/5}}\right),\qquad
PE(pos,2i+1)=\cos\left(\frac{pos}{10000^{2i/5}}\right).
$$

Chỉ lấy các chiều từ 0 đến 4. Các mẫu số là:

$$
10000^{0/5}=1,\quad
10000^{2/5}\approx39.8107,\quad
10000^{4/5}\approx1584.8932.
$$

Vậy:

$$
PE(pos)=\left[
\sin(pos),\ \cos(pos),\
\sin\left(\frac{pos}{39.8107}\right),\
\cos\left(\frac{pos}{39.8107}\right),\
\sin\left(\frac{pos}{1584.8932}\right)
\right].
$$

**Bước 2: Tính ma trận PE**

$$
PE\approx\begin{bmatrix}
0&1&0&1&0\\
0.841471&0.540302&0.025116&0.999685&0.000631\\
0.909297&-0.416147&0.050217&0.998738&0.001262
\end{bmatrix}.
$$

**Bước 3: Cộng vào embedding**

$$
X'=X+PE
\approx\begin{bmatrix}
0&2&0&1&0\\
1.841471&0.540302&0.025116&0.999685&0.000631\\
0.909297&-0.416147&0.050217&0.998738&1.001262
\end{bmatrix}.
$$

Mỗi vị trí có một vector PE khác nhau. Khi cộng PE vào X, cùng một token ở hai vị trí có thể nhận input khác nhau.

## 14. Feed-forward network

Cho x = [1,2]ᵀ, W1 = I và b1 = [0,-1]ᵀ:

$$
W_1x+b_1=
\begin{bmatrix}1\\2\end{bmatrix}+
\begin{bmatrix}0\\-1\end{bmatrix}=
\begin{bmatrix}1\\1\end{bmatrix}.
$$

$$
h=ReLU([1,1]^T)=[1,1]^T.
$$

Đề không cho W2, b2, nên kết quả sau cùng là y = W2[1,1]ᵀ + b2. Nếu W2 = [[a,b],[c,d]] và b2 = [u,v]ᵀ, thì y = [a+b+u,c+d+v]ᵀ.

FFN biến đổi phi tuyến representation ở từng vị trí, không tính tương tác giữa các token như attention.

## 18. Kiểm tra shape

Với B = 8, T = 100, d_model = 128, n_heads = 4, ta có dk = 32.

| Tensor | Shape |
|---|---|
| X | 8 × 100 × 128 |
| Q/K/V trước tách head | 8 × 100 × 128 |
| Q/K/V sau tách head | 8 × 4 × 100 × 32 |
| Attention scores/weights | 8 × 4 × 100 × 100 |
| Context từng head | 8 × 4 × 100 × 32 |
| Ghép heads và output projection | 8 × 100 × 128 |
| Residual + LayerNorm | 8 × 100 × 128 |
| FFN hidden, chọn d_ff = 256 | 8 × 100 × 256 |
| FFN output | 8 × 100 × 128 |
| Block output | 8 × 100 × 128 |

## 19. Số head và dimension

| Heads | d_model | dk |
|---:|---:|---:|
| 1 | 128 | 128 |
| 2 | 128 | 64 |
| 4 | 128 | 32 |
| 8 | 128 | 16 |

Giữ d_model cố định thì tăng số head làm dk giảm. Tổng dimension sau concatenation vẫn bằng 128.

## 22. Sequence length

| T | T² |
|---:|---:|
| 32 | 1.024 |
| 64 | 4.096 |
| 128 | 16.384 |
| 256 | 65.536 |

Từ 128 lên 256 token, attention matrix có số phần tử lớn gấp 4. Đây là số phần tử của một head và một sequence, chưa tính batch, nhiều head hay bộ nhớ phục vụ backpropagation.
