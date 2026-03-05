# Changelog - Hệ thống quản lý khen thưởng

## Version 2.1 - 05/03/2026

### Tính năng mới

#### 1. Quản lý tài khoản người dùng (ADMIN)
- ✅ Trang quản lý tài khoản chỉ dành cho ADMIN
- ✅ Xem danh sách tất cả người dùng
- ✅ Lọc theo vai trò, đơn vị, trạng thái
- ✅ Thêm tài khoản mới với đầy đủ thông tin
- ✅ Chỉnh sửa thông tin tài khoản (trừ mật khẩu)
- ✅ Đặt lại mật khẩu cho người dùng
- ✅ Kích hoạt/Khóa tài khoản
- ✅ Xóa tài khoản (với xác nhận)
- ✅ Bảo vệ: Không thể xóa/khóa tài khoản của chính mình

**Trang:** `/users` (chỉ ADMIN)

**Cách sử dụng:**
1. Đăng nhập với tài khoản ADMIN
2. Click "Quản lý tài khoản" trong menu điều hướng
3. Sử dụng bộ lọc để tìm người dùng
4. Click nút thao tác tương ứng:
   - ✏️ Chỉnh sửa thông tin
   - 🔑 Đặt lại mật khẩu
   - 🔒 Khóa/Mở khóa tài khoản
   - 🗑️ Xóa tài khoản

#### 2. Cải thiện giao diện trang Đơn vị
- ✅ Nút "Hiện menu" xuất hiện khi sidebar bị ẩn (desktop)
- ✅ Nút floating ở góc trên bên trái
- ✅ Gradient màu xanh, dễ nhận biết
- ✅ Chỉ hiển thị trên desktop (ẩn trên mobile)

### API Changes

#### Endpoints mới
```
POST   /api/users/{id}/reset-password   - Đặt lại mật khẩu (ADMIN only)
POST   /api/users/{id}/toggle-status    - Kích hoạt/Khóa tài khoản (ADMIN only)
```

#### Cập nhật endpoints
```
DELETE /api/users/{id}                  - Thêm kiểm tra không thể xóa tài khoản của chính mình
```

### UI/UX Changes

#### Trang quản lý tài khoản
- ✅ Bảng hiển thị người dùng với đầy đủ thông tin
- ✅ Badge màu sắc phân biệt vai trò
- ✅ Badge trạng thái hoạt động/khóa
- ✅ Bộ lọc nhiều tiêu chí
- ✅ Modal tạo/sửa tài khoản với form validation
- ✅ Modal đặt lại mật khẩu với xác nhận
- ✅ Modal xác nhận xóa với cảnh báo màu đỏ

#### Menu điều hướng
- ✅ Link "Quản lý tài khoản" chỉ hiển thị cho ADMIN
- ✅ Tự động ẩn/hiện dựa trên role của user đăng nhập

#### JavaScript
- ✅ Thêm function `getCurrentUser()` trong `app.js`
- ✅ Tự động ẩn/hiện menu items có class `admin-only`

### Files Created/Modified

#### Tạo mới
```
app/templates/users.html      - Trang quản lý tài khoản
app/static/js/users.js        - Logic quản lý tài khoản
```

#### Cập nhật
```
main.py                       - Thêm route /users
app/templates/base.html       - Thêm link "Quản lý tài khoản"
app/static/js/app.js          - Thêm getCurrentUser(), cập nhật loadUserInfo()
app/static/css/style.css      - Thêm style cho nút "Hiện menu"
app/static/js/don_vi_detail.js - Thêm xử lý nút "Hiện menu"
```

### Security

#### Bảo mật tài khoản
- ✅ Chỉ ADMIN mới truy cập được trang quản lý tài khoản
- ✅ Client-side check: Redirect nếu không phải ADMIN
- ✅ Server-side check: API trả về 403 nếu không đủ quyền
- ✅ Không thể xóa tài khoản của chính mình
- ✅ Không thể khóa tài khoản của chính mình
- ✅ Xác nhận trước khi xóa tài khoản

#### Mật khẩu
- ✅ Mật khẩu tối thiểu 6 ký tự
- ✅ Hash mật khẩu bằng bcrypt
- ✅ Xác nhận mật khẩu khi đặt lại

### Testing

#### Test quản lý tài khoản
1. Login với tài khoản không phải ADMIN
   - Không thấy link "Quản lý tài khoản"
   - Truy cập trực tiếp /users → Redirect về dashboard
2. Login với tài khoản ADMIN
   - Thấy link "Quản lý tài khoản" trên menu
   - Click vào → Hiển thị danh sách người dùng
3. Test tạo tài khoản mới
   - Điền đầy đủ thông tin
   - Kiểm tra validation (email, username unique)
   - Tạo thành công → Xuất hiện trong danh sách
