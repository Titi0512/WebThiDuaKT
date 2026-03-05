# Cập nhật lần 3 - Sửa lỗi và cải thiện

## Ngày: 05/03/2026

---

## Các vấn đề đã sửa

### 1. ✅ Thêm Quản lý tài khoản vào menu Danh mục

**Vấn đề:** Menu "Quản lý tài khoản" cần được tổ chức tốt hơn

**Giải pháp:**
- Di chuyển "Quản lý tài khoản" vào dropdown "Danh mục"
- Thêm dấu phân cách (divider) trước mục admin-only
- Thêm icon cho các mục trong dropdown

**File thay đổi:** `app/templates/base.html`

**Cấu trúc menu mới:**
```
Danh mục ▼
├── 🏢 Quản lý đơn vị
├── 🏆 Danh hiệu & Hình thức
├── ─────────────────── (chỉ hiện với ADMIN)
└── 👥 Quản lý tài khoản (chỉ hiện với ADMIN)
```

**Lợi ích:**
- Menu gọn gàng, dễ tìm hơn
- Nhóm các chức năng quản lý lại với nhau
- Phân quyền rõ ràng

---

### 2. ✅ Sửa lỗi nút "Hiện menu" không xuất hiện

**Vấn đề:** 
- Khi ẩn sidebar, không có nút để hiện lại
- CSS selector không hoạt động do cấu trúc HTML

**Nguyên nhân:**
```css
/* CSS cũ - KHÔNG HOẠT ĐỘNG */
.sidebar.collapsed ~ .sidebar-show-btn {
    display: flex;
}
```
Selector `~` (sibling) không tìm thấy vì `.sidebar-show-btn` không phải là sibling của `.sidebar`

**Giải pháp:**
1. Thay đổi CSS selector:
```css
/* CSS mới - SỬ DỤNG CLASS */
.sidebar-show-btn.show {
    display: flex;
}
```

2. Cập nhật JavaScript để toggle class:
```javascript
// Khi ẩn sidebar
if (sidebar.classList.contains('collapsed')) {
    sidebarShowBtn.classList.add('show');  // Hiện nút
}

// Khi hiện sidebar
sidebarShowBtn.classList.remove('show');  // Ẩn nút
```

**File thay đổi:**
- `app/templates/don_vi_detail.html` - CSS
- `app/static/js/don_vi_detail.js` - JavaScript

**Kết quả:**
- ✅ Click nút ẩn sidebar → Nút "Hiện menu" xuất hiện
- ✅ Click nút "Hiện menu" → Sidebar hiện lại, nút biến mất
- ✅ Hoạt động mượt mà với animation

---

### 3. ✅ Cải thiện nút thêm hồ sơ theo phân quyền

**Vấn đề:** 
- Các nút "Thêm hồ sơ" chỉ hiện với đơn vị của user
- ADMIN và LANH_DAO không thể thêm hồ sơ cho đơn vị khác

**Giải pháp:**

#### Logic phân quyền mới:

| Vai trò | Xem đơn vị | Thấy nút thêm | Có thể tạo hồ sơ |
|---------|------------|---------------|------------------|
| **ADMIN** | Tất cả | Tất cả | Tất cả đơn vị ✅ |
| **LANH_DAO** | Tất cả | Tất cả | Tất cả đơn vị ✅ |
| **CAN_BO** | Đơn vị mình | Chỉ đơn vị mình | Chỉ đơn vị mình |
| **USER** | Đơn vị mình | Chỉ đơn vị mình | Chỉ đơn vị mình |
| **VIEW_ONLY** | Đơn vị mình | Không bao giờ | Không ❌ |

#### Code mới:

**Hiển thị nút (don_vi_detail.js dòng 164-178):**
```javascript
const actionButtons = document.getElementById('actionButtons');
if (currentUser && currentUser.role !== 'VIEW_ONLY') {
    // ADMIN và LANH_DAO: thấy nút ở mọi đơn vị
    if (currentUser.role === 'ADMIN' || currentUser.role === 'LANH_DAO') {
        actionButtons.style.display = 'flex';
    } 
    // USER và CAN_BO: chỉ thấy nút ở đơn vị của mình
    else if (currentUser.don_vi_id === unitId) {
        actionButtons.style.display = 'flex';
    } else {
        actionButtons.style.display = 'none';
    }
} else {
    actionButtons.style.display = 'none';
}
```

