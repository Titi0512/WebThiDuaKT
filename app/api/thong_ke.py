from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_, case
from typing import List, Optional

from app.core.database import get_db
from app.models.models import (
    HoSoKhenThuong, DonVi, User, UserRole,
    TrangThaiHoSo, LoaiHoSo, DanhHieuThiDua, HinhThucKhenThuong
)
from app.schemas.schemas import ThongKe, ThongKeTheoDonVi, ThongKeTheoNam
from app.api.auth import get_current_active_user

router = APIRouter(prefix="/thong-ke", tags=["Thống kê & Báo cáo"])


@router.get("/tong-quat", response_model=ThongKe)
async def get_thong_ke_tong_quat(
    nam: Optional[int] = None,
    don_vi_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Thống kê tổng quát."""
    query = db.query(HoSoKhenThuong)
    
    if nam:
        query = query.filter(HoSoKhenThuong.nam_khen_thuong == nam)
    
    if don_vi_id:
        query = query.filter(HoSoKhenThuong.don_vi_id == don_vi_id)
    
    # Non-admin users only see their unit
    if current_user.role not in [UserRole.ADMIN, UserRole.LANH_DAO]:
        query = query.filter(HoSoKhenThuong.don_vi_id == current_user.don_vi_id)
    
    tong_ho_so = query.count()
    ho_so_cho_duyet = query.filter(HoSoKhenThuong.trang_thai == TrangThaiHoSo.CHO_DUYET).count()
    ho_so_da_duyet = query.filter(HoSoKhenThuong.trang_thai == TrangThaiHoSo.DA_DUYET).count()
    ho_so_tu_choi = query.filter(HoSoKhenThuong.trang_thai == TrangThaiHoSo.TU_CHOI).count()
    ho_so_ca_nhan = query.filter(HoSoKhenThuong.loai_ho_so == LoaiHoSo.CA_NHAN).count()
    ho_so_tap_the = query.filter(HoSoKhenThuong.loai_ho_so == LoaiHoSo.TAP_THE).count()
    
    return ThongKe(
        tong_ho_so=tong_ho_so,
        ho_so_cho_duyet=ho_so_cho_duyet,
        ho_so_da_duyet=ho_so_da_duyet,
        ho_so_tu_choi=ho_so_tu_choi,
        ho_so_ca_nhan=ho_so_ca_nhan,
        ho_so_tap_the=ho_so_tap_the
    )


@router.get("/theo-don-vi", response_model=List[ThongKeTheoDonVi])
async def get_thong_ke_theo_don_vi(
    nam: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Thống kê theo đơn vị."""
    query = db.query(
        DonVi.ten_don_vi,
        func.count(HoSoKhenThuong.id).label('so_luong'),
        func.sum(case((HoSoKhenThuong.loai_ho_so == LoaiHoSo.CA_NHAN, 1), else_=0)).label('ca_nhan'),
        func.sum(case((HoSoKhenThuong.loai_ho_so == LoaiHoSo.TAP_THE, 1), else_=0)).label('tap_the')
    ).join(
        HoSoKhenThuong, DonVi.id == HoSoKhenThuong.don_vi_id
    )
    
    if nam:
        query = query.filter(HoSoKhenThuong.nam_khen_thuong == nam)
    
    # Non-admin users only see their unit
    if current_user.role not in [UserRole.ADMIN, UserRole.LANH_DAO]:
        query = query.filter(DonVi.id == current_user.don_vi_id)
    
    query = query.group_by(DonVi.ten_don_vi).order_by(func.count(HoSoKhenThuong.id).desc())
    
    results = query.all()
    
    return [
        ThongKeTheoDonVi(
            don_vi=row[0],
            so_luong=row[1] or 0,
            ca_nhan=row[2] or 0,
            tap_the=row[3] or 0
        )
        for row in results
    ]


@router.get("/theo-nam", response_model=List[ThongKeTheoNam])
async def get_thong_ke_theo_nam(
    don_vi_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Thống kê theo năm."""
    query = db.query(
        HoSoKhenThuong.nam_khen_thuong,
        func.count(HoSoKhenThuong.id).label('so_luong'),
        func.sum(case((HoSoKhenThuong.loai_ho_so == LoaiHoSo.CA_NHAN, 1), else_=0)).label('ca_nhan'),
        func.sum(case((HoSoKhenThuong.loai_ho_so == LoaiHoSo.TAP_THE, 1), else_=0)).label('tap_the')
    )
    
    if don_vi_id:
        query = query.filter(HoSoKhenThuong.don_vi_id == don_vi_id)
    
    # Non-admin users only see their unit
    if current_user.role not in [UserRole.ADMIN, UserRole.LANH_DAO]:
        query = query.filter(HoSoKhenThuong.don_vi_id == current_user.don_vi_id)
    
    query = query.group_by(HoSoKhenThuong.nam_khen_thuong).order_by(HoSoKhenThuong.nam_khen_thuong.desc())
    
    results = query.all()
    
    return [
        ThongKeTheoNam(
            nam=row[0],
            so_luong=row[1] or 0,
            ca_nhan=row[2] or 0,
            tap_the=row[3] or 0
        )
        for row in results
    ]


@router.get("/dashboard")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get dashboard statistics."""
    # Base query
    query = db.query(HoSoKhenThuong)
    
    # Filter by user role
    if current_user.role not in [UserRole.ADMIN, UserRole.LANH_DAO]:
        query = query.filter(HoSoKhenThuong.don_vi_id == current_user.don_vi_id)
    
    # Get statistics
    total_records = query.count()
    pending_approval = query.filter(HoSoKhenThuong.trang_thai == TrangThaiHoSo.CHO_DUYET).count()
    approved = query.filter(HoSoKhenThuong.trang_thai == TrangThaiHoSo.DA_DUYET).count()
    rejected = query.filter(HoSoKhenThuong.trang_thai == TrangThaiHoSo.TU_CHOI).count()
    
    # Recent records
    recent_records = query.order_by(HoSoKhenThuong.created_at.desc()).limit(5).all()
    
    # Count by type
    individual_count = query.filter(HoSoKhenThuong.loai_ho_so == LoaiHoSo.CA_NHAN).count()
    collective_count = query.filter(HoSoKhenThuong.loai_ho_so == LoaiHoSo.TAP_THE).count()
    
    # Count total units, awards, forms
    total_units = db.query(DonVi).filter(DonVi.is_active == True).count()
    total_awards = db.query(DanhHieuThiDua).filter(DanhHieuThiDua.is_active == True).count()
    total_forms = db.query(HinhThucKhenThuong).filter(HinhThucKhenThuong.is_active == True).count()
    
    return {
        "total_records": total_records,
        "pending_approval": pending_approval,
        "approved": approved,
        "rejected": rejected,
        "individual_count": individual_count,
        "collective_count": collective_count,
        "total_units": total_units,
        "total_awards": total_awards,
        "total_forms": total_forms,
        "recent_records": [
            {
                "id": r.id,
                "ma_ho_so": r.ma_ho_so,
                "loai": r.loai_ho_so.value,
                "ten": r.ho_ten if r.loai_ho_so == LoaiHoSo.CA_NHAN else r.ten_tap_the,
                "trang_thai": r.trang_thai.value,
                "created_at": r.created_at.isoformat()
            }
            for r in recent_records
        ]
    }
