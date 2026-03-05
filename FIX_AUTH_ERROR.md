# Khắc phục lỗi Authentication Plugin (MySQL/MariaDB)

## 🔴 Lỗi gặp phải

```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2059, "Authentication plugin 'auth_gssapi_client' not configured")
```

## 🎯 Nguyên nhân

- **MySQL 8.0+:** Sử dụng `caching_sha2_password` hoặc `auth_gssapi_client` mặc định
- **MariaDB 10.4+:** Có thể dùng `auth_gssapi_client` hoặc các plugin khác
- **PyMySQL:** Chỉ hỗ trợ `mysql_native_password`

➡️ **Cần chuyển về** `mysql_native_password` để tương thích với PyMySQL.

## ✅ Giải pháp

### 🔹 **Dành cho MARIADB** (ĐỀ XUẤT nếu bạn dùng MariaDB)

**Bước 1:** Mở MariaDB Command Line hoặc HeidiSQL/MySQL Workbench

**Bước 2:** Chạy lệnh SQL sau:

```sql
-- Đặt lại mật khẩu với mysql_native_password
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('1111');
FLUSH PRIVILEGES;
```

**Lưu ý:** Thay `'1111'` bằng mật khẩu root thực tế của bạn!

**Bước 3:** Kiểm tra:

```sql
SELECT User, Host, plugin FROM mysql.user WHERE User = 'root';
```

Kết quả phải hiển thị: `plugin = mysql_native_password` hoặc trống

**Bước 4:** Chạy lại ứng dụng:

```powershell
python test_connection.py
python init_db.py
```

**🎯 Script tự động:** Chạy file `fix_auth_mariadb.sql`

---

### 🔹 **Dành cho MYSQL 8.0+**

**Bước 1:** Mở MySQL Command Line hoặc MySQL Workbench

**Bước 2:** Chạy các lệnh SQL sau:

```sql
-- Thay đổi authentication method
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1111';
FLUSH PRIVILEGES;
```

**Lưu ý:** Thay `'1111'` bằng mật khẩu root thực tế của bạn!

**Bước 3:** Kiểm tra đã thay đổi thành công:

```sql
SELECT User, Host, plugin FROM mysql.user WHERE User = 'root';
```

Kết quả phải hiển thị: `plugin = mysql_native_password`

**Bước 4:** Chạy lại ứng dụng:

```powershell
python init_db.py
```

---

### **Cách 2: Tạo user mới riêng cho ứng dụng (PRODUCTION)**

**Bước 1:** Trong MySQL, chạy:

```sql
-- Tạo user mới
CREATE USER 'khentuong_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MatKhauManh@123';

-- Cấp quyền
GRANT ALL PRIVILEGES ON khen_thuong_db.* TO 'khentuong_user'@'localhost';
FLUSH PRIVILEGES;
```

**Bước 2:** Cập nhật file `.env`:

```env
DATABASE_URL=mysql+pymysql://khentuong_user:MatKhauManh@123@localhost:3306/khen_thuong_db
```

**Bước 3:** Chạy lại:

```powershell
python init_db.py
```

---

## 🔍 Kiểm tra kết nối

Sau khi fix, test kết nối bằng script Python:

```python
from sqlalchemy import create_engine

# Test connection
engine = create_engine("mysql+pymysql://root:1111@localhost:3306/khen_thuong_db")
with engine.connect() as conn:
    result = conn.execute("SELECT 1")
    print("✅ Kết nối thành công!")
```

---

## 🛠️ Các lỗi khác có thể gặp

### Lỗi: "Can't connect to MySQL server"
- ✅ Kiểm tra MySQL service đã chạy chưa
- ✅ Kiểm tra port 3306 có đang mở không

### Lỗi: "Access denied for user"
- ✅ Kiểm tra username/password trong `.env` file
- ✅ Đảm bảo user có quyền truy cập database

### Lỗi: "Unknown database 'khen_thuong_db'"
- ✅ Chạy: `CREATE DATABASE khen_thuong_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

---

## 📝 Lưu ý quan trọng

⚠️ **PyMySQL không hỗ trợ tham số `auth_plugin` trong connect_args!**

Giải pháp duy nhất là **phải thay đổi authentication method của MySQL user** bằng SQL command như đã hướng dẫn ở trên.

File `app/core/database.py` chỉ cấu hình `charset=utf8mb4` để đảm bảo hỗ trợ tiếng Việt đầy đủ.

---

## 📞 Hỗ trợ thêm

Nếu vẫn gặp lỗi, kiểm tra:
1. Phiên bản MySQL: `mysql --version`
2. Plugin hiện tại: `SELECT User, plugin FROM mysql.user;`
3. Connection string có đúng không