4. Test chỉnh sửa tài khoản
   - Sửa thông tin (tên, email, đơn vị, vai trò)
   - Lưu → Cập nhật thành công
5. Test đặt lại mật khẩu
   - Nhập mật khẩu mới
   - Xác nhận mật khẩu
   - Đặt lại thành công → Đăng xuất và đăng nhập lại với mật khẩu mới
6. Test khóa/mở khóa tài khoản
   - Khóa tài khoản → Badge chuyển sang "Đã khóa"
   - Đăng xuất, thử đăng nhập với tài khoản bị khóa → Không được
   - Mở khóa → Có thể đăng nhập lại
7. Test xóa tài khoản
   - Xóa tài khoản → Hiển thị modal xác nhận
   - Xác nhận xóa → Tài khoản biến mất khỏi danh sách
8. Test bảo vệ tài khoản của chính mình
   - Nút khóa/xóa của tài khoản ADMIN hiện tại bị disabled
   - Không thể khóa/xóa

#### Test nút "Hiện menu"
1. Mở trang Đơn vị
2. Click nút ẩn sidebar
3. Nút "Hiện menu" xuất hiện ở góc trên trái
4. Click nút → Sidebar hiển thị lại
5. Resize xuống mobile → Nút "Hiện menu" biến mất

### Known Issues
- ❌ Chưa có chức năng đổi mật khẩu cho chính mình (sẽ làm ở version sau)
- ❌ Chưa có log audit cho các thao tác quản lý tài khoản (sẽ làm ở version sau)

### Next Version (2.2) - Planned Features
- [ ] Tự đổi mật khẩu cho tài khoản của mình
- [ ] Audit log cho thao tác quản lý tài khoản
- [ ] Export danh sách người dùng
- [ ] Import người dùng từ CSV/Excel
- [ ] Thiết lập chính sách mật khẩu
- [ ] 2FA (Two-factor authentication)

---

## Version 2.0 - 05/03/2026

### Tính năng mới

#### 1. Chức năng ẩn/hiện danh sách đơn vị
- ✅ Thêm nút toggle trên sidebar danh sách đơn vị (desktop)
- ✅ Nút toggle di động cho màn hình nhỏ
- ✅ Animation mượt mà khi ẩn/hiện sidebar
- ✅ Tự động điều chỉnh nội dung chính khi sidebar ẩn/hiện

**Cách sử dụng:**
- Desktop: Click biểu tượng chevron (◀) ở góc phải header sidebar
- Mobile: Click nút menu (☰) ở góc trên bên trái

#### 2. Upload ảnh minh chứng cho hồ sơ khen thưởng
- ✅ Upload nhiều file cùng lúc
- ✅ Hỗ trợ định dạng: JPG, PNG, GIF, PDF, DOC, DOCX
- ✅ Giới hạn kích thước: 10MB mỗi file
- ✅ Hiển thị danh sách file đã upload với preview
- ✅ Xóa file đã upload
- ✅ API endpoints: 
  - `POST /api/ho-so/{id}/upload` - Upload file
  - `DELETE /api/ho-so/{id}/upload/{filename}` - Xóa file

**Cách sử dụng:**
1. Tạo hồ sơ mới và lưu
2. Chỉnh sửa hồ sơ vừa tạo
3. Phần "Ảnh minh chứng" sẽ hiển thị
4. Chọn file và upload
5. File sẽ được lưu tại `/static/uploads/`

#### 3. Phân quyền nâng cao

##### Role mới: VIEW_ONLY (Chỉ xem)
- ✅ Chỉ có quyền xem thông tin, không thể tạo/sửa/xóa
- ✅ Không thể upload/xóa file
- ✅ Thích hợp cho tài khoản giám sát, báo cáo

##### Cập nhật phân quyền USER
- ✅ USER chỉ có thể tạo hồ sơ cho đơn vị của mình
- ✅ USER chỉ có thể sửa/xóa hồ sơ do chính mình tạo
- ✅ USER chỉ nhìn thấy hồ sơ của đơn vị mình

##### Các role và quyền hạn:

| Role | Xem tất cả | Tạo hồ sơ | Sửa hồ sơ | Xóa hồ sơ | Duyệt hồ sơ | Upload file |
|------|------------|-----------|-----------|-----------|-------------|-------------|
| ADMIN | ✅ | ✅ (tất cả đơn vị) | ✅ (tất cả) | ✅ (tất cả) | ✅ | ✅ |
| LANH_DAO | ✅ | ✅ (tất cả đơn vị) | ✅ (tất cả) | ❌ | ✅ | ✅ |
| CAN_BO | ✅ (đơn vị) | ✅ (đơn vị) | ✅ (của mình) | ✅ (của mình) | ❌ | ✅ |
| USER | ✅ (đơn vị) | ✅ (chỉ đơn vị mình) | ✅ (của mình) | ✅ (của mình) | ❌ | ✅ |
| VIEW_ONLY | ✅ (đơn vị) | ❌ | ❌ | ❌ | ❌ | ❌ |

