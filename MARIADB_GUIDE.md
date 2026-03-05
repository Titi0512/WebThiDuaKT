# Hướng dẫn sử dụng với MariaDB

## 📘 Giới thiệu

Hệ thống này được thiết kế để hoạt động với **MariaDB** - một fork mã nguồn mở của MySQL với nhiều cải tiến về hiệu năng và bảo mật.

### Tại sao chọn MariaDB?

- ✅ **Mã nguồn mở hoàn toàn** - Không có phiên bản commercial
- ✅ **Tương thích 100% với MySQL** - Dễ dàng migrate
- ✅ **Hiệu năng tốt hơn** - Tối ưu hóa query engine
- ✅ **Bảo mật cao hơn** - Vá lỗi nhanh hơn, nhiều tính năng bảo mật
- ✅ **Hỗ trợ tiếng Việt tốt** - UTF8MB4 mặc định

## 🔧 Cài đặt MariaDB

### Windows

1. **Tải MariaDB:**
   - Truy cập: https://mariadb.org/download/
   - Chọn phiên bản: MariaDB Server 10.11+ (LTS)
   - Tải: MSI Installer for Windows

2. **Cài đặt:**
   - Chạy file MSI vừa tải
   - Chọn "Custom" hoặc "Complete" installation
   - **QUAN TRỌNG:** Đặt mật khẩu root và nhớ nó!
   - Check vào "Use UTF8 as default server's character set"
   - Để mặc định port 3306

3. **Kiểm tra cài đặt:**
   ```powershell
   # Kiểm tra service
   Get-Service MySQL
   
   # Hoặc kiểm tra version
   mysql --version
   ```

### Linux (Ubuntu/Debian)

```bash
# Cài đặt MariaDB
sudo apt update
sudo apt install mariadb-server -y

# Chạy script bảo mật
sudo mysql_secure_installation

# Khởi động service
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

## 📦 Cấu hình cho ứng dụng

### 1. Tạo Database

Mở MariaDB Command Line hoặc HeidiSQL/MySQL Workbench:

```sql
-- Tạo database với UTF8MB4
CREATE DATABASE khen_thuong_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Kiểm tra
SHOW DATABASES;
```

### 2. Tạo User riêng (Khuyến nghị)

```sql
-- Tạo user cho ứng dụng
CREATE USER 'khentuong_app'@'localhost' IDENTIFIED BY 'MatKhauManh@2026';

-- Cấp quyền
GRANT ALL PRIVILEGES ON khen_thuong_db.* TO 'khentuong_app'@'localhost';
FLUSH PRIVILEGES;

-- Kiểm tra
SELECT User, Host FROM mysql.user WHERE User = 'khentuong_app';
```

### 3. Cấu hình trong .env

```env
# Nếu dùng user mới tạo (khuyến nghị)
DATABASE_URL=mysql+pymysql://khentuong_app:MatKhauManh@2026@localhost:3306/khen_thuong_db?charset=utf8mb4

# Hoặc dùng root (chỉ development)
DATABASE_URL=mysql+pymysql://root:your_root_password@localhost:3306/khen_thuong_db?charset=utf8mb4
```

## 🔐 Khắc phục lỗi Authentication Plugin

MariaDB có thể sử dụng các plugin xác thực mà PyMySQL không hỗ trợ.

### Lỗi: "Authentication plugin not configured"

**Giải pháp:**

```sql
-- Đặt lại mật khẩu với mysql_native_password
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('your_password');
FLUSH PRIVILEGES;

-- Kiểm tra plugin
SELECT User, Host, plugin FROM mysql.user WHERE User = 'root';
```

**Kết quả mong đợi:** `plugin = mysql_native_password`

### Script tự động

Chạy file SQL đã chuẩn bị:

```powershell
# Trong MariaDB command line
source fix_auth_mariadb.sql;

