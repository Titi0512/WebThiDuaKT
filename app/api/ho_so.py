from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, extract
from typing import List, Optional
from datetime import datetime
import os
import uuid
import json
from pathlib import Path

from app.core.database import get_db
from app.models.models import (
    HoSoKhenThuong, User, DonVi, DanhHieuThiDua, HinhThucKhenThuong,
    LichSuXuLy, TrangThaiHoSo, UserRole, LoaiHoSo
)
from app.schemas.schemas import (
    HoSoKhenThuongCreate, HoSoKhenThuongUpdate, HoSoKhenThuongResponse,
    LichSuXuLyResponse
)
from app.api.auth import get_current_active_user

router = APIRouter(prefix="/ho-so", tags=["Hồ sơ khen thưởng"])


def generate_ma_ho_so(db: Session, nam: int) -> str:
    """Generate unique ma_ho_so."""
    count = db.query(HoSoKhenThuong).filter(
        HoSoKhenThuong.nam_khen_thuong == nam
    ).count()
    return f"HS{nam}{(count + 1):04d}"


@router.get("/", response_model=List[HoSoKhenThuongResponse])
async def get_ho_so_list(
    skip: int = 0,
    limit: int = 100,
    loai_ho_so: Optional[LoaiHoSo] = None,
    trang_thai: Optional[TrangThaiHoSo] = None,
    don_vi_id: Optional[int] = None,
    nam_khen_thuong: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all hồ sơ with filters."""
    query = db.query(HoSoKhenThuong)
    
    # Filter by loai_ho_so
    if loai_ho_so:
        query = query.filter(HoSoKhenThuong.loai_ho_so == loai_ho_so)
    
    # Filter by trang_thai
    if trang_thai:
        query = query.filter(HoSoKhenThuong.trang_thai == trang_thai)
    
    # Filter by don_vi
    if don_vi_id:
        query = query.filter(HoSoKhenThuong.don_vi_id == don_vi_id)
    
    # Filter by nam
    if nam_khen_thuong:
        query = query.filter(HoSoKhenThuong.nam_khen_thuong == nam_khen_thuong)
    
    # Search by name
    if search:
        query = query.filter(
            or_(
                HoSoKhenThuong.ho_ten.contains(search),
                HoSoKhenThuong.ten_tap_the.contains(search),
                HoSoKhenThuong.ma_ho_so.contains(search)
            )
        )
    
    # Non-admin users can only see their unit's records or their own
    if current_user.role not in [UserRole.ADMIN, UserRole.LANH_DAO]:
        query = query.filter(
            or_(
                HoSoKhenThuong.don_vi_id == current_user.don_vi_id,
                HoSoKhenThuong.nguoi_tao_id == current_user.id
            )
        )
    
    query = query.order_by(HoSoKhenThuong.created_at.desc())
    ho_so_list = query.offset(skip).limit(limit).all()
    return ho_so_list


@router.get("/{ho_so_id}", response_model=HoSoKhenThuongResponse)
async def get_ho_so(
    ho_so_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get hồ sơ by ID."""
    ho_so = db.query(HoSoKhenThuong).filter(HoSoKhenThuong.id == ho_so_id).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Hồ sơ not found")
    
    # Check permissions
    if current_user.role not in [UserRole.ADMIN, UserRole.LANH_DAO]:
        if ho_so.don_vi_id != current_user.don_vi_id and ho_so.nguoi_tao_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return ho_so


@router.post("/", response_model=HoSoKhenThuongResponse, status_code=status.HTTP_201_CREATED)
async def create_ho_so(
    ho_so_data: HoSoKhenThuongCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create new hồ sơ."""
    # VIEW_ONLY users cannot create records
    if current_user.role == UserRole.VIEW_ONLY:
        raise HTTPException(status_code=403, detail="Tài khoản chỉ xem không có quyền tạo hồ sơ")
    
    # Validate loai_ho_so
    if ho_so_data.loai_ho_so == LoaiHoSo.CA_NHAN and not ho_so_data.ho_ten:
        raise HTTPException(status_code=400, detail="Họ tên is required for cá nhân")
    
    if ho_so_data.loai_ho_so == LoaiHoSo.TAP_THE and not ho_so_data.ten_tap_the:
        raise HTTPException(status_code=400, detail="Tên tập thể is required for tập thể")
    
    # USER role can only create records for their own unit
    if current_user.role == UserRole.USER:
        if ho_so_data.don_vi_id != current_user.don_vi_id:
            raise HTTPException(status_code=403, detail="Bạn chỉ có thể tạo hồ sơ cho đơn vị của mình")
    
    # Generate ma_ho_so
    ma_ho_so = generate_ma_ho_so(db, ho_so_data.nam_khen_thuong)
    
    # Create hồ sơ
    db_ho_so = HoSoKhenThuong(
        **ho_so_data.model_dump(),
        ma_ho_so=ma_ho_so,
        nguoi_tao_id=current_user.id,
        trang_thai=TrangThaiHoSo.NHAP
    )
    
    db.add(db_ho_so)
    db.commit()
    db.refresh(db_ho_so)
    
    # Create lich su
    lich_su = LichSuXuLy(
        ho_so_id=db_ho_so.id,
        nguoi_xu_ly_id=current_user.id,
        trang_thai_moi=TrangThaiHoSo.NHAP,
        hanh_dong="Tạo hồ sơ",
        noi_dung="Khởi tạo hồ sơ khen thưởng"
    )
    db.add(lich_su)
    db.commit()
    
    return db_ho_so


@router.put("/{ho_so_id}", response_model=HoSoKhenThuongResponse)
async def update_ho_so(
    ho_so_id: int,
    ho_so_data: HoSoKhenThuongUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update hồ sơ."""
    # VIEW_ONLY users cannot update records
    if current_user.role == UserRole.VIEW_ONLY:
        raise HTTPException(status_code=403, detail="Tài khoản chỉ xem không có quyền chỉnh sửa")
    
    ho_so = db.query(HoSoKhenThuong).filter(HoSoKhenThuong.id == ho_so_id).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Hồ sơ not found")
    
    # Check permissions
    if current_user.role not in [UserRole.ADMIN, UserRole.LANH_DAO]:
        if ho_so.nguoi_tao_id != current_user.id:
            raise HTTPException(status_code=403, detail="Bạn chỉ có thể sửa hồ sơ do mình tạo")
        if ho_so.trang_thai != TrangThaiHoSo.NHAP:
            raise HTTPException(status_code=400, detail="Chỉ có thể sửa hồ sơ ở trạng thái Nháp")
    
    # Update fields
    update_data = ho_so_data.model_dump(exclude_unset=True)
    trang_thai_cu = ho_so.trang_thai
    
    for field, value in update_data.items():
        setattr(ho_so, field, value)
    
    db.commit()
    db.refresh(ho_so)
    
    # Create lich su if status changed
    if 'trang_thai' in update_data and update_data['trang_thai'] != trang_thai_cu:
        lich_su = LichSuXuLy(
            ho_so_id=ho_so.id,
            nguoi_xu_ly_id=current_user.id,
            trang_thai_cu=trang_thai_cu,
            trang_thai_moi=ho_so.trang_thai,
            hanh_dong="Cập nhật trạng thái",
            noi_dung=f"Thay đổi từ {trang_thai_cu.value} sang {ho_so.trang_thai.value}"
        )
        db.add(lich_su)
        db.commit()
    
    return ho_so


@router.post("/{ho_so_id}/trinh-duyet")
async def trinh_duyet_ho_so(
    ho_so_id: int,
    noi_dung: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Trình duyệt hồ sơ."""
    ho_so = db.query(HoSoKhenThuong).filter(HoSoKhenThuong.id == ho_so_id).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Hồ sơ not found")
    
    if ho_so.trang_thai != TrangThaiHoSo.NHAP:
        raise HTTPException(status_code=400, detail="Hồ sơ must be in NHAP status")
    
    trang_thai_cu = ho_so.trang_thai
    ho_so.trang_thai = TrangThaiHoSo.CHO_DUYET
    
    lich_su = LichSuXuLy(
        ho_so_id=ho_so.id,
        nguoi_xu_ly_id=current_user.id,
        trang_thai_cu=trang_thai_cu,
        trang_thai_moi=TrangThaiHoSo.CHO_DUYET,
        hanh_dong="Trình duyệt",
        noi_dung=noi_dung or "Trình hồ sơ lên cấp trên xem xét"
    )
    
    db.add(lich_su)
    db.commit()
    db.refresh(ho_so)
    
    return {"message": "Trình duyệt thành công", "ho_so": ho_so}


@router.post("/{ho_so_id}/phe-duyet")
async def phe_duyet_ho_so(
    ho_so_id: int,
    noi_dung: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Phê duyệt hồ sơ."""
    if current_user.role not in [UserRole.ADMIN, UserRole.LANH_DAO]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    ho_so = db.query(HoSoKhenThuong).filter(HoSoKhenThuong.id == ho_so_id).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Hồ sơ not found")
    
    if ho_so.trang_thai not in [TrangThaiHoSo.CHO_DUYET, TrangThaiHoSo.DANG_XU_LY]:
        raise HTTPException(status_code=400, detail="Invalid status for approval")
    
    trang_thai_cu = ho_so.trang_thai
    ho_so.trang_thai = TrangThaiHoSo.DA_DUYET
    
    lich_su = LichSuXuLy(
        ho_so_id=ho_so.id,
        nguoi_xu_ly_id=current_user.id,
        trang_thai_cu=trang_thai_cu,
        trang_thai_moi=TrangThaiHoSo.DA_DUYET,
        hanh_dong="Phê duyệt",
        noi_dung=noi_dung or "Phê duyệt hồ sơ khen thưởng"
    )
    
    db.add(lich_su)
    db.commit()
    db.refresh(ho_so)
    
    return {"message": "Phê duyệt thành công", "ho_so": ho_so}


@router.post("/{ho_so_id}/tu-choi")
async def tu_choi_ho_so(
    ho_so_id: int,
    noi_dung: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Từ chối hồ sơ."""
    if current_user.role not in [UserRole.ADMIN, UserRole.LANH_DAO]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    ho_so = db.query(HoSoKhenThuong).filter(HoSoKhenThuong.id == ho_so_id).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Hồ sơ not found")
    
    trang_thai_cu = ho_so.trang_thai
    ho_so.trang_thai = TrangThaiHoSo.TU_CHOI
    
    lich_su = LichSuXuLy(
        ho_so_id=ho_so.id,
        nguoi_xu_ly_id=current_user.id,
        trang_thai_cu=trang_thai_cu,
        trang_thai_moi=TrangThaiHoSo.TU_CHOI,
        hanh_dong="Từ chối",
        noi_dung=noi_dung
    )
    
    db.add(lich_su)
    db.commit()
    db.refresh(ho_so)
    
    return {"message": "Từ chối hồ sơ", "ho_so": ho_so}


@router.get("/{ho_so_id}/lich-su", response_model=List[LichSuXuLyResponse])
async def get_lich_su_ho_so(
    ho_so_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get lịch sử xử lý of hồ sơ."""
    ho_so = db.query(HoSoKhenThuong).filter(HoSoKhenThuong.id == ho_so_id).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Hồ sơ not found")
    
    lich_su_list = db.query(LichSuXuLy).filter(
        LichSuXuLy.ho_so_id == ho_so_id
    ).order_by(LichSuXuLy.created_at.desc()).all()
    
    return lich_su_list


@router.delete("/{ho_so_id}")
async def delete_ho_so(
    ho_so_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete hồ sơ."""
    ho_so = db.query(HoSoKhenThuong).filter(HoSoKhenThuong.id == ho_so_id).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Hồ sơ not found")
    
    # Only creator or admin can delete
    if current_user.role != UserRole.ADMIN and ho_so.nguoi_tao_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Can only delete if in NHAP or TU_CHOI status
    if ho_so.trang_thai not in [TrangThaiHoSo.NHAP, TrangThaiHoSo.TU_CHOI]:
        raise HTTPException(status_code=400, detail="Cannot delete submitted hồ sơ")
    
    db.delete(ho_so)
    db.commit()
    return {"message": "Hồ sơ deleted successfully"}


# Upload ảnh minh chứng
UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/{ho_so_id}/upload")
async def upload_file(
    ho_so_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload ảnh/file minh chứng cho hồ sơ."""
    # VIEW_ONLY users cannot upload files
    if current_user.role == UserRole.VIEW_ONLY:
        raise HTTPException(status_code=403, detail="Tài khoản chỉ xem không có quyền upload file")
    
    # Get ho_so
    ho_so = db.query(HoSoKhenThuong).filter(HoSoKhenThuong.id == ho_so_id).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Hồ sơ not found")
    
    # Check permissions
    if current_user.role not in [UserRole.ADMIN, UserRole.LANH_DAO]:
        if ho_so.nguoi_tao_id != current_user.id:
            raise HTTPException(status_code=403, detail="Bạn chỉ có thể upload file cho hồ sơ do mình tạo")
    
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file content
    content = await file.read()
    
    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Update ho_so file_dinh_kem
    existing_files = json.loads(ho_so.file_dinh_kem) if ho_so.file_dinh_kem else []
    existing_files.append({
        "filename": file.filename,
        "stored_name": unique_filename,
        "url": f"/static/uploads/{unique_filename}",
        "size": len(content),
        "uploaded_at": datetime.utcnow().isoformat()
    })
    ho_so.file_dinh_kem = json.dumps(existing_files)
    
    db.commit()
    db.refresh(ho_so)
    
    return {
        "message": "File uploaded successfully",
        "file": {
            "filename": file.filename,
            "stored_name": unique_filename,
            "url": f"/static/uploads/{unique_filename}",
            "size": len(content)
        }
    }


@router.delete("/{ho_so_id}/upload/{filename}")
async def delete_file(
    ho_so_id: int,
    filename: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Xóa file minh chứng."""
    # VIEW_ONLY users cannot delete files
    if current_user.role == UserRole.VIEW_ONLY:
        raise HTTPException(status_code=403, detail="Tài khoản chỉ xem không có quyền xóa file")
    
    # Get ho_so
    ho_so = db.query(HoSoKhenThuong).filter(HoSoKhenThuong.id == ho_so_id).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Hồ sơ not found")
    
    # Check permissions
    if current_user.role not in [UserRole.ADMIN, UserRole.LANH_DAO]:
        if ho_so.nguoi_tao_id != current_user.id:
            raise HTTPException(status_code=403, detail="Bạn chỉ có thể xóa file của hồ sơ do mình tạo")
    
    # Update ho_so file_dinh_kem
    existing_files = json.loads(ho_so.file_dinh_kem) if ho_so.file_dinh_kem else []
    updated_files = [f for f in existing_files if f["stored_name"] != filename]
    
    if len(updated_files) == len(existing_files):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete physical file
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        os.remove(file_path)
    
    ho_so.file_dinh_kem = json.dumps(updated_files)
    db.commit()
    
    return {"message": "File deleted successfully"}
