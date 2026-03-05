# Hướng dẫn sử dụng - Tính năng mới

## 1. Ẩn/Hiện danh sách đơn vị

### Desktop (màn hình lớn)
1. Mở trang **Đơn vị** từ menu chính
2. Tìm nút mũi tên (◀) ở góc phải phần header của sidebar (bên cạnh chữ "Danh sách đơn vị")
3. Click vào nút này để ẩn/hiện sidebar
4. Khi sidebar ẩn, nội dung chính sẽ tự động mở rộng

### Mobile (màn hình nhỏ)
1. Click vào nút menu (☰) ở góc trên bên trái
2. Sidebar sẽ trượt vào từ bên trái
3. Click vào vùng tối (overlay) hoặc nút menu lại để đóng

---

## 2. Nhập thông tin và upload ảnh minh chứng

### Tạo hồ sơ mới

1. **Vào trang Hồ sơ khen thưởng**
   - Click menu "Hồ sơ khen thưởng" trên thanh menu

2. **Tạo hồ sơ**
   - Click nút "Tạo hồ sơ mới"
   - Chọn loại hồ sơ: Cá nhân hoặc Tập thể
   
3. **Nhập thông tin cá nhân (nếu chọn Cá nhân)**
   - Họ và tên (*)
   - Cấp bậc
   - Chức vụ
   
4. **Nhập thông tin tập thể (nếu chọn Tập thể)**
   - Tên tập thể (*)

5. **Nhập thông tin chung**
   - Đơn vị (*): Chọn từ danh sách
     - *Lưu ý: Tài khoản USER chỉ được chọn đơn vị của mình*
   - Danh hiệu thi đua: Tùy chọn
   - Hình thức khen thưởng: Tùy chọn
   - Năm khen thưởng (*): Nhập năm (VD: 2024)
   - Thành tích (*): Mô tả thành tích đạt được
   - Ghi chú: Thông tin bổ sung (nếu có)

6. **Lưu hồ sơ**
   - Click nút "Lưu"
   - Hồ sơ sẽ được tạo với trạng thái "Nháp"

### Upload ảnh minh chứng

1. **Mở hồ sơ vừa tạo**
   - Trong danh sách hồ sơ, click nút "Sửa" (biểu tượng bút)
   
2. **Phần Upload sẽ hiển thị**
   - Cuộn xuống phần "Ảnh minh chứng"
   - Click "Choose file" để chọn file
   
3. **Chọn file**
   - Có thể chọn nhiều file cùng lúc
   - Định dạng cho phép: JPG, PNG, GIF, PDF, DOC, DOCX
   - Kích thước tối đa: 10MB mỗi file
   
4. **Upload**
   - File sẽ tự động upload khi bạn chọn
   - Thông báo "Upload thành công" sẽ hiện ra
   - File sẽ xuất hiện trong danh sách bên dưới

5. **Quản lý file**
   - Click vào tên file để xem/tải về
   - Click nút thùng rác (🗑️) để xóa file
   - File ảnh sẽ có icon 🖼️, file document có icon 📄

### Tạo hồ sơ từ trang Đơn vị

1. Vào trang **Đơn vị**
2. Click chọn một đơn vị từ sidebar
3. Click nút "Thêm cá nhân" hoặc "Thêm tập thể"
4. Form sẽ tự động điền sẵn đơn vị và loại hồ sơ
5. Tiếp tục nhập thông tin như hướng dẫn trên

---

## 3. Phân quyền tài khoản

### Các loại tài khoản

#### ADMIN (Quản trị viên)
- ✅ Xem tất cả hồ sơ của mọi đơn vị
- ✅ Tạo hồ sơ cho bất kỳ đơn vị nào
- ✅ Sửa, xóa mọi hồ sơ
- ✅ Phê duyệt hồ sơ
- ✅ Upload/xóa file
- ✅ Quản lý người dùng, danh mục

#### LANH_DAO (Lãnh đạo)
- ✅ Xem tất cả hồ sơ
- ✅ Tạo hồ sơ cho bất kỳ đơn vị nào
- ✅ Sửa mọi hồ sơ
- ✅ Phê duyệt hồ sơ
- ✅ Upload/xóa file
- ❌ Không thể xóa hồ sơ

