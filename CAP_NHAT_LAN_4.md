# CẬP NHẬT LẦN 4 - FIX LỖI & THÊM TÍNH NĂNG XUẤT FILE

**Ngày cập nhật:** 05/03/2026

## Tổng quan

Cập nhật này bao gồm:
1. ✅ Sửa lỗi menu quản lý tài khoản không hiển thị
2. ✅ Sửa lỗi nút thêm hồ sơ khen thưởng không hiển thị
3. ✅ Thêm tính năng xuất file Excel, Word, PDF
4. ✅ Chỉnh sửa giao diện đơn vị cho đầy màn hình

---

## I. SỬA LỖI

### 1. Menu Quản lý Tài khoản Không Hiển thị

**Vấn đề:** Menu "Quản lý tài khoản" trong dropdown "Danh mục" không hiển thị cho ADMIN.

**Nguyên nhân:** 
- HTML có `style="display: none;"` inline làm CSS !important override
- JavaScript không xử lý đúng với `<li>` element trong dropdown

**Giải pháp:**

**File: `app/templates/base.html` (dòng 47-57)**
```html
<!-- Xóa style inline, chỉ dùng class -->
<li class="admin-only"><hr class="dropdown-divider"></li>
<li class="admin-only"><a class="dropdown-item" href="/users">...</a></li>
```

**File: `app/static/css/style.css` (thêm dòng 17-20)**
```css
/* Admin-only menu items - hidden by default, shown by JavaScript */
.admin-only {
    display: none !important;
}
```

**File: `app/static/js/app.js` (dòng 113-122)**
```javascript
adminMenuItems.forEach(item => {
    if (user.role === 'ADMIN') {
        // Use block for li elements to restore default display
        item.style.display = item.tagName === 'LI' ? 'block' : '';
    } else {
        item.style.display = 'none';
    }
});
```

---

### 2. Nút Thêm Hồ Sơ Không Hiển thị

**Vấn đề:** Nút "Thêm hồ sơ cá nhân" và "Thêm hồ sơ tập thể" không hiển thị khi chọn đơn vị.

**Nguyên nhân:**
- Biến `currentUser` có thể null khi trang load
- User info chưa được load từ localStorage hoặc API

**Giải pháp:**

**File: `app/static/js/don_vi_detail.js` (dòng 11-28)**
```javascript
document.addEventListener('DOMContentLoaded', async function() {
    // ... existing code ...
    
    // Get current user info from localStorage first
    const userStr = localStorage.getItem('user');
    if (userStr) {
        currentUser = JSON.parse(userStr);
    }
    
    // If not in localStorage, load from API
    if (!currentUser) {
        try {
            currentUser = await apiCall('/auth/me');
            localStorage.setItem('user', JSON.stringify(currentUser));
        } catch (error) {
            console.error('Error loading user:', error);
            window.location.href = '/login';
            return;
        }
    }
    
    console.log('Current user loaded:', currentUser); // Debug log
    
    // ... rest of code ...
});
```

**File: `app/static/js/don_vi_detail.js` (dòng 164-188)**
```javascript
// Thêm debug logging và kiểm tra null
const actionButtons = document.getElementById('actionButtons');

console.log('Checking permissions for unit:', unitId); // Debug
console.log('Current user:', currentUser); // Debug

if (!currentUser) {
    console.warn('No current user found');
    actionButtons.style.display = 'none';
    return;
}

if (currentUser.role === 'VIEW_ONLY') {
    console.log('User is VIEW_ONLY, hiding action buttons');
    actionButtons.style.display = 'none';
} else if (currentUser.role === 'ADMIN' || currentUser.role === 'LANH_DAO') {
    console.log('User is ADMIN/LANH_DAO, showing action buttons');
    actionButtons.style.display = 'flex';
} else if (currentUser.don_vi_id === unitId) {
    console.log('User can manage their own unit, showing action buttons');
    actionButtons.style.display = 'flex';
} else {
    console.log('User cannot manage this unit, hiding action buttons');
    actionButtons.style.display = 'none';
}
```

---

## II. TÍNH NĂNG MỚI: XUẤT FILE

### 1. Cài đặt Thư viện Python

**File: `requirements.txt`**
```bash
# Đã có sẵn
openpyxl==3.1.2      # Excel
reportlab==4.0.7     # PDF

# Thêm mới
python-docx==1.1.0   # Word
```

**Cài đặt:**
```bash
pip install python-docx==1.1.0
```

---

### 2. API Endpoints Xuất File

**File mới: `app/api/export.py`**

