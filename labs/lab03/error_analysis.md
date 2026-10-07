# Error Analysis

Phần này dùng model Word2Vec baseline (`vector_size = 100`, `window = 5`) trên corpus C4 10K.

## Ba trường hợp hợp lý

### 1. `doctor` – `physician`

- Similarity: `0,748929`
- Corpus count: `doctor = 263`, `physician = 86`
- Số lần `physician` nằm trực tiếp trong window 5 của `doctor`: 0

Hai từ không cần đứng cạnh nhau để có vector gần nhau. Chúng có nhiều context chung như `care`, `health` và `medical`, nên model học được cách dùng khá giống nhau.

### 2. `doctor` – `hospital`

- Similarity: `0,569727`
- Corpus count: `doctor = 263`, `hospital = 356`
- Số lần `hospital` nằm trong window 5 của `doctor`: 1

Hai từ cùng xuất hiện trong các context về `care` và `health`. Similarity thấp hơn cặp `doctor`–`physician` vì một từ chỉ người còn một từ chỉ địa điểm.

### 3. `cat` – `dog`

- Similarity: `0,594239`
- Corpus count: `cat = 218`, `dog = 428`

`cat` và `dog` thường xuất hiện trong các context giống nhau như `food`, `your`, `my` và các câu nói về vật nuôi. Vì vậy model đặt hai từ tương đối gần nhau.

## Ba trường hợp bất ngờ

### 4. `doctor` – `dentist`

- Similarity: `0,741220`
- Corpus count: `doctor = 263`, `dentist = 49`
- Số lần `dentist` nằm trong window 5 của `doctor`: 1

Similarity gần bằng cặp `doctor`–`physician` dù `dentist` ít xuất hiện hơn nhiều. Hai từ chia sẻ các context như `visit`, `your` và `you`, nên model nhấn mạnh cách dùng nghề nghiệp hơn sự khác nhau về chuyên môn.

### 5. `doctor` – `veterinarian`

- Similarity: `0,713972`
- Corpus count: `doctor = 263`, `veterinarian = 20`
- Số lần `veterinarian` nằm trong window 5 của `doctor`: 0

`veterinarian` không đứng gần `doctor` trong corpus nhưng vẫn có similarity cao. Các từ như `visit`, `consult`, `call` và `your` xuất hiện quanh cả hai, nên model xem chúng giống nhau dù một nghề điều trị người và một nghề điều trị động vật.

### 6. `doctor` – `ophthalmologist`

- Similarity: `0,702674`
- Corpus count: `doctor = 263`, `ophthalmologist = 10`
- Số lần `ophthalmologist` nằm trong window 5 của `doctor`: 0

`ophthalmologist` chỉ xuất hiện 10 lần nhưng vẫn được xếp gần `doctor`. Một số context chung như `find`, `tell`, `your` và `you` đủ làm vector gần nhau, nhưng count thấp khiến kết quả này kém chắc chắn.

## Kết luận

Các cặp hợp lý có context chung rõ ràng trong corpus. Những trường hợp bất ngờ cho thấy Word2Vec có thể đặt các nghề có cách dùng giống nhau rất gần nhau, ngay cả khi chúng hiếm hoặc không đứng cạnh nhau. Kết quả chịu ảnh hưởng của frequency, corpus và context window.
