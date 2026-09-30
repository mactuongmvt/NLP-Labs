# Dự đoán trước khi chạy thí nghiệm

Nội dung dưới đây được chép lại từ phần prediction trong [bản scan viết tay](./calculations%26prediction.pdf).

## Prediction 1

Khi chuyển từ unigram sang bigram rồi trigram thì vocabulary không tăng.

## Prediction 2

Khi tăng từ unigram sang bigram rồi trigram, số lượng n-gram sẽ tăng trên lượng corpus đủ lớn; không có quy luật cố định.

## Prediction 3

Trigram sẽ dễ gặp zero probability nhất vì mỗi tổ hợp chuỗi ba từ phải xuất hiện theo đúng thứ tự.

## Prediction 4

Theo tôi, trigram thường có training perplexity thấp hơn vì trigram có nhiều context hơn so với bigram và unigram.

## Prediction 5

Nếu corpus rất nhỏ, trigram không chắc chắn tốt hơn bigram vì trong corpus nhỏ thì trigram dễ gặp zero probability.