#### CAN_BO (Cán bộ)
- ✅ Xem hồ sơ của đơn vị mình
- ✅ Tạo hồ sơ cho đơn vị mình
- ✅ Sửa, xóa hồ sơ do mình tạo
- ✅ Upload/xóa file
- ❌ Không thể phê duyệt

#### USER (Người dùng)
- ✅ Xem hồ sơ của đơn vị mình
- ✅ **Chỉ tạo hồ sơ cho đơn vị của mình**
- ✅ Sửa, xóa hồ sơ do mình tạo
- ✅ Upload/xóa file
- ❌ Không thể phê duyệt
- ❌ **Không thể tạo hồ sơ cho đơn vị khác**

#### VIEW_ONLY (Chỉ xem) - MỚI
- ✅ Xem hồ sơ của đơn vị mình
- ❌ **Không thể tạo hồ sơ**
- ❌ **Không thể sửa hồ sơ**
- ❌ **Không thể xóa hồ sơ**
- ❌ **Không thể upload file**

### Giới hạn theo đơn vị

**Tài khoản USER:**
- Khi tạo hồ sơ, chỉ có thể chọn đơn vị của mình trong dropdown
- Nếu cố tình chọn đơn vị khác (qua API), sẽ bị lỗi: *"Bạn chỉ có thể tạo hồ sơ cho đơn vị của mình"*
- Chỉ nhìn thấy hồ sơ của đơn vị mình trong danh sách

**Tài khoản VIEW_ONLY:**
- Nút "Tạo hồ sơ mới" sẽ bị ẩn hoặc vô hiệu hóa
- Không thể click nút "Sửa", "Xóa"
- Không thể upload/xóa file
- Mọi thao tác chỉnh sửa sẽ bị chặn với thông báo: *"Tài khoản chỉ xem không có quyền..."*

---

## 4. Quản lý tài khoản (ADMIN)

### Truy cập trang quản lý

1. **Yêu cầu:** Phải đăng nhập với tài khoản ADMIN
2. **Vào trang:**
   - Click menu "Quản lý tài khoản" trên thanh điều hướng
   - Hoặc truy cập trực tiếp: `/users`
3. **Lưu ý:** Tài khoản không phải ADMIN sẽ không thấy menu này

### Xem danh sách người dùng

1. **Danh sách hiển thị:**
   - Tên đăng nhập
   - Họ và tên
   - Đơn vị
   - Vai trò (với màu sắc phân biệt)
   - Trạng thái (Hoạt động/Đã khóa)
   - Email
   - Các nút thao tác

2. **Lọc người dùng:**
   - **Theo vai trò:** Chọn ADMIN, LANH_DAO, CAN_BO, USER, VIEW_ONLY
   - **Theo đơn vị:** Chọn đơn vị cụ thể
   - **Theo trạng thái:** Đang hoạt động hoặc Đã khóa
   - Click "Tìm" để áp dụng bộ lọc

### Thêm tài khoản mới

1. **Click nút "Thêm tài khoản"**
2. **Nhập thông tin bắt buộc (*)**
   - Tên đăng nhập (*): Chỉ chữ cái, số, dấu gạch dưới
   - Mật khẩu (*): Tối thiểu 6 ký tự
   - Họ và tên (*)
   - Email (*): Phải đúng định dạng email
   - Đơn vị (*): Chọn từ danh sách
   - Vai trò (*): Chọn quyền phù hợp

3. **Nhập thông tin tùy chọn**
   - Cấp bậc
   - Chức vụ

4. **Click "Lưu"**
   - Hệ thống kiểm tra trùng username/email
   - Tài khoản được tạo với trạng thái "Hoạt động"
   - Thông báo "Thêm tài khoản thành công"

### Chỉnh sửa tài khoản

1. **Click nút bút chì (✏️) trên dòng tài khoản**
2. **Thông tin có thể sửa:**
   - Họ và tên
   - Email
   - Cấp bậc
   - Chức vụ
   - Đơn vị
   - Vai trò

