# Reflection

## So sánh các representation

| Representation | Context-dependent? | Sparse/Dense | Một từ có nhiều vector? |
| --- | --- | --- | --- |
| TF-IDF | Không | Sparse | Không |
| Co-occurrence | Không | Sparse | Không |
| Word2Vec | Không | Dense | Không |
| Contextual embedding | Có | Dense | Có, tùy context |

## Tại sao `bank` cần contextual representation?

`bank` có thể mang nghĩa “ngân hàng” trong ngữ cảnh tài chính hoặc “bờ sông” trong ngữ cảnh địa lý. Word2Vec chỉ học một vector duy nhất cho mỗi từ, nên vector của `bank` phải tổng hợp thông tin từ nhiều ngữ cảnh và không thể biểu diễn riêng từng nghĩa. Contextual embedding tạo vector dựa trên câu đang xét nên có thể phân biệt hai nghĩa này.

## Kết luận

Co-occurrence và Word2Vec đều học từ context, nhưng Word2Vec tạo vector dense nhỏ hơn. Kết quả phụ thuộc nhiều vào corpus, window và dimension. Context dài hoặc vector lớn hơn không phải lúc nào cũng tốt hơn nếu dữ liệu không đủ.
