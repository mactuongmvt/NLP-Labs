# Error Analysis

Model phân tích: ALBERT fine-tuned trên 600 IMDb review, max length 64 tính cả special tokens. Nhãn 0 là negative, 1 là positive. Chỉ số test là vị trí trong tập con với seed 42.

## Bảng tổng hợp

| Nhóm | Test index | Text được giữ (trích) | True | Pred | Confidence | Error type | Hypothesis |
|---|---:|---|---:|---:|---:|---|---|
| FP | 1 | this film, by oscar petersson, is unique. its uniqueness doesn't lie in the story, since many a half… | 0 | 1 | 0.870291 | Sarcasm / context | Lời mở đầu và cách chê gián tiếp có thể làm model nhầm sentiment. |
| FP | 10 | this movie had good intentions and a good story to work with. the director and screenwriter of this … | 0 | 1 | 0.856027 | Contrast / context | Lời khen ý tưởng đi cùng phê bình cách thực hiện. |
| FP | 16 | i first didn't want to watch this film, for the trailer gave the impression of a common and too expe… | 0 | 1 | 0.889306 | Context / truncation | Đoạn khen phim khác được giữ lại, kết luận về phim đang review nằm phía sau. |
| FN | 4 | "nothin'. there ain't nothing' in room 237. but you ain't got no business going' in there anyway. so… | 1 | 0 | 0.826279 | Quoted dialogue / truncation | Lời thoại mở đầu chưa thể hiện đánh giá positive của review. |
| FN | 15 | i guess when "beat street" made a national appearance, "flashdance" came at the same time. the probl… | 1 | 0 | 0.859876 | Target context / truncation | Lời chê một phim khác xuất hiện trước lời khen phim được review. |
| FN | 44 | ....rather well done, actually--attack the evil villains in their lair, stop a little big horn style… | 1 | 0 | 0.830665 | Domain-specific expression / context | Từ ngữ kể nội dung hành động không đồng nghĩa sentiment negative. |
| Most confident wrong | 85 | this hodge-podge adapted from a gore vidal novel (actually one of the great american writers) makes … | 0 | 1 | 0.901781 | Sarcasm / mixed target / truncation | Lời khen tác giả hoặc diễn viên không phải lời khen bộ phim. |
| Most confident wrong | 100 | this is high grade cheese fare of b movie kung fu flicks. bruce "wannabe" lee is played by bruce li.… | 0 | 1 | 0.898037 | Sarcasm / truncation | Cách nói đùa và giễu nhại cần context để hiểu sentiment. |

## Ba false positives

### Test index 1 — 0 → 1

- Confidence: 0.870291; P(positive): 0.870291.
- Độ dài trước truncation: 251 token, tính cả special tokens; model nhận tối đa 64.
- Error type: Sarcasm / context.

> this film, by oscar petersson, is unique. its uniqueness doesn't lie in the story, since many a half brained hollywood production has served us comparably miserable plots, but rather in the thorough way that complete and utter lousiness in one aspect is joined with equal lousiness

Phần được giữ có `unique` nhưng cũng có `miserable plots` và `lousiness`. Người viết dùng cách giới thiệu tưởng như khen rồi chê bộ phim. Các dấu hiệu negative đã có trong input, nên không thể quy lỗi chỉ cho truncation. Model có thể chưa kết hợp được ý nghĩa của đoạn phê bình dài này.

### Test index 10 — 0 → 1

- Confidence: 0.856027; P(positive): 0.856027.
- Độ dài trước truncation: 251 token, tính cả special tokens; model nhận tối đa 64.
- Error type: Contrast / context.

> this movie had good intentions and a good story to work with. the director and screenwriter of this movie failed miserably and created a dull, boring filmstrip that made me feel like i was back in mr. hartford's 8th grade social studies class -- way back in 67.br

Input bắt đầu bằng `good intentions` và `a good story`, sau đó là `failed miserably`, `dull`, `boring`. Review phân biệt ý tưởng tốt với bộ phim được thực hiện kém. Model có thể chưa xử lý tốt hai ý trái chiều, nhưng chưa có ablation để xác định cụm nào gây ra prediction.

### Test index 16 — 0 → 1

