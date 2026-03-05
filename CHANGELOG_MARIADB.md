# Cập nhật: Hỗ trợ MariaDB

## 📌 Tổng quan thay đổi

Hệ thống đã được cập nhật để **chính thức hỗ trợ MariaDB** thay vì MySQL. MariaDB là fork mã nguồn mở của MySQL với nhiều cải tiến về hiệu năng và bảo mật.

## ✅ Các file đã cập nhật

### Cấu hình
- ✅ `app/core/config.py` - Thêm ghi chú về MariaDB, charset=utf8mb4
- ✅ `app/core/database.py` - Cấu hình charset cho MariaDB
- ✅ `.env` - Thêm charset vào DATABASE_URL
- ✅ `.env.example` - Cập nhật format với charset
- ✅ `requirements.txt` - Thêm ghi chú về MariaDB connector

### Documentation
- ✅ `README.md` - Thay MySQL → MariaDB trong toàn bộ tài liệu
- ✅ `INSTALL.md` - Hướng dẫn cài đặt MariaDB
- ✅ `FIX_AUTH_ERROR.md` - Thêm hướng dẫn cho MariaDB
- ✅ `MARIADB_GUIDE.md` - **MỚI**: Hướng dẫn chi tiết về MariaDB

### Scripts
- ✅ `test_connection.py` - Tự động nhận diện MariaDB/MySQL
- ✅ `fix_auth_mariadb.sql` - **MỚI**: Script fix authentication cho MariaDB
- ✅ `fix_auth.sql` - Cập nhật hỗ trợ cả MariaDB và MySQL

## 🔄 Migration từ MySQL sang MariaDB

### Nếu bạn đang dùng MySQL

**Không cần làm gì!** Code vẫn tương thích hoàn toàn với MySQL 8.0+.

### Nếu muốn chuyển sang MariaDB

1. **Cài đặt MariaDB:**
   ```
   Download: https://mariadb.org/download/
   ```

2. **Export data từ MySQL:**
   ```bash
   mysqldump -u root -p khen_thuong_db > backup.sql
   ```

3. **Import vào MariaDB:**
   ```bash
   # Tạo database trong MariaDB
   CREATE DATABASE khen_thuong_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   # Import data
   mysql -u root -p khen_thuong_db < backup.sql
   ```

4. **Cập nhật .env** (nếu cần thay đổi password/user)

## 🆕 Tính năng mới

### 1. Auto-detect Database Type

File `test_connection.py` giờ tự động nhận diện MariaDB hoặc MySQL:

```
✅ Kết nối MariaDB thành công!
📦 MariaDB version: 10.11.6-MariaDB
```

### 2. MariaDB-specific SQL Scripts

- `fix_auth_mariadb.sql` - Fix authentication cho MariaDB
- Cú pháp đúng cho MariaDB (khác với MySQL)

### 3. Comprehensive MariaDB Guide

File mới `MARIADB_GUIDE.md` bao gồm:
- Hướng dẫn cài đặt chi tiết
- So sánh MariaDB vs MySQL
- Tối ưu hóa cho production
- Tools quản lý MariaDB
- FAQ

## 🔧 Khắc phục lỗi Authentication

### MariaDB (Cú pháp đặc biệt)

```sql
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('your_password');
FLUSH PRIVILEGES;
```

### MySQL 8.0+

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
```

**Chạy script tự động:**
- MariaDB: `fix_auth_mariadb.sql`
- MySQL: `fix_auth.sql`

## 📋 Checklist sau khi cập nhật

- [ ] Pull code mới nhất từ repository
- [ ] Cài đặt/cập nhật MariaDB (nếu chưa có)
- [ ] Chạy `python test_connection.py` để kiểm tra kết nối
- [ ] Nếu lỗi authentication → Chạy `fix_auth_mariadb.sql`
- [ ] Chạy `python init_db.py` để khởi tạo database
- [ ] Đọc `MARIADB_GUIDE.md` để tìm hiểu thêm

## 📖 Tài liệu tham khảo

### Đọc trước khi bắt đầu
1. **MARIADB_GUIDE.md** - Hướng dẫn toàn diện về MariaDB
2. **INSTALL.md** - Hướng dẫn cài đặt cập nhật
3. **FIX_AUTH_ERROR.md** - Khắc phục lỗi authentication

### Nếu gặp vấn đề
- Lỗi kết nối → `FIX_AUTH_ERROR.md`
- Không biết dùng MariaDB hay MySQL → Đọc so sánh trong `MARIADB_GUIDE.md`
- Muốn tối ưu hóa → Phần "Tối ưu hóa cho Production" trong `MARIADB_GUIDE.md`

## 🎯 Lợi ích khi dùng MariaDB

✅ **Miễn phí 100%** - Không có phiên bản commercial  
✅ **Hiệu năng cao hơn** - Query engine được tối ưu  
✅ **Bảo mật tốt hơn** - Vá lỗi nhanh hơn MySQL  
✅ **Hỗ trợ UTF8MB4 mặc định** - Hoàn hảo cho tiếng Việt  
✅ **Tương thích 100% MySQL** - Dễ dàng migrate  

## 💡 Lưu ý quan trọng

1. **PyMySQL driver tương thích với cả hai:**
   - Không cần cài driver riêng cho MariaDB
   - Connection string giống nhau: `mysql+pymysql://...`

2. **Cú pháp SQL hầu hết giống nhau:**
   - Chỉ khác một số lệnh quản trị (như SET PASSWORD)
   - Application code không cần thay đổi gì

3. **Authentication plugin:**
   - MariaDB: Dùng `SET PASSWORD` hoặc `PASSWORD()` function
   - MySQL 8.0+: Dùng `ALTER USER ... IDENTIFIED WITH ... BY`

## 🚀 Quick Start (MariaDB)

```bash
# 1. Test kết nối
python test_connection.py

# 2. Nếu lỗi authentication, fix ngay:
# Mở MariaDB Command Line và chạy:
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('your_password');
FLUSH PRIVILEGES;

# 3. Khởi tạo database
python init_db.py

# 4. Chạy ứng dụng
python main.py
```

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra MariaDB service đã chạy chưa
2. Test kết nối: `python test_connection.py`
3. Đọc error message và tìm trong `FIX_AUTH_ERROR.md`
4. Tham khảo `MARIADB_GUIDE.md` phần FAQ

---

**Ngày cập nhật:** 5/3/2026  
**Phiên bản:** 1.0.0  
**Người thực hiện:** GitHub Copilot
