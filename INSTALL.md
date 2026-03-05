# Hướng dẫn cài đặt nhanh

## Bước 1: Cài đặt môi trường

### Cài đặt Python
- Tải Python 3.9 hoặc mới hơn từ https://www.python.org/downloads/
- Trong quá trình cài đặt, check vào "Add Python to PATH"

### Cài đặt MariaDB
- Tải MariaDB từ https://mariadb.org/download/
- Cài đặt và nhớ mật khẩu root
- **Lưu ý:** MariaDB tương thích với MySQL, nên các lệnh SQL tương tự

## Bước 2: Tạo môi trường ảo Python

Mở PowerShell/CMD trong thư mục dự án:

```powershell
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
.\venv\Scripts\activate

# Nếu gặp lỗi về ExecutionPolicy, chạy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Bước 3: Cài đặt packages

```powershell
pip install -r requirements.txt
```

## Bước 4: Tạo database

Mở MariaDB Command Line hoặc MySQL Workbench (tương thích với MariaDB) và chạy:

```sql
CREATE DATABASE khen_thuong_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Bước 5: Cấu hình kết nối

Chỉnh sửa file `.env`:

```
DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost:3306/khen_thuong_db
```

Thay `YOUR_MYSQL_PASSWORD` bằng mật khẩu MySQL của bạn.

## Bước 6: Test kết nối MySQL (Quan trọng!)

```powershell
python test_connection.py
```

Nếu gặp lỗi authentication plugin, xem file `FIX_AUTH_ERROR.md` hoặc chạy SQL sau trong MySQL:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
```

## Bước 7: Khởi tạo database

```powershell
python init_db.py
```

Lệnh này sẽ:
- Tạo tất cả các bảng
- Thêm dữ liệu mẫu (đơn vị, danh hiệu, hình thức)
- Tạo 2 tài khoản: admin/admin123 và user/user123

## Bước 8: Chạy ứng dụng

```powershell
python main.py
```

Hoặc:

```powershell
uvicorn main:app --reload
```

## Bước 9: Truy cập ứng dụng

Mở trình duyệt và truy cập:
- Trang chủ: http://localhost:8000
- Đăng nhập: http://localhost:8000/login
- API Docs: http://localhost:8000/docs

## Tài khoản đăng nhập

**Admin (Toàn quyền):**
- Username: `admin`
- Password: `admin123`

**User (Người dùng thường):**
- Username: `user`
- Password: `user123`

## Khắc phục sự cố

### Lỗi kết nối MariaDB
- Kiểm tra MariaDB service đã chạy chưa
- Kiểm tra mật khẩu trong file `.env`
- Kiểm tra database đã tạo chưa
- **Lỗi authentication plugin:** Xem file `FIX_AUTH_ERROR.md` hoặc chạy:
  ```sql
  SET PASSWORD FOR 'root'@'localhost' = PASSWORD('your_password');
  FLUSH PRIVILEGES;
  ```

### Lỗi import module
```powershell
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Lỗi port 8000 đã được sử dụng
```powershell
# Chạy trên port khác
uvicorn main:app --reload --port 8001
```

### Reset database
```powershell
# Xóa và tạo lại database
DROP DATABASE khen_thuong_db;
CREATE DATABASE khen_thuong_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Chạy lại init
python init_db.py
```

## Chức năng chính

1. **Dashboard**: Xem tổng quan thống kê
2. **Hồ sơ khen thưởng**: Tạo, xem, sửa, xóa hồ sơ
3. **Danh mục**: Quản lý đơn vị, danh hiệu, hình thức
4. **Thống kê**: Xem báo cáo theo đơn vị, năm
5. **Quy trình**: Trình duyệt, phê duyệt, từ chối hồ sơ

## Ghi chú

- Sau khi hoàn thành, nhớ đổi SECRET_KEY trong file `.env`
- Trong môi trường production, đặt DEBUG=False
- Backup database định kỳ
- Đổi mật khẩu tài khoản admin ngay sau khi cài đặt
