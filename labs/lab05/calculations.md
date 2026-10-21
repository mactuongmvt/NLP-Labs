# Calculations — RNN và LSTM

## Bài 1 — Một bước RNN

Notebook dùng $x_t=[1,0]^T$, $h_{t-1}=[0.5,0.2]^T$,
$b_h=[0,0]^T$ và hai ma trận:

$$
W_{xh}=\begin{bmatrix}0.5&0.2\\0.1&0.4\end{bmatrix},\qquad
W_{hh}=\begin{bmatrix}0.3&0.1\\0.2&0.5\end{bmatrix}.
$$

Với $a_t=W_{xh}x_t+W_{hh}h_{t-1}+b_h$:

$$
W_{xh}x_t=\begin{bmatrix}0.5\\0.1\end{bmatrix},\qquad
W_{hh}h_{t-1}=\begin{bmatrix}0.3(0.5)+0.1(0.2)\\0.2(0.5)+0.5(0.2)\end{bmatrix}
=\begin{bmatrix}0.17\\0.20\end{bmatrix}.
$$

Vì vậy $a_t=[0.67,0.30]^T$.

$$
h_t=\tanh(a_t)
=
\begin{bmatrix}
\tanh(0.67)\\
\tanh(0.30)
\end{bmatrix}.
$$

Với:

$$
\tanh(x)=\frac{e^x-e^{-x}}{e^x+e^{-x}}.
$$

Phần tử thứ nhất:

$$
\tanh(0.67)
=
\frac{e^{0.67}-e^{-0.67}}
     {e^{0.67}+e^{-0.67}}.
$$

Vì:

$$
e^{0.67}\approx1.954,\qquad
e^{-0.67}\approx0.512,
$$

nên:

$$
\tanh(0.67)
\approx
\frac{1.954-0.512}{1.954+0.512}
=
\frac{1.442}{2.466}
\approx0.585.
$$

Tương tự:

$$
\tanh(0.30)
=
\frac{e^{0.30}-e^{-0.30}}
     {e^{0.30}+e^{-0.30}}.
$$

Vì:

$$
e^{0.30}\approx1.350,\qquad
e^{-0.30}\approx0.741,
$$

nên:

$$
\tanh(0.30)
\approx
\frac{1.350-0.741}{1.350+0.741}
=
\frac{0.609}{2.091}
\approx0.291.
$$

Do đó:

$$
h_t\approx
\begin{bmatrix}
0.585\\
0.291
\end{bmatrix}.
$$


## Bài 2 — Information flow

Với câu *I did not like this movie*, RNN đọc lần lượt từng token. Trạng thái sau
`not` có thể mang thông tin phủ định; khi đọc `like`, mô hình có thể kết hợp động
từ tích cực với phủ định trước đó, rồi truyền kết quả đến các token tiếp theo.
Điều này là khả năng của kiến trúc, không đảm bảo mô hình đã học được cách hiểu
phủ định trong mọi câu.

Average Word2Vec lấy trung bình các vector từ. Nó có thể chứa vector của `not`,
nhưng phép trung bình không giữ vị trí hay phạm vi tác động của từ phủ định. Do
đó nó khó phân biệt các câu có cùng từ nhưng trật tự và quan hệ cú pháp khác
nhau. Hidden state của RNN phụ thuộc vào trạng thái trước đó, nên có thể giữ
thông tin về thứ tự.

## Bài 3 — Sequence order

`dog bites man` và `man bites dog` có cùng ba từ. Average Word2Vec cho cùng
một vector trung bình vì phép cộng không phụ thuộc thứ tự. Với RNN, các bước cập
nhật hidden state khác nhau: từ đầu câu khác nhau làm thay đổi trạng thái trước
khi đọc `bites`, nên biểu diễn cuối câu có thể khác. Tuy nhiên, việc phân biệt
đúng ai cắn ai còn phụ thuộc dữ liệu huấn luyện và những gì mô hình học được.

## Vanishing gradient

Khi học từ một token ở xa, gradient phải đi ngược qua nhiều bước thời gian.
Mỗi bước nhân thêm Jacobian của phép cập nhật hidden state; với `tanh`, đạo hàm
có độ lớn tối đa 1 và thường nhỏ hơn 1. Tích của nhiều hệ số nhỏ dần về 0,
khiến RNN khó gán ảnh hưởng của token đầu câu cho dự đoán cuối câu. Nếu các
hệ số quá lớn, gradient cũng có thể bùng nổ.

LSTM có đường truyền cell state cùng các gate để giữ hoặc bỏ thông tin qua
nhiều bước, nên thường xử lý phụ thuộc dài tốt hơn Simple RNN. Gate chỉ giảm
khó khăn này, không bảo đảm mọi phụ thuộc dài đều được nhớ.

## LSTM gates và cell state

Forget gate $f_t$ điều chỉnh phần cell state cũ được giữ lại. Input gate $i_t$
điều chỉnh phần thông tin mới $\widetilde c_t$ được thêm vào cell state.

## Bài tập tính toán — LSTM gates

Cho:

$$
f_t=0.9,\qquad
i_t=0.2,\qquad
\widetilde c_t=0.5,\qquad
c_{t-1}=0.8.
$$

Cell state mới được tính bằng:

$$
c_t=f_tc_{t-1}+i_t\widetilde c_t.
$$

Thay số:

$$
c_t=0.9(0.8)+0.2(0.5).
$$

$$
c_t=0.72+0.10=0.82.
$$

Vậy:

$$
\boxed{c_t=0.82}
$$

Nếu forget gate gần 1, model có xu hướng giữ lại phần lớn thông tin từ cell state cũ.

Nếu forget gate gần 0, model có xu hướng loại bỏ phần lớn thông tin cũ.
