@echo off
chcp 65001 >nul
title Hệ thống Quản lý Khen thưởng

echo.
echo ========================================
echo   HỆ THỐNG QUẢN LÝ KHEN THƯỞNG
echo   Trường Sĩ quan Chính trị
echo ========================================
echo.

REM Kiểm tra môi trường ảo
if not exist "venv\Scripts\activate.bat" (
    echo [!] Chưa tìm thấy môi trường ảo Python
    echo [*] Đang tạo môi trường ảo...
    python -m venv venv
    if errorlevel 1 (
        echo [X] Lỗi: Không thể tạo môi trường ảo
        pause
        exit /b 1
    )
)

REM Kích hoạt môi trường ảo
echo [*] Đang kích hoạt môi trường ảo...
call venv\Scripts\activate.bat

REM Kiểm tra đã cài đặt packages chưa
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [*] Đang cài đặt các packages cần thiết...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [X] Lỗi: Không thể cài đặt packages
        pause
        exit /b 1
    )
)

REM Kiểm tra file .env
if not exist ".env" (
    echo [!] Cảnh báo: Chưa tìm thấy file .env
    echo [*] Đang tạo file .env từ .env.example...
    copy .env.example .env >nul
    echo [!] Vui lòng cấu hình DATABASE_URL trong file .env
    echo [!] Sau đó chạy: python init_db.py để khởi tạo database
    pause
)

REM Khởi động server
echo.
echo [*] Đang khởi động server...
echo [*] Truy cập: http://localhost:8000
echo [*] API Docs: http://localhost:8000/docs
echo.
echo [!] Nhấn Ctrl+C để dừng server
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
