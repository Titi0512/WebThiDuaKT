"""
Script to initialize database with sample data
"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.models import (
    User, DonVi, DanhHieuThiDua, HinhThucKhenThuong,
    UserRole, LoaiDonVi
)

# Create all tables
Base.metadata.create_all(bind=engine)


def init_db():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already initialized!")
            return
        
        print("Initializing database...")
        
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            ho_ten="Quản trị viên",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        
        # Create demo user
        demo_user = User(
            username="user",
            email="user@example.com",
            hashed_password=get_password_hash("user123"),
            ho_ten="Người dùng demo",
            role=UserRole.USER,
            is_active=True
        )
        db.add(demo_user)
        
        print("✓ Created users")
        
        # Create Khối cơ quan
        khoi_co_quan = [
            ("B1", "Phòng Tham mưu - Hành chính", 1),
            ("B2", "Phòng Đào tạo", 2),
            ("B3", "Phòng Chính trị", 3),
            ("B4", "Phòng Khoa học quân sự", 4),
            ("B5", "Phòng Hậu cần - Kỹ thuật", 5),
            ("B6", "Ban Tài Chính", 6),
            ("B7", "Ban Khảo thí và đảm bảo chất lượng giáo dục đào tạo", 7),
            ("B8", "Ban Sau Đại học", 8),
            ("B9", "Ban thông tin khoa học quân sự", 9),
            ("B11", "Uỷ Ban kiểm tra Đảng", 11),
            ("B12", "Thanh tra Nhà trường", 12),
        ]
        
        for ma, ten, thu_tu in khoi_co_quan:
            don_vi = DonVi(
                ma_don_vi=ma,
                ten_don_vi=ten,
                loai_don_vi=LoaiDonVi.KHOI_CO_QUAN,
                thu_tu=thu_tu
            )
            db.add(don_vi)
        
        print("✓ Created Khối cơ quan")
        
        # Create Các khoa
        khoa = [
            ("K1", "Khoa Triết học Mác - Lênin", 1),
            ("K2", "Khoa Lịch sử Đảng Cộng sản Việt Nam", 2),
            ("K3", "Khoa Công tác Đảng,Công tác Chính trị", 3),
            ("K4", "Khoa Chiến thuật", 4),
            ("K5", "Khoa Văn hóa - Ngoại ngữ", 5),
            ("K6", "Khoa Kinh tế chính trị Mác - Lênin", 6),
            ("K7", "Khoa Chủ nghĩa xã hội khoa học", 7),
            ("K8", "Khoa Tâm lý học quân sự", 8),
            ("K9", "Khoa Bắn súng", 9),
            ("K10", "Khoa Quân sự chung", 10),
            ("K11", "Khoa Giáo dục thể chất", 11),
            ("K12", "Khoa Sư phạm quân sự", 12),
            ("K13", "Khoa Tư tưởng Hồ Chí Minh", 13),
            ("K14", "Khoa Nhà nước & Pháp luật", 14),
        ]
        
        for ma, ten, thu_tu in khoa:
            don_vi = DonVi(
                ma_don_vi=ma,
                ten_don_vi=ten,
                loai_don_vi=LoaiDonVi.KHOA,
                thu_tu=thu_tu
            )
            db.add(don_vi)
        
        print("✓ Created Các khoa")
        
        # Create Đơn vị trực thuộc
        don_vi_truc_thuoc = [
            ("HE1", "Hệ 1 (Hệ Chuyển loại cán bộ chính trị, hoàn thiện đại học)", 1),
            ("HE2", "Hệ 2 (Hệ sau đại học)", 2),
            ("HE3", "Hệ 3 (Hệ quốc tế)", 3),
        ]
        
        for i in range(1, 13):
            don_vi_truc_thuoc.append((f"TD{i}", f"Tiểu đoàn {i}", i + 3))
        
        for ma, ten, thu_tu in don_vi_truc_thuoc:
            don_vi = DonVi(
                ma_don_vi=ma,
                ten_don_vi=ten,
                loai_don_vi=LoaiDonVi.DON_VI_TRUC_THUOC,
                thu_tu=thu_tu
            )
            db.add(don_vi)
        
        print("✓ Created Đơn vị trực thuộc")
        
        # Create Danh hiệu thi đua
        danh_hieu = [
            ("DH01", "Chiến sĩ thi đua cơ sở", "Cấp cơ sở", 1),
            ("DH02", "Chiến sĩ thi đua cấp Bộ", "Cấp Bộ", 2),
            ("DH03", "Chiến sĩ thi đua toàn quốc", "Cấp Nhà nước", 3),
            ("DH04", "Tập thể lao động tiên tiến", "Cấp cơ sở", 4),
            ("DH05", "Tập thể lao động xuất sắc", "Cấp Bộ", 5),
            ("DH06", "Cờ thi đua của Chính phủ", "Cấp Nhà nước", 6),
            ("DH07", "Chiến sĩ tiên tiến", "Cấp đơn vị", 7),
        ]
        
        for ma, ten, cap, thu_tu in danh_hieu:
            dh = DanhHieuThiDua(
                ma_danh_hieu=ma,
                ten_danh_hieu=ten,
                cap_khen_thuong=cap,
                thu_tu=thu_tu
            )
            db.add(dh)
        
        print("✓ Created Danh hiệu thi đua")
        
        # Create Hình thức khen thưởng
        hinh_thuc = [
            ("HT01", "Bằng khen của Thủ tướng Chính phủ", None, "Cấp Nhà nước", 1),
            ("HT02", "Bằng khen của Bộ trưởng", None, "Cấp Bộ", 2),
            ("HT03", "Giấy khen của Hiệu trưởng", None, "Cấp Trường", 3),
            ("HT04", "Huân chương Lao động hạng Nhất", None, "Cấp Nhà nước", 4),
            ("HT05", "Huân chương Lao động hạng Nhì", None, "Cấp Nhà nước", 5),
            ("HT06", "Huân chương Lao động hạng Ba", None, "Cấp Nhà nước", 6),
            ("HT07", "Huy chương Vì sự nghiệp giáo dục", None, "Cấp Bộ", 7),
            ("HT08", "Giấy khen và tiền thưởng", 2000000, "Cấp Trường", 8),
        ]
        
        for ma, ten, muc, cap, thu_tu in hinh_thuc:
            ht = HinhThucKhenThuong(
                ma_hinh_thuc=ma,
                ten_hinh_thuc=ten,
                muc_thuong=muc,
                cap_khen_thuong=cap,
                thu_tu=thu_tu
            )
            db.add(ht)
        
        print("✓ Created Hình thức khen thưởng")
        
        # Commit all changes
        db.commit()
        
        print("\n✓✓✓ Database initialized successfully! ✓✓✓")
        print("\nDefault users:")
        print("  Admin: admin / admin123")
        print("  User:  user / user123")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("Initializing Database...")
    print("=" * 50)
    init_db()
