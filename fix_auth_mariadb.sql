-- ============================================
-- KHẮC PHỤC LỖI AUTHENTICATION - MARIADB
-- Script dành riêng cho MariaDB
-- ============================================

-- Bước 1: Kiểm tra plugin hiện tại
SELECT User, Host, plugin 
FROM mysql.user 
WHERE User = 'root';

-- Bước 2: Đặt lại mật khẩu với mysql_native_password
-- ⚠️ THAY '1111' bằng mật khẩu root THỰC TẾ của bạn!
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('1111');

-- Bước 3: Làm mới quyền
FLUSH PRIVILEGES;

-- Bước 4: Kiểm tra lại
SELECT User, Host, plugin 
FROM mysql.user 
WHERE User = 'root';

-- ============================================
-- Nếu lệnh trên vẫn lỗi, thử cách này:
-- ============================================
-- UPDATE mysql.user SET plugin='mysql_native_password' WHERE User='root' AND Host='localhost';
-- SET PASSWORD FOR 'root'@'localhost' = PASSWORD('1111');
-- FLUSH PRIVILEGES;

-- ============================================
-- HOÀN THÀNH!
-- Sau đó chạy: python test_connection.py
-- ============================================
