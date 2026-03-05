"""
Test MySQL connection
Kiểm tra kết nối MySQL trước khi chạy ứng dụng chính
"""

import sys
from sqlalchemy import create_engine, text

def test_connection():
    """Test kết nối database"""
    
    # Đọc DATABASE_URL từ file .env
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('DATABASE_URL='):
                    database_url = line.split('=', 1)[1].strip()
                    break
            else:
                print("❌ Không tìm thấy DATABASE_URL trong file .env")
                print("📝 Vui lòng tạo file .env từ .env.example")
                return False
    except FileNotFoundError:
        print("❌ Không tìm thấy file .env")
        print("📝 Vui lòng tạo file .env từ .env.example")
        return False
    
    print(f"🔍 Đang kiểm tra kết nối...")
    print(f"📍 URL: {database_url.replace(database_url.split('@')[0].split('//')[1], '***')}")
    print()
    
    try:
        # Tạo engine với charset utf8mb4 cho MariaDB
        engine = create_engine(
            database_url,
            connect_args={"charset": "utf8mb4"}
        )
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            
            # Xác định loại database
            db_type = "MariaDB" if "MariaDB" in version else "MySQL"
            
            print(f"✅ Kết nối {db_type} thành công!")
            print(f"📦 {db_type} version: {version}")
            print()
            
            # Kiểm tra database có tồn tại không
            db_name = database_url.split('/')[-1].split('?')[0]
            result = conn.execute(text(f"SHOW DATABASES LIKE '{db_name}'"))
            if result.fetchone():
                print(f"✅ Database '{db_name}' đã tồn tại")
            else:
                print(f"⚠️  Database '{db_name}' chưa tồn tại")
                print(f"💡 Chạy lệnh: CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            
            print()
            print("🎉 Bạn có thể chạy: python init_db.py")
            return True
            
    except Exception as e:
        print("❌ Lỗi kết nối MariaDB/MySQL!")
        print(f"📄 Chi tiết: {str(e)}")
        print()
        print("🔧 Các bước khắc phục:")
        print()
        
        if "Authentication plugin" in str(e):
            print("1️⃣  Lỗi Authentication Plugin - Đây là MariaDB, chạy lệnh SQL sau:")
            print("   SET PASSWORD FOR 'root'@'localhost' = PASSWORD('your_password');")
            print("   FLUSH PRIVILEGES;")
            print()
            print("   Xem chi tiết: FIX_AUTH_ERROR.md hoặc fix_auth_mariadb.sql")
            
        elif "Access denied" in str(e):
            print("1️⃣  Kiểm tra username/password trong file .env")
            print("2️⃣  Đảm bảo user có quyền truy cập MariaDB")
            
        elif "Can't connect" in str(e):
            print("1️⃣  Kiểm tra MariaDB service đã chạy chưa")
            print("2️⃣  Kiểm tra host và port có đúng không (mặc định: localhost:3306)")
            
        else:
            print("1️⃣  Kiểm tra MariaDB đã cài đặt và đang chạy")
            print("2️⃣  Kiểm tra DATABASE_URL trong file .env")
            print("3️⃣  Xem file FIX_AUTH_ERROR.md để biết thêm chi tiết")
        
        print()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  TEST KẾT NỐI MARIADB")
    print("  Hệ thống Quản lý Khen thưởng")
    print("=" * 60)
    print()
    
    success = test_connection()
    
    print()
    print("=" * 60)
    
    sys.exit(0 if success else 1)
