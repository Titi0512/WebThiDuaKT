from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enums
class LoaiDonVi(str, Enum):
    KHOI_CO_QUAN = "khoi_co_quan"
    KHOA = "khoa"
    DON_VI_TRUC_THUOC = "don_vi_truc_thuoc"


class UserRole(str, Enum):
    ADMIN = "admin"
    LANH_DAO = "lanh_dao"
    CAN_BO = "can_bo"
    USER = "user"
    VIEW_ONLY = "view_only"


class TrangThaiHoSo(str, Enum):
    NHAP = "nhap"
    CHO_DUYET = "cho_duyet"
    DANG_XU_LY = "dang_xu_ly"
    DA_DUYET = "da_duyet"
    TU_CHOI = "tu_choi"


class LoaiHoSo(str, Enum):
    CA_NHAN = "ca_nhan"
    TAP_THE = "tap_the"


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    ho_ten: str = Field(..., min_length=1, max_length=255)
    cap_bac: Optional[str] = None
    chuc_vu: Optional[str] = None
    don_vi_id: Optional[int] = None
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    ho_ten: Optional[str] = None
    cap_bac: Optional[str] = None
    chuc_vu: Optional[str] = None
    don_vi_id: Optional[int] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# DonVi Schemas
class DonViBase(BaseModel):
    ma_don_vi: str = Field(..., max_length=50)
    ten_don_vi: str = Field(..., max_length=255)
    loai_don_vi: LoaiDonVi
    mo_ta: Optional[str] = None
    thu_tu: int = 0


class DonViCreate(DonViBase):
    pass


class DonViUpdate(BaseModel):
    ten_don_vi: Optional[str] = None
    mo_ta: Optional[str] = None
    thu_tu: Optional[int] = None
    is_active: Optional[bool] = None


class DonViResponse(DonViBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# DanhHieuThiDua Schemas
class DanhHieuThiDuaBase(BaseModel):
    ma_danh_hieu: str = Field(..., max_length=50)
    ten_danh_hieu: str = Field(..., max_length=255)
    mo_ta: Optional[str] = None
    cap_khen_thuong: Optional[str] = None
    thu_tu: int = 0


class DanhHieuThiDuaCreate(DanhHieuThiDuaBase):
    pass


class DanhHieuThiDuaUpdate(BaseModel):
    ten_danh_hieu: Optional[str] = None
    mo_ta: Optional[str] = None
    cap_khen_thuong: Optional[str] = None
    thu_tu: Optional[int] = None
    is_active: Optional[bool] = None


class DanhHieuThiDuaResponse(DanhHieuThiDuaBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# HinhThucKhenThuong Schemas
class HinhThucKhenThuongBase(BaseModel):
    ma_hinh_thuc: str = Field(..., max_length=50)
    ten_hinh_thuc: str = Field(..., max_length=255)
    mo_ta: Optional[str] = None
    muc_thuong: Optional[float] = None
    cap_khen_thuong: Optional[str] = None
    thu_tu: int = 0


class HinhThucKhenThuongCreate(HinhThucKhenThuongBase):
    pass


class HinhThucKhenThuongUpdate(BaseModel):
    ten_hinh_thuc: Optional[str] = None
    mo_ta: Optional[str] = None
    muc_thuong: Optional[float] = None
    cap_khen_thuong: Optional[str] = None
    thu_tu: Optional[int] = None
    is_active: Optional[bool] = None


class HinhThucKhenThuongResponse(HinhThucKhenThuongBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# HoSoKhenThuong Schemas
class HoSoKhenThuongBase(BaseModel):
    loai_ho_so: LoaiHoSo
    ho_ten: Optional[str] = None
    cap_bac: Optional[str] = None
    chuc_vu: Optional[str] = None
    ten_tap_the: Optional[str] = None
    don_vi_id: int
    danh_hieu_id: Optional[int] = None
    hinh_thuc_id: Optional[int] = None
    thanh_tich: str
    nam_khen_thuong: int
    ghi_chu: Optional[str] = None


class HoSoKhenThuongCreate(HoSoKhenThuongBase):
    pass


class HoSoKhenThuongUpdate(BaseModel):
    ho_ten: Optional[str] = None
    cap_bac: Optional[str] = None
    chuc_vu: Optional[str] = None
    ten_tap_the: Optional[str] = None
    don_vi_id: Optional[int] = None
    danh_hieu_id: Optional[int] = None
    hinh_thuc_id: Optional[int] = None
    thanh_tich: Optional[str] = None
    nam_khen_thuong: Optional[int] = None
    trang_thai: Optional[TrangThaiHoSo] = None
    ghi_chu: Optional[str] = None


class HoSoKhenThuongResponse(HoSoKhenThuongBase):
    id: int
    ma_ho_so: str
    trang_thai: TrangThaiHoSo
    nguoi_tao_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# LichSuXuLy Schemas
class LichSuXuLyBase(BaseModel):
    ho_so_id: int
    hanh_dong: str
    noi_dung: Optional[str] = None
    trang_thai_cu: Optional[TrangThaiHoSo] = None
    trang_thai_moi: Optional[TrangThaiHoSo] = None


class LichSuXuLyCreate(LichSuXuLyBase):
    pass


class LichSuXuLyResponse(LichSuXuLyBase):
    id: int
    nguoi_xu_ly_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Statistics Schema
class ThongKe(BaseModel):
    tong_ho_so: int = 0
    ho_so_cho_duyet: int = 0
    ho_so_da_duyet: int = 0
    ho_so_tu_choi: int = 0
    ho_so_ca_nhan: int = 0
    ho_so_tap_the: int = 0


class ThongKeTheoDonVi(BaseModel):
    don_vi: str
    so_luong: int
    ca_nhan: int = 0
    tap_the: int = 0


class ThongKeTheoNam(BaseModel):
    nam: int
    so_luong: int
    ca_nhan: int = 0
    tap_the: int = 0
