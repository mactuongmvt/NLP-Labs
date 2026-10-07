# Reflection

## So sánh các representation

| Representation | Context-dependent? | Sparse/Dense | Một từ có nhiều vector? |
| --- | --- | --- | --- |
| TF-IDF | Không | Sparse | Không |
| Co-occurrence | Không | Sparse | Không |
| Word2Vec | Không | Dense | Không |
| Contextual embedding | Có | Dense | Có, tùy context |

## Tại sao `bank` cần contextual representation?

`bank` có thể là ngân hàng hoặc bờ sông. Word2Vec chỉ tạo một vector chung nên hai nghĩa bị trộn với nhau. Contextual embedding tạo vector dựa trên câu đang xét, vì vậy có thể biểu diễn hai nghĩa khác nhau.

## Kết luận

Co-occurrence và Word2Vec đều học từ context, nhưng Word2Vec tạo vector dense nhỏ hơn. Kết quả phụ thuộc nhiều vào corpus, window và dimension. Context dài hoặc vector lớn hơn không phải lúc nào cũng tốt hơn nếu dữ liệu không đủ.
