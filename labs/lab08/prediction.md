# Prediction trước experiment

## Prediction 1 — Pretrained và from scratch

**Prediction:** Một pretrained Transformer sau fine-tuning có khả năng đạt kết quả tốt hơn Transformer nhỏ được train từ đầu trên cùng dữ liệu IMDb.

**Reason:** Pretrained model đã học các đặc điểm ngôn ngữ từ lượng văn bản lớn. Khi chuyển sang bài toán mới, model có thể tận dụng những gì đã học, trong khi model train từ đầu phải học từ trọng số ngẫu nhiên.

**Expected evidence:** Pretrained model có accuracy và F1 cao hơn model train từ đầu khi được đánh giá trên cùng dữ liệu.

## Prediction 2 — Frozen và fine-tuning

**Prediction:** Chọn C: chỉ train classification head với frozen encoder có thể cho kết quả kém hơn fine-tuning toàn bộ model.

**Reason:** Khi encoder bị freeze, representation được giữ nguyên và chỉ head học cách phân loại. Fine-tuning toàn bộ cho phép điều chỉnh cả encoder để phù hợp hơn với bài toán mới.

**Expected evidence:** Fine-tuning toàn bộ có accuracy và F1 cao hơn chế độ frozen khi so sánh trên cùng dữ liệu.

## Prediction 3 — Lượng training data

**Prediction:** Khi chỉ còn 10% training data, model train từ đầu có thể giảm performance mạnh hơn pretrained model.

**Reason:** Khi dữ liệu ít, model train từ đầu có ít ví dụ để học cả representation và cách phân loại. Pretrained model đã có các đặc điểm ngôn ngữ từ pretraining nên có thể ít phụ thuộc hơn vào lượng dữ liệu của bài toán mới.

**Expected evidence:** Khi lượng training data giảm từ 100% xuống 50%, 25% và 10%, accuracy và F1 của model train từ đầu giảm mạnh hơn pretrained model. Đường cong kết quả ở các mức dữ liệu sẽ được dùng để kiểm tra dự đoán này.