**Kiểm tra quyền khi tạo (dòng 370-390):**
```javascript
function addPersonalRecord() {
    // Không cho phép VIEW_ONLY
    if (!currentUser || currentUser.role === 'VIEW_ONLY') {
        showToast('Bạn không có quyền thêm hồ sơ', 'error');
        return;
    }
    
    // USER và CAN_BO chỉ tạo cho đơn vị mình
    if ((currentUser.role === 'USER' || currentUser.role === 'CAN_BO') 
        && currentUser.don_vi_id !== currentUnitId) {
        showToast('Bạn chỉ có thể thêm hồ sơ cho đơn vị của mình', 'error');
        return;
    }
    
    // ADMIN và LANH_DAO: Không bị chặn, có thể tạo cho mọi đơn vị
    window.location.href = `/ho-so?don_vi_id=${currentUnitId}&loai_ho_so=ca_nhan`;
}
```

**File thay đổi:** `app/static/js/don_vi_detail.js`

**Lợi ích:**
- ✅ ADMIN có toàn quyền quản lý mọi đơn vị
- ✅ LANH_DAO có thể tạo hồ sơ cho bất kỳ đơn vị nào
- ✅ USER/CAN_BO giới hạn trong đơn vị của mình
- ✅ VIEW_ONLY không thể tạo hồ sơ
- ✅ Phù hợp với workflow thực tế

---

### 4. ✅ Sửa lỗi hiển thị menu admin-only

**Vấn đề:**
- Code set `display: 'block'` cho các item trong dropdown
- List item (`<li>`) không nên dùng `display: block`

**Giải pháp:**
```javascript
// Cũ
item.style.display = 'block';  // ❌ Sai

// Mới  
item.style.display = '';  // ✅ Đúng - khôi phục display mặc định
```

**File thay đổi:** `app/static/js/app.js` (dòng 114-121)

**Kết quả:**
- Menu hiển thị đúng định dạng
- Không bị lỗi layout

---

## Tóm tắt các file đã thay đổi

| File | Thay đổi | Dòng |
|------|----------|------|
| `app/templates/base.html` | Menu quản lý tài khoản vào dropdown | 51-56 |
| `app/templates/don_vi_detail.html` | Sửa CSS cho nút show | 116-119 |
| `app/static/js/app.js` | Sửa hiển thị admin menu | 114-121 |
| `app/static/js/don_vi_detail.js` | Sửa logic nút show | 49-77 |
| `app/static/js/don_vi_detail.js` | Cải thiện phân quyền nút thêm | 164-178 |
| `app/static/js/don_vi_detail.js` | Cập nhật hàm thêm hồ sơ | 370-415 |

---

## Hướng dẫn kiểm tra

### Test 1: Menu Quản lý tài khoản

1. **Đăng nhập với ADMIN:**
   - ✅ Vào menu "Danh mục"
   - ✅ Thấy dấu gạch ngang (divider)
   - ✅ Thấy mục "👥 Quản lý tài khoản"
   - ✅ Click vào → Mở trang quản lý users

2. **Đăng nhập với USER:**
   - ✅ Vào menu "Danh mục"
   - ✅ KHÔNG thấy divider
   - ✅ KHÔNG thấy mục quản lý tài khoản
   - ✅ Chỉ thấy 2 mục: Quản lý đơn vị, Danh hiệu & Hình thức

### Test 2: Nút Hiện menu

1. Mở trang `/don-vi-chi-tiet` trên desktop
2. Click nút ẩn sidebar (◀)
   - ✅ Sidebar ẩn đi
   - ✅ Nội dung mở rộng
   - ✅ **Nút tròn màu xanh xuất hiện ở góc trên trái** 👈 MỚI
3. Click nút hiện menu
   - ✅ Sidebar hiện lại
   - ✅ Nút biến mất
   - ✅ Animation mượt mà

4. Resize xuống mobile
   - ✅ Nút tròn không hiển thị
   - ✅ Dùng nút hamburger menu thay thế

### Test 3: Nút thêm hồ sơ theo vai trò

