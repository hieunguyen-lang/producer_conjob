# FastAPI Cronjob Example

Đây là một ví dụ về ứng dụng FastAPI với chức năng cronjob sử dụng APScheduler.

## Cài đặt

1. Tạo môi trường ảo (khuyến nghị):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Cài đặt các dependencies:
```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
python main.py
```
Hoặc 
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

Ứng dụng sẽ chạy tại địa chỉ: http://localhost:8000

## API Endpoints

- `GET /`: Trang chủ
- `GET /jobs`: Liệt kê tất cả các cronjobs đang chạy

## Cronjobs

Ứng dụng có 2 cronjobs mẫu:
1. Chạy mỗi phút
2. Chạy mỗi giờ

Bạn có thể thêm hoặc sửa đổi các cronjobs trong file `main.py`.

## Tài liệu API

Sau khi chạy ứng dụng, bạn có thể truy cập tài liệu API tại:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 