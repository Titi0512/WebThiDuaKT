from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class LoaiDonVi(str, enum.Enum):
    """Loại đơn vị"""
    KHOI_CO_QUAN = "khoi_co_quan"
    KHOA = "khoa"
    DON_VI_TRUC_THUOC = "don_vi_truc_thuoc"


class UserRole(str, enum.Enum):
    """Vai trò người dùng"""
    ADMIN = "admin"
    LANH_DAO = "lanh_dao"
    CAN_BO = "can_bo"
    USER = "user"
    VIEW_ONLY = "view_only"


class TrangThaiHoSo(str, enum.Enum):
    """Trạng thái hồ sơ"""
    NHAP = "nhap"
    CHO_DUYET = "cho_duyet"
    DANG_XU_LY = "dang_xu_ly"
    DA_DUYET = "da_duyet"
    TU_CHOI = "tu_choi"


class LoaiHoSo(str, enum.Enum):
    """Loại hồ sơ khen thưởng"""
    CA_NHAN = "ca_nhan"
    TAP_THE = "tap_the"


class User(Base):
    """Model người dùng"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    ho_ten = Column(String(255), nullable=False)
    cap_bac = Column(String(100))
    chuc_vu = Column(String(255))
    don_vi_id = Column(Integer, ForeignKey("don_vi.id"))
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    don_vi = relationship("DonVi", back_populates="users")
    ho_so_tao = relationship("HoSoKhenThuong", foreign_keys="HoSoKhenThuong.nguoi_tao_id", back_populates="nguoi_tao")
    xu_ly_ho_so = relationship("LichSuXuLy", back_populates="nguoi_xu_ly")
    nhat_ky = relationship("NhatKyHoatDong", back_populates="user")


class DonVi(Base):
    """Model đơn vị"""
    __tablename__ = "don_vi"
    
    id = Column(Integer, primary_key=True, index=True)
    ma_don_vi = Column(String(50), unique=True, index=True, nullable=False)
    ten_don_vi = Column(String(255), nullable=False)
    loai_don_vi = Column(Enum(LoaiDonVi), nullable=False)
    mo_ta = Column(Text)
    thu_tu = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="don_vi")
    ho_so_khen_thuong = relationship("HoSoKhenThuong", back_populates="don_vi")


class DanhHieuThiDua(Base):
    """Model danh hiệu thi đua"""
    __tablename__ = "danh_hieu_thi_dua"
    
    id = Column(Integer, primary_key=True, index=True)
    ma_danh_hieu = Column(String(50), unique=True, index=True, nullable=False)
    ten_danh_hieu = Column(String(255), nullable=False)
    mo_ta = Column(Text)
    cap_khen_thuong = Column(String(100))  # Cấp Bộ, cấp Quân khu, cấp Trường...
    thu_tu = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ho_so_khen_thuong = relationship("HoSoKhenThuong", back_populates="danh_hieu")


class HinhThucKhenThuong(Base):
    """Model hình thức khen thưởng"""
    __tablename__ = "hinh_thuc_khen_thuong"
    
    id = Column(Integer, primary_key=True, index=True)
    ma_hinh_thuc = Column(String(50), unique=True, index=True, nullable=False)
    ten_hinh_thuc = Column(String(255), nullable=False)
    mo_ta = Column(Text)
    muc_thuong = Column(Float)  # Mức thưởng (nếu có)
    cap_khen_thuong = Column(String(100))
    thu_tu = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ho_so_khen_thuong = relationship("HoSoKhenThuong", back_populates="hinh_thuc")


class HoSoKhenThuong(Base):
    """Model hồ sơ khen thưởng"""
    __tablename__ = "ho_so_khen_thuong"
    
    id = Column(Integer, primary_key=True, index=True)
    ma_ho_so = Column(String(100), unique=True, index=True, nullable=False)
    loai_ho_so = Column(Enum(LoaiHoSo), nullable=False)
    
    # Thông tin cá nhân/tập thể
    ho_ten = Column(String(255))  # Cho cá nhân
    cap_bac = Column(String(100))  # Cho cá nhân
    chuc_vu = Column(String(255))
    ten_tap_the = Column(String(255))  # Cho tập thể
    
    # Đơn vị
    don_vi_id = Column(Integer, ForeignKey("don_vi.id"), nullable=False)
    
    # Thông tin khen thưởng
    danh_hieu_id = Column(Integer, ForeignKey("danh_hieu_thi_dua.id"))
    hinh_thuc_id = Column(Integer, ForeignKey("hinh_thuc_khen_thuong.id"))
    
    # Thành tích
    thanh_tich = Column(Text, nullable=False)
    nam_khen_thuong = Column(Integer, nullable=False)
    
    # Trạng thái
    trang_thai = Column(Enum(TrangThaiHoSo), default=TrangThaiHoSo.NHAP)
    
    # File đính kèm
    file_dinh_kem = Column(Text)  # JSON array of file paths
    
    # Người tạo
    nguoi_tao_id = Column(Integer, ForeignKey("users.id"))
    
    # Ghi chú
    ghi_chu = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    don_vi = relationship("DonVi", back_populates="ho_so_khen_thuong")
    danh_hieu = relationship("DanhHieuThiDua", back_populates="ho_so_khen_thuong")
    hinh_thuc = relationship("HinhThucKhenThuong", back_populates="ho_so_khen_thuong")
    nguoi_tao = relationship("User", foreign_keys=[nguoi_tao_id], back_populates="ho_so_tao")
    lich_su_xu_ly = relationship("LichSuXuLy", back_populates="ho_so", cascade="all, delete-orphan")


class LichSuXuLy(Base):
    """Model lịch sử xử lý hồ sơ"""
    __tablename__ = "lich_su_xu_ly"
    
    id = Column(Integer, primary_key=True, index=True)
    ho_so_id = Column(Integer, ForeignKey("ho_so_khen_thuong.id"), nullable=False)
    nguoi_xu_ly_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    trang_thai_cu = Column(Enum(TrangThaiHoSo))
    trang_thai_moi = Column(Enum(TrangThaiHoSo))
    
    hanh_dong = Column(String(255), nullable=False)  # Trình duyệt, Phê duyệt, Từ chối...
    noi_dung = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ho_so = relationship("HoSoKhenThuong", back_populates="lich_su_xu_ly")
    nguoi_xu_ly = relationship("User", back_populates="xu_ly_ho_so")


class NhatKyHoatDong(Base):
    """Model nhật ký hoạt động hệ thống"""
    __tablename__ = "nhat_ky_hoat_dong"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hanh_dong = Column(String(255), nullable=False)
    mo_ta = Column(Text)
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="nhat_ky")
