-- Fix MySQL Authentication Plugin Error
-- Chạy script này trong MySQL Workbench hoặc MySQL Command Line

-- Thay đổi authentication plugin cho user root
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1111';
FLUSH PRIVILEGES;

-- Kiểm tra authentication plugin hiện tại
SELECT User, Host, plugin FROM mysql.user WHERE User = 'root';

-- Nếu bạn muốn tạo user mới riêng cho ứng dụng (khuyến nghị cho production)
-- CREATE USER 'khentuong_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_strong_password';
-- GRANT ALL PRIVILEGES ON khen_thuong_db.* TO 'khentuong_user'@'localhost';
-- FLUSH PRIVILEGES;

-- Sau khi chạy xong, cập nhật DATABASE_URL trong file .env nếu tạo user mới:
-- DATABASE_URL=mysql+pymysql://khentuong_user:your_strong_password@localhost:3306/khen_thuong_db