Tạo 3 endpoints:
- `GET /api/export/excel` - Xuất Excel (.xlsx)
- `GET /api/export/word` - Xuất Word (.docx)
- `GET /api/export/pdf` - Xuất PDF (.pdf)

**Tham số query string:**
- `don_vi_id` (optional): Lọc theo đơn vị
- `loai_ho_so` (optional): `ca_nhan` hoặc `tap_the`
- `nam_khen_thuong` (optional): Năm khen thưởng
- `trang_thai` (optional): Trạng thái hồ sơ

**Ví dụ:**
```
GET /api/export/excel?don_vi_id=1&loai_ho_so=ca_nhan&nam_khen_thuong=2025
```

**Quyền hạn:**
- ADMIN, LANH_DAO: Xuất tất cả hồ sơ (theo filter)
- USER, CAN_BO: Chỉ xuất hồ sơ của đơn vị mình
- VIEW_ONLY: Chỉ xem, không xuất

---

### 3. Đăng ký Router

**File: `main.py` (dòng 10, 45)**
```python
from app.api import auth, users, don_vi, danh_hieu, hinh_thuc, ho_so, thong_ke, export

# ...

app.include_router(export.router, prefix="/api")
```

---

### 4. Giao diện Nút Xuất File

**File: `app/templates/ho_so_list.html` (dòng 7-23)**
```html
<div class="col-md-6 text-end">
    <!-- Export buttons -->
    <div class="btn-group me-2" role="group">
        <button type="button" class="btn btn-outline-success" onclick="exportExcel()">
            <i class="bi bi-file-earmark-excel me-1"></i>Excel
        </button>
        <button type="button" class="btn btn-outline-primary" onclick="exportWord()">
            <i class="bi bi-file-earmark-word me-1"></i>Word
        </button>
        <button type="button" class="btn btn-outline-danger" onclick="exportPDF()">
            <i class="bi bi-file-earmark-pdf me-1"></i>PDF
        </button>
    </div>
    <button class="btn btn-primary" ...>
        <i class="bi bi-plus-circle me-2"></i>Tạo hồ sơ mới
    </button>
</div>
```

---

### 5. JavaScript Xuất File

**File: `app/static/js/ho_so.js` (thêm cuối file)**

**Hàm chính:**
- `exportExcel()` - Tải file Excel
- `exportWord()` - Tải file Word  
- `exportPDF()` - Tải file PDF
- `getExportParams()` - Lấy tham số filter hiện tại

**Luồng hoạt động:**
1. Lấy tham số filter từ form (loại hồ sơ, trạng thái, năm)
2. Gọi API với token authentication
3. Download file blob về máy
4. Hiển thị thông báo thành công/lỗi

**Ví dụ code:**
```javascript
async function exportExcel() {
    try {
        const params = getExportParams();
        const token = localStorage.getItem('token');
        
        const url = `/api/export/excel?${params}`;
        
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Xuất file thất bại');
        }
        
        // Download file
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `danh_sach_khen_thuong_${new Date().getTime()}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        a.remove();
        
        showSuccess('Xuất file Excel thành công');
    } catch (error) {
        showError('Lỗi xuất file Excel: ' + error.message);
    }
}
```

---

### 6. Định dạng File Xuất

#### **Excel (.xlsx)**
- Tiêu đề: "DANH SÁCH HỒ SƠ KHEN THƯỞNG" (font xanh, bold, size 16)
- Ngày xuất ở dòng 2
- Header với background xanh (#0066CC), chữ trắng, bold
- 10 cột: STT, Mã hồ sơ, Loại, Tên, Đơn vị, Danh hiệu, Hình thức, Năm, Trạng thái, Ghi chú
- Border cho tất cả cells
- Tự động điều chỉnh độ rộng cột

#### **Word (.docx)**
- Tiêu đề căn giữa, màu xanh
- Table với style "Light Grid Accent 1"
- 9 cột (không có Ghi chú do giới hạn chiều ngang)
- Header bold

#### **PDF (.pdf)**
- Khổ A4 ngang (landscape)
- Font Helvetica
- Header xanh (#0066CC), chữ trắng
- Row backgrounds xen kẽ (trắng/xám nhạt)
- Dữ liệu được rút gọn để vừa khổ giấy

---

## III. GIAO DIỆN ĐƠN VỊ FULLSCREEN

**File: `app/templates/don_vi_detail.html`**

**Thay đổi:**

1. **Xóa padding container** (dòng 223):
```html
{% block main_class %}p-0{% endblock %}
```

2. **CSS fullscreen** (dòng 6-12):
```css
body {
    overflow-x: hidden;
}

.sidebar {
    height: calc(100vh - 56px);
    /* ... */
}

