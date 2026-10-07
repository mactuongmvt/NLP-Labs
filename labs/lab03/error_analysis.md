# Error Analysis

Phần này dùng model Word2Vec baseline với `vector_size = 100`, `window = 5` trên 10.000 documents đầu tiên của C4 30K.

## Ba trường hợp hợp lý

### 1. `doctor` – `physician`

- **Observed:** similarity = `0.700131`. `doctor` xuất hiện 263 lần và `physician` xuất hiện 86 lần.
- **Expected:** hai từ này nên có similarity khá cao vì nghĩa và cách sử dụng gần nhau.
- **Possible explanation:** `doctor` và `physician` xuất hiện trong nhiều context tương tự dù chúng không cần đứng cạnh nhau trực tiếp.
- **Evidence from corpus:** `physician` không nằm trực tiếp trong window 5 của `doctor`, nhưng hai từ có các context chung như `care`, `medical`, `health`, `may` và `who`.

### 2. `doctor` – `hospital`

- **Observed:** similarity = `0.524763`. `doctor` xuất hiện 263 lần và `hospital` xuất hiện 356 lần.
- **Expected:** hai từ nên có liên quan nhưng similarity thấp hơn `doctor–physician`.
- **Possible explanation:** `doctor` chỉ người còn `hospital` chỉ địa điểm, nhưng cả hai thường xuất hiện trong cùng chủ đề y tế.
- **Evidence from corpus:** `hospital` nằm trong window 5 của `doctor` 1 lần. Hai từ còn có các context chung như `care`, `health`, `visit` và `can`.

### 3. `cat` – `dog`

- **Observed:** similarity = `0.619464`. `cat` xuất hiện 218 lần và `dog` xuất hiện 428 lần.
- **Expected:** similarity tương đối cao vì cả hai đều là vật nuôi phổ biến.
- **Possible explanation:** `cat` và `dog` thường được dùng trong các câu có context giống nhau.
- **Evidence from corpus:** hai từ có các context chung như `my`, `food`, `can` và một số câu nói về vật nuôi. Chúng cũng xuất hiện trong window của nhau trong corpus.

## Ba trường hợp bất ngờ

### 4. `doctor` – `ophthalmologist`

- **Observed:** similarity = `0.733865`, cao hơn cả `doctor–physician`, mặc dù `ophthalmologist` chỉ xuất hiện 10 lần.
- **Expected:** tôi vẫn mong hai từ gần nhau vì `ophthalmologist` là một chuyên môn y tế, nhưng không nghĩ similarity lại cao hơn `doctor–physician`.
- **Possible explanation:** số lần xuất hiện của `ophthalmologist` khá ít và các lần xuất hiện đó tập trung vào những context giống với `doctor`, nên vector có thể bị ảnh hưởng mạnh bởi các context này.
- **Evidence from corpus:** `ophthalmologist` không nằm trực tiếp trong window 5 của `doctor`, nhưng hai từ có các context chung như `can`, `find`, `out` và `tell`.

### 5. `doctor` – `dentist`

- **Observed:** similarity = `0.726909`. `dentist` chỉ xuất hiện 49 lần nhưng similarity vẫn cao hơn `doctor–physician`.
- **Expected:** `dentist` nên gần `doctor`, nhưng tôi mong `physician` gần `doctor` hơn.
- **Possible explanation:** hai nghề này thường xuất hiện trong những câu có cách sử dụng tương tự, ví dụ nói về việc đi khám hoặc hỏi ý kiến chuyên môn.
- **Evidence from corpus:** `dentist` nằm trong window 5 của `doctor` 1 lần và có các context chung như `may`, `can`, `about` và `visit`.

### 6. `doctor` – `veterinarian`

- **Observed:** similarity = `0.721922`. `veterinarian` xuất hiện 20 lần và không nằm trực tiếp trong window 5 của `doctor`.
- **Expected:** hai từ có liên quan vì đều là nghề khám và điều trị, nhưng tôi không nghĩ similarity sẽ cao như vậy.
- **Possible explanation:** Word2Vec học từ cách sử dụng trong context. `doctor` và `veterinarian` có thể xuất hiện trong những mẫu câu tương tự dù một nghề điều trị người và một nghề điều trị động vật.
- **Evidence from corpus:** hai từ có các context chung như `visit`, `consult`, `call` và `being`.

## Kết luận

Các kết quả nhìn chung cho thấy Word2Vec đặt những từ có cách sử dụng tương tự ở gần nhau. Tuy nhiên, similarity còn phụ thuộc vào corpus, tần suất xuất hiện và context window. Vì vậy một số từ ít xuất hiện vẫn có thể có similarity cao nếu các context của chúng khá giống nhau.
