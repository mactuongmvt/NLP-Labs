# Reflection

## So sánh các representation

| Representation | Context-dependent? | Sparse/Dense | Một từ có nhiều vector? |
| --- | --- | --- | --- |
| TF-IDF | Không | Sparse | Không |
| Co-occurrence | Không | Sparse | Không |
| Word2Vec | Không | Dense | Không |
| Contextual embedding | Có | Dense | Có, tùy context |

## Tại sao `bank` cần contextual representation?

`bank` có thể có nghĩa là “ngân hàng” trong câu về tiền bạc, nhưng cũng có thể có nghĩa là “bờ sông” trong một câu khác.

Word2Vec chỉ tạo một vector cố định cho từ `bank`, nên hai nghĩa này vẫn dùng chung một representation. Contextual embedding tạo vector dựa trên câu hiện tại, vì vậy cùng một từ `bank` có thể có representation khác nhau khi context thay đổi.

## Kết luận

TF-IDF và co-occurrence là các representation sparse, còn Word2Vec tạo dense word vectors. Hạn chế của Word2Vec là mỗi từ chỉ có một vector cố định. Contextual embedding giải quyết tốt hơn trường hợp một từ có nhiều nghĩa phụ thuộc vào context.
