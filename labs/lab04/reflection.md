# Reflection

Kết quả thí nghiệm cho thấy representation ảnh hưởng rõ đến chất lượng classification. Trên dataset IMDb, TF-IDF đạt kết quả tốt hơn Average Word2Vec vì các từ và cụm từ mang sentiment có vai trò quan trọng. Khi thêm bigram, F1 được cải thiện nhưng vocabulary và thời gian train cũng tăng.

Accuracy không đủ để đánh giá toàn diện một model. Cần xem thêm precision, recall, F1 và confusion matrix. Các review dài, chứa nhiều ý trái chiều hoặc có nội dung không khớp rõ với label vẫn là những trường hợp khó đối với model.
