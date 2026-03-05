# Hệ thống quản lý khen thưởng - Trường Sĩ quan Chính trị

Hệ thống quản lý toàn diện các danh hiệu thi đua và hình thức khen thưởng tại Trường Sĩ quan Chính trị.

> **🔵 Database:** Hệ thống sử dụng **MariaDB** (tương thích với MySQL). Xem hướng dẫn chi tiết trong [MARIADB_GUIDE.md](MARIADB_GUIDE.md)

## Tính năng chính

### 1. Quản lý danh mục
- **Đơn vị**: Khối cơ quan, Các khoa, Đơn vị trực thuộc
- **Danh hiệu thi đua**: Quản lý các loại danh hiệu (cho phép thêm mới)
- **Hình thức khen thưởng**: Quản lý các hình thức khen thưởng (cho phép thêm mới)
- **Hồ sơ khen thưởng**: Quản lý hồ sơ cá nhân và tập thể

### 2. Quy trình xét duyệt
- Tạo đề nghị khen thưởng
- Kiểm tra thông tin
- Trình duyệt nhiều cấp
- Theo dõi trạng thái hồ sơ
- Lịch sử xử lý chi tiết

### 3. Tìm kiếm và tra cứu
- Tìm kiếm theo họ tên
- Lọc theo đơn vị
- Lọc theo năm
- Lọc theo hình thức khen thưởng
- Tra cứu đề xuất đạt chỉ tiêu

### 4. Báo cáo - Thống kê
- Báo cáo theo năm
- Báo cáo theo đơn vị
- Tổng hợp danh hiệu
- Xuất Word/PDF/Excel

### 5. Quản trị hệ thống
- Phân quyền người dùng (Admin, Lãnh đạo, Cán bộ, User)
- Nhật ký hoạt động
- Sao lưu dữ liệu

## Công nghệ sử dụng

### Backend
- **FastAPI**: Framework web hiện đại, nhanh
- **SQLAlchemy**: ORM cho Python
- **MariaDB**: Hệ quản trị cơ sở dữ liệu (MySQL-compatible)
- **JWT**: Authentication token-based
- **Pydantic**: Data validation

### Frontend
- **Bootstrap 5**: Framework CSS hiện đại
- **JavaScript (Vanilla)**: Logic frontend
- **Chart.js**: Biểu đồ thống kê
- **Axios**: HTTP client

## Cài đặt

### Yêu cầu hệ thống
- Python 3.9+
- MariaDB 10.5+ (hoặc MySQL 8.0+ - tương thích)
- pip (Python package manager)

### Các bước cài đặt

1. **Clone repository hoặc tải source code**

2. **Tạo môi trường ảo Python**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
# hoặc
source venv/bin/activate  # Linux/Mac
```

3. **Cài đặt các package cần thiết**
```bash
pip install -r requirements.txt
```

4. **Tạo database MariaDB**
```sql
CREATE DATABASE khen_thuong_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. **Cấu hình môi trường**
- Copy file `.env.example` thành `.env`
- Chỉnh sửa thông tin kết nối database trong file `.env`:
```
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/khen_thuong_db?charset=utf8mb4
SECRET_KEY=your-secret-key-here
```
**Lưu ý:** PyMySQL driver tương thích với MariaDB

6. **Test kết nối MariaDB**
```bash
python test_connection.py
```
⚠️ **Nếu gặp lỗi authentication plugin**, xem file `FIX_AUTH_ERROR.md`

7. **Khởi tạo database với dữ liệu mẫu**
```bash
python init_db.py
```

8. **Chạy ứng dụng**
```bash
python main.py
```

Hoặc sử dụng uvicorn trực tiếp:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

8. **Truy cập ứng dụng**
- Web UI: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## Tài khoản mặc định

Sau khi chạy `init_db.py`, hệ thống tạo sẵn 2 tài khoản:

- **Admin**: 
  - Username: `admin`
  - Password: `admin123`
  - Quyền: Quản trị viên (toàn quyền)

- **User**: 
  - Username: `user`
  - Password: `user123`
  - Quyền: Người dùng thường

## Cấu trúc thư mục

