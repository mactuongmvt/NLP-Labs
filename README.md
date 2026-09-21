# Natural Language Processing Labs

Kho lưu trữ các bài thực hành môn **Xử lý ngôn ngữ tự nhiên**.

## Thông tin sinh viên

- Họ và tên: Mạc Văn Tường
- Mã sinh viên: 23001951
- Lớp học phần: MAT3561E 4

## Danh sách bài thực hành

| Bài thực hành | Nội dung | Trạng thái |
| --- | --- | --- |
| [Lab 01](labs/lab01/) | TF-IDF và Document Search | Đang thực hiện |

## Cấu trúc repository

```text
NLP-Labs/
├── labs/
│   └── lab01/
│       └── README.md
├── data/
│   └── README.md
├── .gitignore
├── README.md
└── requirements.txt
```

Mỗi thư mục lab sẽ có hướng dẫn riêng về yêu cầu, cách cài đặt, cách chạy và kết quả.

## Cài đặt

```bash
python -m venv .venv
```

Kích hoạt môi trường trên Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cài đặt thư viện sau khi `requirements.txt` được cập nhật:

```bash
pip install -r requirements.txt
```

## Quy ước

- Không đưa dataset hoặc model dung lượng lớn lên Git.
- Không đưa môi trường ảo, cache hay thông tin đăng nhập lên Git.
- Mỗi thay đổi hoàn chỉnh nên được lưu bằng một commit có nội dung rõ ràng.
