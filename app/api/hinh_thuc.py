from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import HinhThucKhenThuong, User, UserRole
from app.schemas.schemas import HinhThucKhenThuongCreate, HinhThucKhenThuongUpdate, HinhThucKhenThuongResponse
from app.api.auth import get_current_active_user

router = APIRouter(prefix="/hinh-thuc", tags=["Hình thức khen thưởng"])


@router.get("/", response_model=List[HinhThucKhenThuongResponse])
async def get_hinh_thuc_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all hình thức khen thưởng."""
    hinh_thuc_list = db.query(HinhThucKhenThuong).order_by(
        HinhThucKhenThuong.thu_tu, HinhThucKhenThuong.ten_hinh_thuc
    ).offset(skip).limit(limit).all()
    return hinh_thuc_list


@router.get("/{hinh_thuc_id}", response_model=HinhThucKhenThuongResponse)
async def get_hinh_thuc(
    hinh_thuc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get hình thức by ID."""
    hinh_thuc = db.query(HinhThucKhenThuong).filter(HinhThucKhenThuong.id == hinh_thuc_id).first()
    if not hinh_thuc:
        raise HTTPException(status_code=404, detail="Hình thức not found")
    return hinh_thuc


@router.post("/", response_model=HinhThucKhenThuongResponse, status_code=status.HTTP_201_CREATED)
async def create_hinh_thuc(
    hinh_thuc_data: HinhThucKhenThuongCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create new hình thức."""
    if current_user.role not in [UserRole.ADMIN, UserRole.CAN_BO]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if ma_hinh_thuc exists
    if db.query(HinhThucKhenThuong).filter(HinhThucKhenThuong.ma_hinh_thuc == hinh_thuc_data.ma_hinh_thuc).first():
        raise HTTPException(status_code=400, detail="Mã hình thức already exists")
    
    db_hinh_thuc = HinhThucKhenThuong(**hinh_thuc_data.model_dump())
    db.add(db_hinh_thuc)
    db.commit()
    db.refresh(db_hinh_thuc)
    return db_hinh_thuc


@router.put("/{hinh_thuc_id}", response_model=HinhThucKhenThuongResponse)
async def update_hinh_thuc(
    hinh_thuc_id: int,
    hinh_thuc_data: HinhThucKhenThuongUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update hình thức."""
    if current_user.role not in [UserRole.ADMIN, UserRole.CAN_BO]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    hinh_thuc = db.query(HinhThucKhenThuong).filter(HinhThucKhenThuong.id == hinh_thuc_id).first()
    if not hinh_thuc:
        raise HTTPException(status_code=404, detail="Hình thức not found")
    
    update_data = hinh_thuc_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(hinh_thuc, field, value)
    
    db.commit()
    db.refresh(hinh_thuc)
    return hinh_thuc


@router.delete("/{hinh_thuc_id}")
async def delete_hinh_thuc(
    hinh_thuc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete hình thức."""
    if current_user.role not in [UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    hinh_thuc = db.query(HinhThucKhenThuong).filter(HinhThucKhenThuong.id == hinh_thuc_id).first()
    if not hinh_thuc:
        raise HTTPException(status_code=404, detail="Hình thức not found")
    
    db.delete(hinh_thuc)
    db.commit()
    return {"message": "Hình thức deleted successfully"}
