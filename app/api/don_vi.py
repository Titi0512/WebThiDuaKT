from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import DonVi, User, UserRole
from app.schemas.schemas import DonViCreate, DonViUpdate, DonViResponse
from app.api.auth import get_current_active_user

router = APIRouter(prefix="/don-vi", tags=["Đơn vị"])


@router.get("/", response_model=List[DonViResponse])
async def get_don_vi_list(
    skip: int = 0,
    limit: int = 100,
    loai_don_vi: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all đơn vị."""
    query = db.query(DonVi)
    
    if loai_don_vi:
        query = query.filter(DonVi.loai_don_vi == loai_don_vi)
    
    query = query.order_by(DonVi.thu_tu, DonVi.ten_don_vi)
    don_vi_list = query.offset(skip).limit(limit).all()
    return don_vi_list


@router.get("/{don_vi_id}", response_model=DonViResponse)
async def get_don_vi(
    don_vi_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get đơn vị by ID."""
    don_vi = db.query(DonVi).filter(DonVi.id == don_vi_id).first()
    if not don_vi:
        raise HTTPException(status_code=404, detail="Đơn vị not found")
    return don_vi


@router.post("/", response_model=DonViResponse, status_code=status.HTTP_201_CREATED)
async def create_don_vi(
    don_vi_data: DonViCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create new đơn vị."""
    if current_user.role not in [UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if ma_don_vi exists
    if db.query(DonVi).filter(DonVi.ma_don_vi == don_vi_data.ma_don_vi).first():
        raise HTTPException(status_code=400, detail="Mã đơn vị already exists")
    
    db_don_vi = DonVi(**don_vi_data.model_dump())
    db.add(db_don_vi)
    db.commit()
    db.refresh(db_don_vi)
    return db_don_vi


@router.put("/{don_vi_id}", response_model=DonViResponse)
async def update_don_vi(
    don_vi_id: int,
    don_vi_data: DonViUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update đơn vị."""
    if current_user.role not in [UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    don_vi = db.query(DonVi).filter(DonVi.id == don_vi_id).first()
    if not don_vi:
        raise HTTPException(status_code=404, detail="Đơn vị not found")
    
    update_data = don_vi_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(don_vi, field, value)
    
    db.commit()
    db.refresh(don_vi)
    return don_vi


@router.delete("/{don_vi_id}")
async def delete_don_vi(
    don_vi_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete đơn vị."""
    if current_user.role not in [UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    don_vi = db.query(DonVi).filter(DonVi.id == don_vi_id).first()
    if not don_vi:
        raise HTTPException(status_code=404, detail="Đơn vị not found")
    
    db.delete(don_vi)
    db.commit()
    return {"message": "Đơn vị deleted successfully"}


@router.get("/{don_vi_id}/thong-ke")
async def get_don_vi_statistics(
    don_vi_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get statistics for a specific đơn vị."""
    from app.models.models import HoSoKhenThuong, TrangThaiHoSo, LoaiHoSo
    
    don_vi = db.query(DonVi).filter(DonVi.id == don_vi_id).first()
    if not don_vi:
        raise HTTPException(status_code=404, detail="Đơn vị not found")
    
    # Total records
    total = db.query(HoSoKhenThuong).filter(HoSoKhenThuong.don_vi_id == don_vi_id).count()
    
    # Personal records
    personal = db.query(HoSoKhenThuong).filter(
        HoSoKhenThuong.don_vi_id == don_vi_id,
        HoSoKhenThuong.loai_ho_so == LoaiHoSo.CA_NHAN
    ).count()
    
    # Collective records
    collective = db.query(HoSoKhenThuong).filter(
        HoSoKhenThuong.don_vi_id == don_vi_id,
        HoSoKhenThuong.loai_ho_so == LoaiHoSo.TAP_THE
    ).count()
    
    # Approved records
    approved = db.query(HoSoKhenThuong).filter(
        HoSoKhenThuong.don_vi_id == don_vi_id,
        HoSoKhenThuong.trang_thai == TrangThaiHoSo.DA_DUYET
    ).count()
    
    return {
        "don_vi": {
            "id": don_vi.id,
            "ma_don_vi": don_vi.ma_don_vi,
            "ten_don_vi": don_vi.ten_don_vi,
            "loai_don_vi": don_vi.loai_don_vi
        },
        "statistics": {
            "total": total,
            "personal": personal,
            "collective": collective,
            "approved": approved
        }
    }

