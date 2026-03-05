# FIX LỖI IMPORT - CẬP NHẬT LẦN 4

## Lỗi đã fix

### ImportError: cannot import name 'get_current_user' from 'app.core.security'

**Nguyên nhân:**  
Hàm `get_current_user` không nằm trong `app.core.security.py` mà nằm trong `app.api.auth.py`

**Giải pháp:**  
Đã sửa dòng 33 trong `app/api/export.py`:

```python
# SAI:
from app.core.security import get_current_user

# ĐÚNG:
from app.api.auth import get_current_user
```

---

### ImportError: cannot import name 'HoSo' from 'app.models.models'

**Nguyên nhân:**  
Tên model trong database là `HoSoKhenThuong`, không phải `HoSo`

**Giải pháp:**  
Đã thay thế tất cả `HoSo` thành `HoSoKhenThuong` trong `app/api/export.py`:

```python
# SAI:
from app.models.models import User, HoSo, DonVi
query = db.query(HoSo).join(DonVi)

# ĐÚNG:
from app.models.models import User, HoSoKhenThuong, DonVi
query = db.query(HoSoKhenThuong).join(DonVi)
```

---

## Kiểm tra lại

Chạy lệnh sau để test import thành công:

```bash
python -c "from app.api import export; print('Import export.py thanh cong!')"
```

**Kết quả mong đợi:**
```
Database URL: mysql+pymysql://root:1111@localhost:3306/khen_thuong_db?charset=utf8mb4
Import export.py thanh cong!
```

---

## Khởi động server

```bash
python main.py
```

Server sẽ chạy tại: http://localhost:8000

---

## File đã sửa

- ✅ `app/api/export.py` (dòng 33-34, và tất cả các dòng sử dụng HoSo)
  - Import đúng `get_current_user` từ `auth.py`
  - Đổi tên model từ `HoSo` → `HoSoKhenThuong`

---

**Lỗi đã được fix hoàn toàn!** Server có thể chạy bình thường.