#### Test với ADMIN:
1. Đăng nhập với tài khoản ADMIN
2. Vào trang Đơn vị
3. Chọn BẤT KỲ đơn vị nào
   - ✅ Thấy nút "Thêm hồ sơ cá nhân"
   - ✅ Thấy nút "Thêm hồ sơ tập thể"
4. Click nút → Trang tạo hồ sơ mở với đơn vị đã chọn
5. Thử tạo hồ sơ → ✅ Thành công

#### Test với LANH_DAO:
1. Đăng nhập với tài khoản LANH_DAO
2. Chọn bất kỳ đơn vị nào
   - ✅ Thấy nút thêm hồ sơ
3. Click → ✅ Có thể tạo hồ sơ cho đơn vị đó

#### Test với USER/CAN_BO:
1. Đăng nhập với USER (ví dụ: đơn vị ID = 5)
2. Chọn đơn vị của mình (ID = 5)
   - ✅ Thấy nút thêm hồ sơ
3. Chọn đơn vị khác (ID = 10)
   - ✅ KHÔNG thấy nút thêm
4. Thử tạo qua URL `/ho-so?don_vi_id=10`
   - ✅ Bị chặn bởi API với lỗi 403

#### Test với VIEW_ONLY:
1. Đăng nhập với VIEW_ONLY
2. Chọn bất kỳ đơn vị nào
   - ✅ KHÔNG BAO GIỜ thấy nút thêm
3. Thử URL trực tiếp → ✅ Bị chặn

---

## So sánh trước và sau

### Trước khi sửa:
- ❌ Menu "Quản lý tài khoản" nằm riêng lẻ
- ❌ Không có nút hiện sidebar khi đã ẩn
- ❌ ADMIN/LANH_DAO không thể thêm hồ sơ cho đơn vị khác
- ❌ Phân quyền chưa linh hoạt

### Sau khi sửa:
- ✅ Menu gọn gàng, có tổ chức
- ✅ Nút hiện/ẩn sidebar hoạt động hoàn hảo
- ✅ ADMIN/LANH_DAO quản lý được tất cả đơn vị
- ✅ Phân quyền linh hoạt theo vai trò
- ✅ UX tốt hơn, trực quan hơn

---

## Lưu ý khi sử dụng

### Quyền hạn của các vai trò:

**ADMIN (Quản trị viên):**
- ✅ Quản lý tài khoản người dùng
- ✅ Tạo hồ sơ cho MỌI đơn vị
- ✅ Sửa/Xóa mọi hồ sơ
- ✅ Toàn quyền hệ thống

**LANH_DAO (Lãnh đạo):**
- ✅ Xem tất cả hồ sơ
- ✅ Tạo hồ sơ cho MỌI đơn vị
- ✅ Phê duyệt hồ sơ
- ❌ Không quản lý tài khoản

**CAN_BO (Cán bộ):**
- ✅ Quản lý hồ sơ ĐƠN VỊ MÌNH
- ❌ Không tạo cho đơn vị khác

**USER (Người dùng):**
- ✅ Tạo hồ sơ cho ĐƠN VỊ MÌNH
- ❌ Giới hạn trong đơn vị

**VIEW_ONLY (Chỉ xem):**
- ✅ Chỉ xem thông tin
- ❌ Không thể tạo/sửa/xóa

---

## Các vấn đề đã khắc phục

1. ✅ Nút "Hiện menu" bây giờ hoạt động đúng
2. ✅ Menu admin được tổ chức tốt hơn
3. ✅ ADMIN/LANH_DAO có đủ quyền quản lý
4. ✅ Phân quyền chính xác theo vai trò
5. ✅ CSS display không còn lỗi

---

## Không có Breaking Changes

- ✅ Tương thích ngược với code cũ
- ✅ Không cần migration database
- ✅ Không cần cập nhật dependencies
- ✅ Chỉ cần restart server

---

## Kết luận

Tất cả 3 yêu cầu đã được hoàn thành:

1. ✅ **Quản lý tài khoản** - Đã thêm vào menu Danh mục với phân quyền ADMIN
2. ✅ **Nút hiện menu** - Đã sửa lỗi, hoạt động hoàn hảo
3. ✅ **Nút thêm hồ sơ** - Đã cải thiện phân quyền cho ADMIN/LANH_DAO

Hệ thống bây giờ hoạt động đúng với quy trình quản lý thực tế!
