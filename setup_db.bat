@echo off
chcp 65001 >nul
title Khởi tạo Database - Hệ thống Quản lý Khen thưởng

echo.
echo ========================================
echo   KHỞI TẠO DATABASE
echo   Hệ thống Quản lý Khen thưởng
echo ========================================
echo.

REM Kích hoạt môi trường ảo
if not exist "venv\Scripts\activate.bat" (
    echo [X] Lỗi: Chưa tìm thấy môi trường ảo
    echo [*] Vui lòng chạy run_app.bat trước
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Kiểm tra file .env
if not exist ".env" (
    echo [X] Lỗi: Chưa tìm thấy file .env
    echo [*] Vui lòng tạo file .env từ .env.example
    pause
    exit /b 1
)

REM Test kết nối MySQL
echo [*] Đang kiểm tra kết nối MySQL...
python test_connection.py

if errorlevel 1 (
    echo.
    echo [X] Lỗi kết nối MySQL!
    echo [*] Vui lòng xem file FIX_AUTH_ERROR.md để khắc phục
    echo.
    echo [*] Lỗi thường gặp: Authentication plugin
    echo [*] Giải pháp nhanh - Chạy lệnh SQL sau trong MySQL:
    echo.
    echo     ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
    echo     FLUSH PRIVILEGES;
    echo.
    pause
    exit /b 1
)

echo.

REM Chạy script khởi tạo
echo [*] Đang khởi tạo database...
echo [*] Tạo bảng và dữ liệu mẫu...
echo.

python init_db.py

if errorlevel 1 (
    echo.
    echo [X] Lỗi: Không thể khởi tạo database
    echo [*] Kiểm tra lại:
    echo     - MySQL đã chạy chưa?
    echo     - DATABASE_URL trong .env đã đúng chưa?
    echo     - Database đã tạo chưa?
    echo.
    pause
    exit /b 1
)

echo.
echo [✓] Khởi tạo database thành công!
echo.
echo Tài khoản đăng nhập:
echo   Admin: admin / admin123
echo   User:  user / user123
echo.
echo Bạn có thể chạy ứng dụng bằng: run_app.bat
echo.

pause