# Hoặc
mysql -u root -p < fix_auth_mariadb.sql
```

## 🎯 Khác biệt giữa MariaDB và MySQL

| Tính năng | MariaDB | MySQL |
|-----------|---------|-------|
| **Mã nguồn** | Hoàn toàn mở | Dual license |
| **Engine mặc định** | InnoDB, Aria | InnoDB |
| **Authentication** | mysql_native_password | caching_sha2_password |
| **JSON** | Hỗ trợ đầy đủ | Hỗ trợ đầy đủ |
| **Sequence** | Có | Không |
| **Window Functions** | Có (10.2+) | Có (8.0+) |

### Với ứng dụng này

- ✅ **PyMySQL driver** hoạt động tốt với cả hai
- ✅ **SQLAlchemy** tương thích hoàn toàn
- ✅ **Không cần thay đổi code** nếu dùng MariaDB thay vì MySQL
- ⚠️ **Chỉ khác cú pháp authentication** khi setup

## 🛠️ Tools quản lý MariaDB

### Giao diện đồ họa (GUI)

1. **HeidiSQL** (Windows - Miễn phí)
   - Download: https://www.heidisql.com/
   - Nhẹ, nhanh, dễ dùng
   - **KHUYẾN NGHỊ cho Windows**

2. **MySQL Workbench** (Cross-platform - Miễn phí)
   - Download: https://dev.mysql.com/downloads/workbench/
   - Tương thích hoàn toàn với MariaDB
   - Nhiều tính năng cao cấp

3. **DBeaver** (Cross-platform - Miễn phí)
   - Download: https://dbeaver.io/
   - Hỗ trợ nhiều loại database

### Command Line

```bash
# Đăng nhập
mysql -u root -p

# Chạy SQL file
mysql -u root -p khen_thuong_db < file.sql

# Backup database
mysqldump -u root -p khen_thuong_db > backup.sql

# Restore database
mysql -u root -p khen_thuong_db < backup.sql
```

## 🔍 Test kết nối

```powershell
# Chạy script test
python test_connection.py
```

Script sẽ tự động nhận diện MariaDB và hiển thị version.

**Kết quả thành công:**

```
✅ Kết nối MariaDB thành công!
📦 MariaDB version: 10.11.x-MariaDB
```

## 📊 Tối ưu hóa cho Production

### 1. Cấu hình MariaDB

File: `my.ini` (Windows) hoặc `/etc/mysql/mariadb.conf.d/50-server.cnf` (Linux)

```ini
[mysqld]
# Character set
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# Performance
max_connections = 200
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M

# Security
bind-address = 127.0.0.1
```

### 2. Backup tự động

**Windows (Task Scheduler):**

```batch
@echo off
set BACKUP_DIR=D:\Backups\MariaDB
set DATE=%date:~-4%%date:~3,2%%date:~0,2%
mysqldump -u khentuong_app -p"MatKhauManh@2026" khen_thuong_db > %BACKUP_DIR%\backup_%DATE%.sql
```

**Linux (Cron):**

```bash
# /etc/cron.daily/mariadb-backup.sh
#!/bin/bash
mysqldump -u khentuong_app -p'MatKhauManh@2026' khen_thuong_db > /backup/khentuong_$(date +\%Y\%m\%d).sql
```

## ❓ FAQ

**Q: PyMySQL có hoạt động với MariaDB không?**
A: Có! PyMySQL được thiết kế tương thích với cả MySQL và MariaDB.

**Q: Có cần thay đổi code khi dùng MariaDB?**
A: Không, code hoàn toàn tương thích. Chỉ khác cấu hình authentication.

**Q: Có nên dùng mariadb connector thay vì pymysql?**
A: PyMySQL ổn định hơn và được hỗ trợ rộng rãi. Chỉ dùng mariadb connector nếu cần tính năng đặc biệt.

**Q: MariaDB có nhanh hơn MySQL không?**
A: Trong hầu hết trường hợp, MariaDB có hiệu năng tốt hơn hoặc tương đương MySQL.

## 🔗 Tài liệu tham khảo

- MariaDB Official: https://mariadb.org/
- MariaDB Documentation: https://mariadb.com/kb/
- PyMySQL: https://pymysql.readthedocs.io/
- SQLAlchemy MariaDB: https://docs.sqlalchemy.org/en/20/dialects/mysql.html

---

**Lưu ý:** Tất cả các tài liệu đề cập đến "MySQL" trong project này đều áp dụng cho MariaDB do tính tương thích cao.
