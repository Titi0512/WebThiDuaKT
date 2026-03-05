from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import DanhHieuThiDua, User, UserRole
from app.schemas.schemas import DanhHieuThiDuaCreate, DanhHieuThiDuaUpdate, DanhHieuThiDuaResponse
from app.api.auth import get_current_active_user

router = APIRouter(prefix="/danh-hieu", tags=["Danh hiệu thi đua"])


@router.get("/", response_model=List[DanhHieuThiDuaResponse])
async def get_danh_hieu_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all danh hiệu thi đua."""
    danh_hieu_list = db.query(DanhHieuThiDua).order_by(
        DanhHieuThiDua.thu_tu, DanhHieuThiDua.ten_danh_hieu
    ).offset(skip).limit(limit).all()
    return danh_hieu_list


@router.get("/{danh_hieu_id}", response_model=DanhHieuThiDuaResponse)
async def get_danh_hieu(
    danh_hieu_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get danh hiệu by ID."""
    danh_hieu = db.query(DanhHieuThiDua).filter(DanhHieuThiDua.id == danh_hieu_id).first()
    if not danh_hieu:
        raise HTTPException(status_code=404, detail="Danh hiệu not found")
    return danh_hieu


@router.post("/", response_model=DanhHieuThiDuaResponse, status_code=status.HTTP_201_CREATED)
async def create_danh_hieu(
    danh_hieu_data: DanhHieuThiDuaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create new danh hiệu."""
    if current_user.role not in [UserRole.ADMIN, UserRole.CAN_BO]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if ma_danh_hieu exists
    if db.query(DanhHieuThiDua).filter(DanhHieuThiDua.ma_danh_hieu == danh_hieu_data.ma_danh_hieu).first():
        raise HTTPException(status_code=400, detail="Mã danh hiệu already exists")
    
    db_danh_hieu = DanhHieuThiDua(**danh_hieu_data.model_dump())
    db.add(db_danh_hieu)
    db.commit()
    db.refresh(db_danh_hieu)
    return db_danh_hieu


@router.put("/{danh_hieu_id}", response_model=DanhHieuThiDuaResponse)
async def update_danh_hieu(
    danh_hieu_id: int,
    danh_hieu_data: DanhHieuThiDuaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update danh hiệu."""
    if current_user.role not in [UserRole.ADMIN, UserRole.CAN_BO]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    danh_hieu = db.query(DanhHieuThiDua).filter(DanhHieuThiDua.id == danh_hieu_id).first()
    if not danh_hieu:
        raise HTTPException(status_code=404, detail="Danh hiệu not found")
    
    update_data = danh_hieu_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(danh_hieu, field, value)
    
    db.commit()
    db.refresh(danh_hieu)
    return danh_hieu


@router.delete("/{danh_hieu_id}")
async def delete_danh_hieu(
    danh_hieu_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete danh hiệu."""
    if current_user.role not in [UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    danh_hieu = db.query(DanhHieuThiDua).filter(DanhHieuThiDua.id == danh_hieu_id).first()
    if not danh_hieu:
        raise HTTPException(status_code=404, detail="Danh hiệu not found")
    
    db.delete(danh_hieu)
    db.commit()
    return {"message": "Danh hiệu deleted successfully"}
