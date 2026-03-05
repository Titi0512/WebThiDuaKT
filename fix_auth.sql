-- ============================================
-- KHẮC PHỤC LỖI AUTHENTICATION PLUGIN
-- Hỗ trợ cả MySQL và MariaDB
-- ============================================

-- Bước 1: Kiểm tra authentication plugin hiện tại
SELECT User, Host, plugin 
FROM mysql.user 
WHERE User = 'root';

-- ============================================
-- Bước 2: Chọn CÚ PHÁP PHÙ HỢP với database của bạn
-- ⚠️ QUAN TRỌNG: Thay '1111' bằng mật khẩu root THỰC TẾ!
-- ============================================

-- ============================================
-- CÁCH 1: Dành cho MARIADB (Chạy cái này nếu bạn dùng MariaDB)
-- ============================================
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('1111');
-- Hoặc nếu lệnh trên không được, thử:
-- ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING PASSWORD('1111');

-- ============================================
-- CÁCH 2: Dành cho MYSQL 8.0+ (Nếu lệnh trên lỗi, dùng cái này)
-- ============================================
-- ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1111';

-- Bước 3: Làm mới quyền
FLUSH PRIVILEGES;

-- Bước 4: Kiểm tra lại kết quả
SELECT User, Host, plugin 
FROM mysql.user 
WHERE User = 'root';

-- ============================================
-- HOÀN THÀNH!
-- Sau khi chạy xong, bạn có thể:
-- 1. Đóng MySQL
-- 2. Chạy: python test_connection.py (để kiểm tra)
-- 3. Chạy: python init_db.py (để khởi tạo database)
-- ============================================
