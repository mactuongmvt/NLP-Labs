# Data

Thư mục này dành cho dữ liệu dùng trong các bài thực hành.

Dataset không được lưu trực tiếp lên Git theo mặc định. Khi một lab sử dụng dữ liệu, hãy ghi tại đây hoặc trong README của lab:

- Tên và nguồn dữ liệu.
- Cách tải dữ liệu.
- Vị trí cần đặt dữ liệu sau khi tải.
- Cấu trúc tệp mong đợi.

## Lab 01 — C4 30K

- Tên file: `c4-train.00000-of-01024-30K.json.gz`
- Nguồn: tài nguyên do giảng viên chia sẻ trên Google Classroom.
- Định dạng: gzip chứa JSON Lines.
- Số documents: 30.000.
- Các trường: `text`, `timestamp`, `url`.
- Vị trí cục bộ: `data/raw/c4-train.00000-of-01024-30K.json.gz`.

Không giải nén và không đưa file dữ liệu này lên GitHub. Notebook đọc trực tiếp định dạng `.json.gz`.