- Confidence: 0.889306; P(positive): 0.889306.
- Độ dài trước truncation: 269 token, tính cả special tokens; model nhận tối đa 64.
- Error type: Context / truncation.

> i first didn't want to watch this film, for the trailer gave the impression of a common and too expected film...but as i recently had the pleasure to discover the surprising "mensonges et trahisons et plus si affinite"" which was beautifully directed and written by

Phần đầu nhắc một bộ phim khác được `beautifully directed and written`. Sau đó người viết nói bộ phim đang review không được như kỳ vọng, gồm `And it is absolutely not` và `lazy work`, nhưng các ý này nằm ngoài 64 token được giữ. Đây là bằng chứng về thông tin bị cắt; vẫn cần thử lại với input đầy đủ để kiểm tra giả thuyết về lỗi.

## Ba false negatives

### Test index 4 — 1 → 0

- Confidence: 0.826279; P(positive): 0.173721.
- Độ dài trước truncation: 356 token, tính cả special tokens; model nhận tối đa 64.
- Error type: Quoted dialogue / truncation.

> "nothin'. there ain't nothing' in room 237. but you ain't got no business going' in there anyway. so stay out. you understand? stay out." br /br /never has there been such a feat of

Input chủ yếu là lời thoại có `nothing` và `stay out`, rồi mới bắt đầu chuyển sang nhận xét. Các lời khen như `superb actor`, `greatest performances` và `10/10` nằm sau phần bị giữ lại. Không nên hiểu mọi từ phủ định trong lời thoại là người viết chê phim.

### Test index 15 — 1 → 0

- Confidence: 0.859876; P(positive): 0.140124.
- Độ dài trước truncation: 491 token, tính cả special tokens; model nhận tối đa 64.
- Error type: Target context / truncation.

> i guess when "beat street" made a national appearance, "flashdance" came at the same time. the problem with "flashdance" is that there was only one break dancing scene and the rest was jazz dance and ballet. that was one of the reasons why "beat street"

Phần được giữ nói về `the problem with Flashdance`, trong khi review đánh giá Beat Street tích cực hơn. Các câu `was better` và `I loved all of them` xuất hiện sau đoạn được giữ. Model có thể chưa nhận đúng đối tượng đang được đánh giá khi context bị cắt.

### Test index 44 — 1 → 0

- Confidence: 0.830665; P(positive): 0.169335.
- Độ dài trước truncation: 322 token, tính cả special tokens; model nhận tối đa 64.
- Error type: Domain-specific expression / context.

> ....rather well done, actually--attack the evil villains in their lair, stop a little big horn style ambush, save the day via the waterboys' bugling, works for me. stiff upper british lip and all that.br /br /so how

Input có lời khen `rather well done` và `works for me`, cùng các từ kể cốt truyện như `evil villains`, `ambush`. Model vẫn dự đoán negative dù tín hiệu positive có trong phần được giữ. Đây có thể là lỗi phân biệt nội dung phim với đánh giá của người viết; không có bằng chứng xác định riêng token nào gây lỗi.

## Hai prediction sai có confidence cao nhất

Hai mẫu dưới đây có confidence xấp xỉ 90%. Chỉ một mẫu đạt bin High (≥0.90); mẫu còn lại thuộc Medium. Giữ nguyên ngưỡng và xác suất thực tế.

### Test index 85 — 0 → 1

- Confidence: 0.901781; P(positive): 0.901781.
- Độ dài trước truncation: 235 token, tính cả special tokens; model nhận tối đa 64.
- Error type: Sarcasm / mixed target / truncation.

