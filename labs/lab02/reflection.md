# Reflection

## Câu 1 — Khi tăng n, mô hình nhận thêm thông tin gì?

Khi tăng n thì mô hình sẽ sử dụng nhiều từ đứng trước hơn để dự đoán từ tiếp theo. Unigram không dùng từ trước, bigram dùng 1 từ trước và trigram dùng 2 từ trước.

## Câu 2 — Tại sao tăng n làm sparsity tăng?

Vì khi n tăng thì các n-gram trở nên cụ thể hơn và có nhiều tổ hợp khác nhau hơn. Trong khi corpus có giới hạn nên nhiều bigram, đặc biệt là trigram chỉ xuất hiện rất ít lần hoặc không xuất hiện.

## Câu 3 — Tại sao smoothing cần thiết?

Nếu dùng MLE thì một n-gram chưa từng xuất hiện sẽ có xác suất bằng 0. Chỉ cần một xác suất bằng 0 thì xác suất của cả câu cũng bằng 0 và perplexity có thể thành vô hạn. Smoothing giúp các trường hợp chưa thấy vẫn có xác suất lớn hơn 0.

## Câu 4 — Perplexity đo điều gì?

Perplexity cho biết mức độ “bối rối” của mô hình khi dự đoán dữ liệu. Perplexity càng thấp thì nhìn chung mô hình càng dự đoán tốt trên tập dữ liệu đó.

## Câu 5 — Perplexity thấp hơn có luôn tạo văn bản tốt hơn với con người không?

Không. Perplexity thấp chỉ cho thấy mô hình dự đoán các từ trong dữ liệu tốt hơn. Nó không đảm bảo câu được tạo ra sẽ tự nhiên, có ý nghĩa hoặc tốt hơn đối với con người.

## Câu 6 — N-gram thất bại ở đâu so với cách con người hiểu ngôn ngữ?

N-gram chủ yếu dựa vào các từ xuất hiện gần nhau trong corpus. Nó không thực sự hiểu nghĩa của câu và cũng không sử dụng tốt những thông tin ở xa trong câu như con người.

## Câu 7 — Nếu context dài 100 từ, trigram có dùng được thông tin của 97 từ đầu không?

Không. Trigram chỉ sử dụng 2 từ gần nhất để dự đoán từ tiếp theo nên 97 từ phía trước sẽ không được sử dụng.

## Đối chiếu prediction ban đầu

Kết quả nhìn chung giống với dự đoán ban đầu của tôi. Khi tăng từ unigram lên bigram và trigram, số n-gram khác nhau tăng và trigram gặp nhiều trường hợp chưa xuất hiện hơn. Trên training set, MLE có perplexity giảm khi tăng n, nhưng trên validation/test thì bigram và trigram có thể gặp zero probability. Khi dùng Laplace, perplexity hữu hạn nhưng trigram vẫn không tốt hơn do dữ liệu bị sparse. Vì vậy context dài hơn không phải lúc nào cũng tốt hơn nếu corpus không đủ lớn.