```
WebThiDuaKT/
├── app/
│   ├── api/              # API endpoints
│   │   ├── auth.py       # Authentication
│   │   ├── users.py      # User management
│   │   ├── don_vi.py     # Unit management
│   │   ├── danh_hieu.py  # Awards
│   │   ├── hinh_thuc.py  # Reward forms
│   │   ├── ho_so.py      # Records
│   │   └── thong_ke.py   # Statistics
│   │
│   ├── core/             # Core modules
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # Database setup
│   │   └── security.py   # Security functions
│   │
│   ├── models/           # Database models
│   │   └── models.py     # SQLAlchemy models
│   │
│   ├── schemas/          # Pydantic schemas
│   │   └── schemas.py    # Request/Response schemas
│   │
│   ├── static/           # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── app.js
│   │       ├── ho_so.js
│   │       └── thong_ke.js
│   │
│   └── templates/        # HTML templates
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── dashboard.html
│       ├── ho_so_list.html
│       ├── don_vi.html
│       ├── danh_muc.html
│       └── thong_ke.html
│
├── main.py               # Application entry point
├── init_db.py           # Database initialization
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - Đăng nhập
- `GET /api/auth/me` - Lấy thông tin user hiện tại

### Users
- `GET /api/users/` - Danh sách users
- `POST /api/users/` - Tạo user mới
- `GET /api/users/{id}` - Chi tiết user
- `PUT /api/users/{id}` - Cập nhật user
- `DELETE /api/users/{id}` - Xóa user

### Đơn vị
- `GET /api/don-vi/` - Danh sách đơn vị
- `POST /api/don-vi/` - Tạo đơn vị
- `PUT /api/don-vi/{id}` - Cập nhật đơn vị
- `DELETE /api/don-vi/{id}` - Xóa đơn vị

### Danh hiệu thi đua
- `GET /api/danh-hieu/` - Danh sách danh hiệu
- `POST /api/danh-hieu/` - Tạo danh hiệu
- `PUT /api/danh-hieu/{id}` - Cập nhật
- `DELETE /api/danh-hieu/{id}` - Xóa

### Hình thức khen thưởng
- `GET /api/hinh-thuc/` - Danh sách hình thức
- `POST /api/hinh-thuc/` - Tạo hình thức
- `PUT /api/hinh-thuc/{id}` - Cập nhật
- `DELETE /api/hinh-thuc/{id}` - Xóa

### Hồ sơ khen thưởng
- `GET /api/ho-so/` - Danh sách hồ sơ (có filter)
- `POST /api/ho-so/` - Tạo hồ sơ
- `GET /api/ho-so/{id}` - Chi tiết hồ sơ
- `PUT /api/ho-so/{id}` - Cập nhật hồ sơ
- `DELETE /api/ho-so/{id}` - Xóa hồ sơ
- `POST /api/ho-so/{id}/trinh-duyet` - Trình duyệt
- `POST /api/ho-so/{id}/phe-duyet` - Phê duyệt
- `POST /api/ho-so/{id}/tu-choi` - Từ chối
- `GET /api/ho-so/{id}/lich-su` - Lịch sử xử lý

### Thống kê
- `GET /api/thong-ke/tong-quat` - Thống kê tổng quát
- `GET /api/thong-ke/theo-don-vi` - Thống kê theo đơn vị
- `GET /api/thong-ke/theo-nam` - Thống kê theo năm
- `GET /api/thong-ke/dashboard` - Dashboard statistics

## Phân quyền

### Admin (Quản trị viên)
- Toàn quyền trên hệ thống
- Quản lý users, đơn vị, danh mục
- Xem, duyệt, xóa mọi hồ sơ

### Lãnh đạo
- Xem tất cả hồ sơ
- Phê duyệt/từ chối hồ sơ
- Xem báo cáo thống kê

### Cán bộ
- Quản lý danh mục (danh hiệu, hình thức)
- Tạo, sửa hồ sơ của đơn vị
- Xem thống kê đơn vị

### User (Người dùng)
- Tạo hồ sơ cho bản thân/đơn vị
- Xem hồ sơ đã tạo
- Xem thống kê đơn vị

## Bảo mật

- Authentication: JWT (JSON Web Token)
- Password hashing: Bcrypt
- CORS protection
- SQL Injection protection (SQLAlchemy ORM)
- XSS protection (Template escaping)

## Hỗ trợ

Nếu có vấn đề hoặc câu hỏi, vui lòng liên hệ quản trị viên hệ thống.

## License

Copyright © 2026 Trường Sĩ quan Chính trị