3. **Thông tin KHÔNG thể sửa:**
   - Tên đăng nhập (readonly)
   - Mật khẩu (dùng chức năng "Đặt lại mật khẩu")

4. **Click "Lưu"** để cập nhật

### Đặt lại mật khẩu

1. **Click nút chìa khóa (🔑)**
2. **Nhập thông tin:**
   - Mật khẩu mới (*): Tối thiểu 6 ký tự
   - Xác nhận mật khẩu (*): Phải trùng với mật khẩu mới

3. **Click "Đặt lại mật khẩu"**
   - Mật khẩu được cập nhật ngay lập tức
   - Người dùng phải đăng nhập lại với mật khẩu mới

### Khóa/Mở khóa tài khoản

1. **Click nút khóa (🔒) hoặc mở khóa (🔓)**
2. **Xác nhận thao tác**
3. **Kết quả:**
   - **Khóa:** Tài khoản không thể đăng nhập
   - **Mở khóa:** Tài khoản có thể đăng nhập trở lại

4. **Lưu ý:**
   - Không thể khóa tài khoản của chính mình
   - Nút sẽ bị vô hiệu hóa (disabled) cho tài khoản hiện tại

### Xóa tài khoản

1. **Click nút thùng rác (🗑️)**
2. **Xác nhận trong modal màu đỏ:**
   - ⚠️ **Cảnh báo:** Hành động này không thể hoàn tác!
   - Kiểm tra kỹ tên tài khoản trước khi xóa

3. **Click "Xóa"** để xác nhận
4. **Tài khoản bị xóa vĩnh viễn**

5. **Lưu ý:**
   - Không thể xóa tài khoản của chính mình
   - Nút sẽ bị vô hiệu hóa (disabled) cho tài khoản hiện tại
   - Nên khóa tài khoản thay vì xóa để giữ lịch sử

### Màu sắc vai trò

- 🔴 **ADMIN** (Quản trị viên): Badge đỏ
- 🟡 **LANH_DAO** (Lãnh đạo): Badge vàng
- 🔵 **CAN_BO** (Cán bộ): Badge xanh dương
- 🟢 **USER** (Người dùng): Badge xanh lá
- ⚫ **VIEW_ONLY** (Chỉ xem): Badge xám

### Trạng thái tài khoản

- ✅ **Hoạt động**: Badge xanh lá, có thể đăng nhập
- 🔒 **Đã khóa**: Badge xám, không thể đăng nhập

---

## 5. Workflow sử dụng hoàn chỉnh

### Quy trình đơn vị tạo hồ sơ

1. **Cán bộ đơn vị (USER) tạo hồ sơ**
   - Đăng nhập với tài khoản USER
   - Tạo hồ sơ cho đơn vị của mình
   - Upload ảnh minh chứng
   - Lưu với trạng thái "Nháp"

2. **Kiểm tra và trình duyệt**
   - Kiểm tra lại thông tin
   - Click "Trình duyệt" để gửi lên cấp trên
   - Trạng thái chuyển sang "Chờ duyệt"

3. **Lãnh đạo phê duyệt**
   - Đăng nhập với tài khoản LANH_DAO
   - Xem danh sách hồ sơ "Chờ duyệt"
   - Xem chi tiết và ảnh minh chứng
   - Chọn "Phê duyệt" hoặc "Từ chối"

4. **Hoàn tất**
   - Hồ sơ chuyển sang "Đã duyệt" hoặc "Từ chối"
   - Nếu từ chối, USER có thể sửa và trình lại

### Quy trình giám sát (VIEW_ONLY)

1. **Tài khoản chỉ xem**
   - Đăng nhập với tài khoản VIEW_ONLY
   - Xem danh sách hồ sơ của đơn vị
   - Xem chi tiết hồ sơ
   - Tải về file minh chứng
   - Xuất báo cáo (nếu có)

2. **Không thể chỉnh sửa**
   - Không có nút "Tạo", "Sửa", "Xóa"
   - Chỉ xem thông tin read-only

---

## 6. Lưu ý quan trọng