#### 4. Cải thiện giao diện

##### Sidebar đơn vị
- ✅ Header với nút toggle desktop
- ✅ Icon cho từng loại đơn vị
- ✅ Hover effect
- ✅ Active state cho đơn vị đang chọn

##### Form nhập liệu
- ✅ Layout rõ ràng, dễ sử dụng
- ✅ Validation tốt hơn
- ✅ Phần upload file với preview
- ✅ Hiển thị danh sách file đã upload

##### Hiển thị ảnh
- ✅ Preview ảnh trong danh sách file
- ✅ Icon phân biệt loại file (ảnh/document)
- ✅ Hiển thị kích thước file
- ✅ Link download file
- ✅ Responsive trên mobile

##### CSS improvements
- ✅ File upload area với drag & drop style
- ✅ File item với hover effect
- ✅ Animation cho sidebar toggle
- ✅ Responsive design tốt hơn

### API Changes

#### Endpoints mới
```
POST   /api/ho-so/{id}/upload          - Upload file cho hồ sơ
DELETE /api/ho-so/{id}/upload/{file}   - Xóa file của hồ sơ
```

#### Cập nhật endpoints
```
POST   /api/ho-so/                     - Thêm kiểm tra quyền theo đơn vị
PUT    /api/ho-so/{id}                 - Thêm kiểm tra quyền VIEW_ONLY
DELETE /api/ho-so/{id}                 - Thêm kiểm tra quyền VIEW_ONLY
```

### Database Changes

#### Models
- ✅ Thêm enum `VIEW_ONLY` vào `UserRole`
- ✅ Trường `file_dinh_kem` đã tồn tại, lưu dạng JSON

#### Storage
- ✅ Thư mục `app/static/uploads/` để lưu file upload
- ✅ File được đổi tên unique bằng UUID
- ✅ Metadata lưu trong database

### Breaking Changes
- ❌ Không có breaking changes
- ✅ Tương thích ngược với version cũ

### Migration Guide

#### Cập nhật code
```bash
# Pull latest code
git pull origin main

# Install dependencies (nếu có thêm)
pip install -r requirements.txt
```

#### Cập nhật database
```bash
# Không cần chạy migration, SQLAlchemy tự động cập nhật enum
# Chỉ cần restart server
python main.py
```

#### Tạo tài khoản VIEW_ONLY
```python
# Trong Python shell hoặc init_db.py
from app.models.models import User, UserRole
from app.core.database import SessionLocal
from app.core.security import get_password_hash

db = SessionLocal()
user = User(
    username="viewer",
    email="viewer@example.com",
    hashed_password=get_password_hash("password123"),
    ho_ten="Tài khoản xem",
    role=UserRole.VIEW_ONLY,
    don_vi_id=1,  # Chọn đơn vị
    is_active=True
)
db.add(user)
db.commit()
```

### Testing

#### Test upload file
1. Login với tài khoản USER hoặc cao hơn
2. Tạo hồ sơ mới
3. Sau khi lưu, mở lại hồ sơ để chỉnh sửa
4. Upload file ảnh hoặc document
5. Kiểm tra file hiển thị trong danh sách
6. Test xóa file
7. Kiểm tra file đã bị xóa khỏi server

#### Test phân quyền
1. Tạo tài khoản VIEW_ONLY
2. Login và thử tạo hồ sơ → Phải bị từ chối
3. Thử upload file → Phải bị từ chối
4. Login với USER role
5. Thử tạo hồ sơ cho đơn vị khác → Phải bị từ chối
6. Tạo hồ sơ cho đơn vị của mình → Thành công

#### Test sidebar toggle
1. Mở trang Đơn vị
2. Click nút toggle desktop → Sidebar ẩn/hiện
3. Resize trình duyệt xuống mobile size
4. Click nút menu mobile → Sidebar slide in/out
5. Click overlay → Sidebar đóng lại

### Known Issues
- ❌ Chưa hỗ trợ drag & drop để upload file (sẽ làm ở version sau)
- ❌ Chưa có preview ảnh full size (sẽ làm ở version sau)
- ❌ Chưa có progress bar khi upload file lớn (sẽ làm ở version sau)

### Next Version (2.1) - Planned Features
- [ ] Drag & drop upload files
- [ ] Image preview modal/lightbox
- [ ] Upload progress bar
- [ ] File compression trước khi upload
- [ ] Batch delete files
- [ ] Export hồ sơ với file đính kèm
- [ ] Email notification khi hồ sơ được duyệt

---

## Version 1.0 - Initial Release
- Quản lý đơn vị
- Quản lý hồ sơ khen thưởng cá nhân/tập thể
- Workflow phê duyệt
- Thống kê và báo cáo
- 4 roles: ADMIN, LANH_DAO, CAN_BO, USER
