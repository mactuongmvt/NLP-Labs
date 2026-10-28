# Prediction

## Prediction 1

**Prediction:** Key có dot product lớn nhất sẽ nhận attention weight lớn nhất.

**Reason:** Softmax bảo toàn thứ tự score; score lớn nhất có số mũ lớn nhất.

**Confidence:** Cao.

## Prediction 2

**Prediction:** Nếu mọi score bằng nhau thì các attention weight bằng nhau.

**Reason:** Các số mũ bằng nhau và softmax chuẩn hóa thành phân phối đều.

**Confidence:** Cao.

## Prediction 3

**Prediction:** Với scores `[1, 1, 10]`, attention sẽ tập trung phần lớn vào key thứ ba.

**Reason:** Chênh lệch score lớn làm số mũ của score 10 vượt xa hai score còn lại.

**Confidence:** Cao.

## Prediction 4

**Prediction:** Tăng sequence từ 10 lên 1.000 tokens làm số phần tử attention matrix tăng từ 100 lên 1.000.000.

**Reason:** Với full self-attention, attention matrix có kích thước `T × T`, nên số phần tử tăng theo `T²`. Khi sequence tăng từ 10 lên 1.000 tokens, số phần tử tăng từ 100 lên 1.000.000.

**Confidence:** Cao.

## Prediction 5

**Prediction:** Attention không phải lúc nào cũng tập trung vào token mà con người đánh giá là quan trọng.

**Reason:** Attention phụ thuộc vào query, key, value và các tham số đã học; heatmap chỉ thể hiện phân phối trọng số.

**Confidence:** Trung bình.
