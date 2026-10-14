# IMDb dataset

- Nguồn: Stanford Large Movie Review Dataset.
- URL: https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz
- Dữ liệu gốc có 50.000 review có nhãn: 25.000 negative và 25.000 positive.
- Có 418 document trùng lặp hoàn toàn và không có trường hợp trùng lặp xung đột nhãn.
- Sau khi loại duplicate còn 49.582 samples.
- Chia stratified với `random_state = 42`: train 60%, validation 20%, test 20%.

| File | Samples | Negative | Positive |
| --- | ---: | ---: | ---: |
| `imdb_train.csv.gz` | 29.749 | 14.819 | 14.930 |
| `imdb_validation.csv.gz` | 9.916 | 4.939 | 4.977 |
| `imdb_test.csv.gz` | 9.917 | 4.940 | 4.977 |

Mỗi file có hai cột: `text` và `label`, với `0 = negative`, `1 = positive`.