### Về upload file
- ⚠️ Phải **lưu hồ sơ trước** mới có thể upload file
- ⚠️ File không thể upload khi tạo hồ sơ mới
- ⚠️ Mở lại hồ sơ (Sửa) để thấy phần upload
- ⚠️ Kích thước file tối đa: 10MB
- ⚠️ File được lưu vĩnh viễn, ngay cả khi hồ sơ chưa được duyệt

### Về phân quyền
- ⚠️ USER **không thể** tạo hồ sơ cho đơn vị khác
- ⚠️ VIEW_ONLY **không thể** làm gì ngoài xem
- ⚠️ Chỉ người tạo hoặc ADMIN mới xóa được hồ sơ
- ⚠️ Hồ sơ đã duyệt không thể xóa (trừ ADMIN)

### Về trạng thái hồ sơ
- **Nháp**: Có thể sửa, xóa, upload file
- **Chờ duyệt**: Không thể sửa (trừ ADMIN/LANH_DAO)
- **Đang xử lý**: Đang được xem xét
- **Đã duyệt**: Không thể sửa/xóa
- **Từ chối**: Có thể sửa lại và trình lại

---

## 7. Câu hỏi thường gặp (FAQ)

**Q: Tại sao tôi không thấy phần upload file?**
A: Bạn phải lưu hồ sơ trước, sau đó mở lại để chỉnh sửa. Phần upload chỉ hiện khi sửa hồ sơ đã tồn tại.

**Q: Tại sao tôi không thể tạo hồ sơ cho đơn vị khác?**
A: Nếu bạn là USER, bạn chỉ được tạo hồ sơ cho đơn vị của mình. Liên hệ ADMIN để được nâng quyền.

**Q: Làm sao để ẩn sidebar đơn vị?**
A: Click vào biểu tượng mũi tên (◀) ở header của sidebar (desktop) hoặc nút menu (☰) trên mobile.

**Q: File upload lưu ở đâu?**
A: File lưu tại thư mục `app/static/uploads/` trên server.

**Q: Có thể upload file khi hồ sơ đang chờ duyệt không?**
A: Có, bạn vẫn có thể upload/xóa file ngay cả khi hồ sơ đang chờ duyệt.

**Q: Tài khoản VIEW_ONLY dùng để làm gì?**
A: Dùng cho người chỉ cần xem thông tin, không cần chỉnh sửa. VD: Ban giám sát, kiểm tra.

**Q: Làm sao để tạo tài khoản VIEW_ONLY?**
A: Chỉ ADMIN mới có thể tạo. Liên hệ quản trị viên hệ thống.

**Q: Tại sao tôi không thấy menu "Quản lý tài khoản"?**
A: Menu này chỉ hiển thị cho tài khoản ADMIN. Nếu bạn cần quản lý người dùng, liên hệ ADMIN để được cấp quyền.

**Q: Có thể xóa hoặc khóa tài khoản của chính mình không?**
A: Không. Hệ thống tự động vô hiệu hóa các nút này để tránh khóa/xóa nhầm tài khoản đang dùng.

**Q: Tài khoản bị khóa có thể đăng nhập không?**
A: Không. Tài khoản bị khóa sẽ không thể đăng nhập cho đến khi ADMIN mở khóa lại.

**Q: Xóa tài khoản có thể hoàn tác không?**
A: Không. Việc xóa tài khoản là vĩnh viễn. Nên khóa tài khoản thay vì xóa để giữ lại lịch sử.

**Q: Mật khẩu mặc định khi tạo tài khoản mới là gì?**
A: Không có mật khẩu mặc định. ADMIN phải nhập mật khẩu khi tạo tài khoản mới.

**Q: Người dùng có thể tự đổi mật khẩu không?**
A: Chưa có chức năng này trong phiên bản hiện tại. Phải nhờ ADMIN đặt lại mật khẩu.

---

## Liên hệ hỗ trợ

Nếu gặp vấn đề hoặc cần hỗ trợ, vui lòng liên hệ:
- 📧 Email: support@example.com
- 📞 Hotline: 0123-456-789
- 🌐 Website: https://example.com