> this hodge-podge adapted from a gore vidal novel (actually one of the great american writers) makes the magic christian and valley of the dolls look like fellini art-works. raquel welch, with an incredible body (and she's actually not very tall) in a lead role (

Đoạn đầu có `great American writers`, `incredible body` khi nói về tác giả và diễn viên; cả review lại chê phim, kết thúc bằng `A 2 out of 10`. Cách so sánh và châm biếm cùng việc cắt phần sau có thể khiến sentiment chung khó nhận ra. Đây là giả thuyết dựa trên text, không phải kết luận về cơ chế model.

### Test index 100 — 0 → 1

- Confidence: 0.898037; P(positive): 0.898037.
- Độ dài trước truncation: 281 token, tính cả special tokens; model nhận tối đa 64.
- Error type: Sarcasm / truncation.

> this is high grade cheese fare of b movie kung fu flicks. bruce "wannabe" lee is played by bruce li...i think. of course, let's show quick clips of bruce and do closeups of his eyes and if you quint at the right angle during a certain

Input có `high grade cheese fare` và Bruce `wannabe` Lee. Review dùng giọng giễu nhại; những ý chê rõ hơn ở phần sau bị cắt. Model có thể đọc chưa đúng cách diễn đạt này. Confidence 0.8980 rất gần 0.90 nhưng vẫn thuộc bin Medium đã định trước, không đổi ngưỡng sau khi xem kết quả.

## Kết luận

Các mẫu trên cho thấy lỗi có thể liên quan đến sentiment trái chiều, lời thoại, đối tượng được đánh giá, giọng châm biếm và context bị cắt. Tất cả tám mẫu được chọn đều dài hơn budget 64 token, nhưng một số vẫn có dấu hiệu đúng ngay trong phần được giữ. Vì vậy truncation chưa được chứng minh là nguyên nhân duy nhất.

Error type và hypothesis là nhận xét từ text và output. Muốn kiểm tra nguyên nhân cần thí nghiệm thêm, chẳng hạn so sánh cùng mẫu với context đầy đủ. Không suy từ confidence cao sang việc model hiểu đúng review.

## 28. Câu hỏi bắt buộc

### Q1. Model nào hưởng lợi nhiều hơn khi training data ít?

ALBERT có F1 theo 10/25/50/100% là 10%: 0.6552, 25%: 0.6783, 50%: 0.6154, 100%: 0.7902; scratch là 10%: 0.6689, 25%: 0.2602, 50%: 0.6667, 100%: 0.5306. ALBERT có accuracy cao hơn ở cả bốn mức, nhưng không thể chỉ dựa vào F1 ở 10%: scratch gần như dự đoán toàn positive, accuracy chỉ 0.5050. Đường cong còn dao động và mỗi mức mới có một seed, nên chưa đủ kết luận chắc model nào giảm performance mạnh hơn nói chung.

### Q2. Nếu pretrained tốt hơn from-scratch, điều đó chứng minh điều gì?

Trong cấu hình này, ALBERT đạt F1 0.7902, cao hơn scratch 0.5306. Điều đó cho thấy pipeline pretrained hữu ích cho bài thử nghiệm này. Nó chưa chứng minh model hiểu ngôn ngữ như con người hay pretraining là nguyên nhân duy nhất, vì hai kiến trúc có kích thước khác nhau.

### Q3. Nếu frozen gần bằng fine-tuned, điều đó có ý nghĩa gì?

Điều đó gợi ý representation pretrained đã khá phù hợp với task và head đơn giản có thể tận dụng được. Ở lần chạy này frozen F1 = 0.6520, fine-tuned = 0.7902; phải xem mức chênh lệch thực tế, không mặc định hai chế độ tương đương.

### Q4. Nếu fine-tuning tốt hơn frozen rất nhiều, điều đó gợi ý điều gì?

Điều đó gợi ý việc điều chỉnh encoder cho dữ liệu downstream có ích. Chênh lệch F1 ở đây là 0.1382. Learning rate và cách tối ưu cũng khác nhau nên chưa tách được tác động riêng của từng yếu tố.

### Q5. Nếu performance giảm mạnh trên domain khác, nguyên nhân có thể là gì?

Từ vựng, cách thể hiện sentiment, độ dài, style hoặc phân phối nhãn có thể thay đổi. Thực tế IMDb F1 = 0.7902, Amazon F1 = 0.8285, nên không quan sát thấy suy giảm trên tập Amazon này. Cần phân biệt số quan sát với giả thuyết về nguyên nhân. Pretraining không đảm bảo không bị domain shift trên những tập khác.

### Q6. Nếu length tăng nhưng performance gần như không đổi còn time tăng mạnh, có nên tiếp tục tăng?

Không nên tăng chỉ vì muốn giữ thêm token. Cần cân nhắc mức cải thiện trên validation so với thời gian và memory. Chỉ số test được dùng để báo cáo, không chọn length bằng cách nhìn test rồi lấy cấu hình tốt nhất. Bảng length trong notebook ghi đầy đủ cả ba mức 64/128/256.