.main-content {
    margin-left: 280px;
    padding: 20px;
    transition: margin-left 0.3s ease-in-out;
    min-height: calc(100vh - 56px);  /* Full viewport height */
    background: #f8f9fa;
}
```

3. **Ẩn footer** (thêm sau dòng 460):
```html
{% block footer %}
<!-- No footer on this page for fullscreen experience -->
{% endblock %}
```

**Kết quả:**
- Sidebar chiếm full chiều cao viewport
- Main content chiếm toàn bộ không gian còn lại
- Không có margin/padding thừa
- Footer bị ẩn để tối ưu không gian

---

## IV. KIỂM TRA & TESTING

### Test 1: Menu Quản lý Tài khoản

**Bước 1:** Đăng nhập với tài khoản ADMIN
```
Username: admin
Password: admin123
```

**Bước 2:** Click vào menu "Danh mục" ở navbar

**Kết quả mong đợi:**
- ✅ Thấy item "Quản lý đơn vị"
- ✅ Thấy item "Danh hiệu & Hình thức"
- ✅ Thấy đường kẻ divider
- ✅ Thấy item "Quản lý tài khoản" (với icon người dùng)

**Bước 3:** Đăng nhập với tài khoản USER
```
Username: user1
```

**Kết quả mong đợi:**
- ✅ Thấy 2 item đầu
- ✅ KHÔNG thấy divider và "Quản lý tài khoản"

---

### Test 2: Nút Thêm Hồ Sơ

**Bước 1:** Đăng nhập với tài khoản ADMIN

**Bước 2:** Vào trang "Đơn vị" → Chọn bất kỳ đơn vị nào

**Kết quả mong đợi:**
- ✅ Console log: "Current user loaded: {role: 'ADMIN', ...}"
- ✅ Console log: "User is ADMIN/LANH_DAO, showing action buttons"
- ✅ Hiển thị 2 nút: "Thêm hồ sơ cá nhân" và "Thêm hồ sơ tập thể" (màu xanh lá và xanh dương)

**Bước 3:** Đăng nhập với tài khoản USER (đơn vị: Khoa Chính trị - ID: 14)

**Bước 4:** Chọn đơn vị "Khoa Chính trị"

**Kết quả mong đợi:**
- ✅ Hiển thị nút thêm hồ sơ

**Bước 5:** Chọn đơn vị khác (VD: Khoa Quân sự chung)

**Kết quả mong đợi:**
- ✅ KHÔNG hiển thị nút thêm hồ sơ
- ✅ Console log: "User cannot manage this unit, hiding action buttons"

---

### Test 3: Xuất File Excel

**Bước 1:** Đăng nhập, vào trang "Hồ sơ khen thưởng"

**Bước 2:** Chọn filter (tuỳ chọn):
- Loại: Cá nhân
- Trạng thái: Đã duyệt
- Năm: 2025

**Bước 3:** Click nút "Excel" (màu xanh lá)

**Kết quả mong đợi:**
- ✅ Toast thông báo "Xuất file Excel thành công"
- ✅ File tải về tên: `danh_sach_khen_thuong_[timestamp].xlsx`
- ✅ Mở file Excel:
  - Tiêu đề màu xanh
  - Header có background xanh, chữ trắng
  - Dữ liệu đầy đủ theo filter
  - Các cột có độ rộng phù hợp

---

### Test 4: Xuất File Word & PDF

**Tương tự Test 3** với:
- Word: File `.docx`, table có style đẹp
- PDF: File `.pdf`, khổ A4 ngang, dữ liệu rút gọn

---

### Test 5: Giao diện Fullscreen

**Bước 1:** Vào trang "Đơn vị"

**Bước 2:** Chọn 1 đơn vị bất kỳ

**Kết quả mong đợi:**
- ✅ Sidebar chiếm full chiều cao màn hình (trừ navbar)
- ✅ Main content chiếm toàn bộ phần còn lại
- ✅ Không có footer
- ✅ Không có khoảng trắng thừa ở trên/dưới
- ✅ Scroll chỉ trong sidebar và main content, không scroll cả trang

**Bước 3:** Click nút ẩn sidebar (chevron bên trái)

**Kết quả mong đợi:**
- ✅ Sidebar slide sang trái biến mất
- ✅ Main content expand chiếm full width
- ✅ Nút tròn xanh "Hiện menu" xuất hiện ở góc trên trái

---

## V. HƯỚNG DẪN DEPLOY

### 1. Cài đặt Dependencies

```bash
cd D:\Codes\WebThiDuaKT
pip install -r requirements.txt
```

### 2. Clear Browser Cache

**Lý do:** Trình duyệt có thể cache JavaScript/CSS cũ

**Cách 1: Hard Refresh**
- Windows: `Ctrl + Shift + R` hoặc `Ctrl + F5`
- Mac: `Cmd + Shift + R`

**Cách 2: Clear Cache**
- Chrome: Settings → Privacy → Clear browsing data → Cached images and files
- Firefox: Options → Privacy → Clear Data → Cached Web Content

### 3. Khởi động Server

```bash
python main.py
```

Server chạy tại: http://localhost:8000

### 4. Test Từng Tính năng

Làm theo các test case ở phần IV.

---

## VI. TROUBLESHOOTING

### Vấn đề 1: Menu ADMIN vẫn không hiện

**Nguyên nhân:** Cache hoặc token cũ

**Giải pháp:**
1. Clear browser cache (Ctrl + Shift + R)
2. Logout → Login lại
3. F12 → Console → Check error
4. Kiểm tra: `localStorage.getItem('user')` → Phải có `role: "ADMIN"`

### Vấn đề 2: Nút "Thêm hồ sơ" không hiện

**Kiểm tra:**
1. F12 → Console → Xem debug logs:
   ```
   Current user loaded: {role: '...', don_vi_id: ...}
   Checking permissions for unit: ...
   ```

2. Nếu thấy "No current user found":
   - Logout → Login lại
   - Check token: `localStorage.getItem('token')`

3. Nếu thấy "User cannot manage this unit":
   - Kiểm tra `currentUser.don_vi_id` === `unitId`
   - ADMIN/LANH_DAO luôn thấy nút

### Vấn đề 3: Xuất file bị lỗi 401 Unauthorized

**Nguyên nhân:** Token hết hạn hoặc không gửi

**Giải pháp:**
1. Check token: `localStorage.getItem('token')`
2. Login lại để refresh token
3. F12 → Network → Click Export → Check Request Headers → Phải có `Authorization: Bearer ...`

### Vấn đề 4: File Excel/Word/PDF bị lỗi format

**Nguyên nhân:** Thiếu thư viện Python

**Giải pháp:**
```bash
pip install openpyxl python-docx reportlab
```

Restart server sau khi cài.

### Vấn đề 5: Import error `app.api.export`

**Nguyên nhân:** File `export.py` chưa được tạo hoặc sai vị trí

**Giải pháp:**
1. Check file tồn tại: `D:\Codes\WebThiDuaKT\app\api\export.py`
2. Check `__init__.py` trong `app/api/` (không bắt buộc với Python 3.3+)
3. Restart Python interpreter

---

## VII. TỔNG KẾT

### Các file đã sửa/thêm:

**Backend:**
- ✅ `requirements.txt` - Thêm python-docx
- ✅ `main.py` - Import và đăng ký export router
- ✅ `app/api/export.py` - **FILE MỚI** - API xuất Excel/Word/PDF

**Frontend - Templates:**
- ✅ `app/templates/base.html` - Sửa menu admin, thêm footer block
- ✅ `app/templates/ho_so_list.html` - Thêm nút xuất file
- ✅ `app/templates/don_vi_detail.html` - Fullscreen layout, ẩn footer

**Frontend - CSS:**
- ✅ `app/static/css/style.css` - Thêm `.admin-only { display: none !important; }`

**Frontend - JavaScript:**
- ✅ `app/static/js/app.js` - Fix hiển thị menu admin
- ✅ `app/static/js/don_vi_detail.js` - Fix load user, debug permission logic
- ✅ `app/static/js/ho_so.js` - Thêm 3 hàm export (Excel/Word/PDF)

**Documentation:**
- ✅ `CAP_NHAT_LAN_4.md` - **FILE NÀY**

---

## VIII. NEXT STEPS (Tùy chọn)

Các tính năng có thể phát triển thêm:

1. **Xuất file theo template:**
   - Cho phép admin upload template Word/Excel
   - Merge dữ liệu vào template

2. **Xuất file đính kèm:**
   - Tạo file ZIP chứa tất cả evidence files
   - Download cùng với danh sách hồ sơ

3. **Lịch sử xuất file:**
   - Lưu log khi user xuất file
   - Hiển thị "Ai đã xuất file gì, khi nào"

4. **Tùy chọn cột xuất:**
   - Cho phép user chọn cột nào muốn xuất
   - Lưu preset export template

5. **Watermark & chữ ký số:**
   - Thêm watermark vào PDF
   - Tích hợp chữ ký điện tử

---

**Hoàn thành:** 05/03/2026
**Người thực hiện:** OpenCode Assistant
**Phiên bản:** 2.3.0
