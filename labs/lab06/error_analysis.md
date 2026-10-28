# Error Analysis

Phân tích dùng self-attention classifier trên test subset gồm 2.000 review. Model đạt accuracy `0,7275` và F1 `0,722646`.

## Ba prediction đúng

### 1. Negative → Negative

Review mở đầu bằng “I am definitely in the minority opinion…” và có các từ tiêu cực như `worst`. Model dự đoán negative với `P(positive) = 0,0317`. Review dài 159 token nên bị cắt ở giới hạn 100 token.

### 2. Positive → Positive

Review bắt đầu bằng “Great movie. I was laughing all time through.” Các từ `great` và `laughing` thể hiện phản hồi tích cực rõ. Model dự đoán positive với xác suất `0,7110`; review dài 84 token nên không bị cắt.

### 3. Negative → Negative

Review có cụm “a really bad movie” cùng các từ như `awful`. Model dự đoán negative với `P(positive) = 0,0164`. Review dài 274 token và bị cắt.

## Ba prediction sai

### 4. Positive → Negative

Review mở đầu “I did not intend to write this review…” và dài 565 token, nên chỉ 100 token đầu được đưa vào model. `P(positive) = 0,2537`. Câu mở đầu có từ phủ định, còn phần review dài có thể chứa đánh giá tích cực ở xa hơn. Đây có thể là trường hợp truncation và ngữ cảnh dài ảnh hưởng đến dự đoán.

Attention trung bình nhận được nhiều nhất ở `show`, `read`, `point`, `did`, `off`. Các token này chưa thể hiện rõ sentiment của toàn review.

### 5. Positive → Negative

Review bắt đầu bằng “This movie had an interesting cast…” nhưng model dự đoán negative với `P(positive) = 0,3784`. Review dài 157 token, vượt giới hạn 100. Cụm mở đầu khá trung tính và phần nội dung sau có thể bị cắt; đây là một giả thuyết cho lỗi, không thể kết luận chỉ từ attention.

Các token nhận attention trung bình cao nhất là `ordinary`, `job`, `im`, `they`, `they`. Những token này không thể hiện sentiment positive rõ ràng. Đây là một quan sát từ attention weights, chưa đủ để xác định nguyên nhân model dự đoán sai.

### 6. Negative → Positive

Review mở đầu bằng “Ed Gein, one of the most famous serial killers…” nhưng nhãn chung là negative. Model dự đoán positive với `P(positive) = 0,8495`; review dài 305 token và bị cắt. Phần mở đầu thiên về mô tả chủ đề hơn là bộc lộ sentiment, nên model có thể không nắm được đánh giá tổng thể trong phần văn bản còn lại.

Các token nhận attention trung bình cao nhất là `few`, `watched`, `most`, `most`, `all`. Phần lớn các token này không thể hiện trực tiếp sentiment negative. Tuy nhiên, không thể kết luận prediction sai là do model tập trung vào các token này.

## Confusion matrix

- 745 negative được dự đoán đúng; 255 negative bị dự đoán thành positive.
- 710 positive được dự đoán đúng; 290 positive bị dự đoán thành negative.

False negative nhiều hơn false positive 35 review. Trên các câu mẫu của application, model cũng dự đoán nhầm hai câu mang sentiment positive thành negative, trong khi dự đoán đúng câu “I do not like this movie.”

## Quan sát attention

Trong câu “The cat that I adopted yesterday is sleeping.”, query `cat` chú ý nhiều nhất đến `sleeping` (0,303), còn query `adopted` chú ý nhiều nhất đến `yesterday` (0,815). Đây là các pattern trong output của model, nhưng riêng chúng không chứng minh model hiểu quan hệ ngữ pháp hay đã reasoning.

## Kết luận

Trong ba prediction đúng, model nhận diện được các review có tín hiệu sentiment khá rõ trong phần văn bản được giữ lại.

Cả ba prediction sai đều là review dài hơn 100 tokens và bị truncation. Tuy nhiên, hai prediction đúng cũng bị truncation, nên không thể kết luận đây là nguyên nhân duy nhất khiến model sai.

Các attention weights cho thấy một số token nhận mức chú ý cao nhưng không mang sentiment rõ ràng. Đây chỉ là quan sát từ model, chưa đủ để chứng minh những token đó gây ra prediction sai.

Nhìn chung, model vẫn gặp khó với một số review dài hoặc có sentiment không rõ ở phần đầu. Cần phân biệt giữa kết quả quan sát được và giả thuyết về nguyên nhân lỗi.
