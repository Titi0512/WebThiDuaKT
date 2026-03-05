@echo off
chcp 65001 >nul
title Khắc phục lỗi MySQL Authentication

echo.
echo ========================================
echo   KHẮC PHỤC LỖI AUTHENTICATION PLUGIN
echo ========================================
echo.
echo Lỗi: Authentication plugin 'auth_gssapi_client' not configured
echo.
echo ĐÂY LÀ CÁC LỆNH SQL BẠN CẦN CHẠY TRONG MYSQL:
echo.
echo ----------------------------------------
echo.
echo ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1111';
echo FLUSH PRIVILEGES;
echo SELECT User, Host, plugin FROM mysql.user WHERE User = 'root';
echo.
echo ----------------------------------------
echo.
echo 📝 HƯỚNG DẪN:
echo.
echo CÁCH 1: Dùng MySQL Command Line Client
echo   1. Tìm "MySQL 8.0 Command Line Client" trong Start Menu
echo   2. Nhấn Enter, nhập mật khẩu root của MySQL
echo   3. Copy và paste 3 lệnh SQL ở trên
echo   4. Nhấn Enter sau mỗi lệnh
echo   5. Nếu thấy "mysql_native_password" trong kết quả ^=^> THÀNH CÔNG!
echo.
echo CÁCH 2: Dùng MySQL Workbench
echo   1. Mở MySQL Workbench
echo   2. Kết nối vào localhost
echo   3. Mở SQL Editor (tab mới)
echo   4. Copy và paste 3 lệnh SQL ở trên
echo   5. Nhấn nút Execute (biểu tượng sét)
echo.
echo ⚠️  LƯU Ý:
echo   - Thay '1111' bằng MẬT KHẨU ROOT THỰC TẾ của bạn
echo   - Nếu password có ký tự đặc biệt, giữ nguyên trong dấu ngoặc đơn
echo.
echo ========================================
echo.
pause
echo.
echo [*] Bạn đã chạy xong lệnh SQL chưa? (Y/N)
set /p choice=Nhập Y nếu đã chạy xong: 

if /i "%choice%"=="Y" (
    echo.
    echo [*] Đang kiểm tra kết nối...
    
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
        python test_connection.py
        
        if errorlevel 1 (
            echo.
            echo [X] Vẫn còn lỗi! Vui lòng kiểm tra lại:
            echo     1. Đã chạy đúng 3 lệnh SQL chưa?
            echo     2. Password trong lệnh SQL có đúng không?
            echo     3. Kết quả SELECT có hiển thị "mysql_native_password" không?
            pause
            exit /b 1
        ) else (
            echo.
            echo [✓] THÀNH CÔNG! Bây giờ bạn có thể chạy:
            echo     python init_db.py
            echo     hoặc: setup_db.bat
            echo.
            pause
        )
    ) else (
        echo.
        echo [!] Chưa tìm thấy môi trường ảo
        echo [*] Vui lòng chạy: run_app.bat trước
        pause
    )
) else (
    echo.
    echo [*] Vui lòng chạy lệnh SQL trước, sau đó chạy lại file này
    pause
)
