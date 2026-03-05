# Tính năng mới: Menu Đơn vị Chi tiết

## 📋 Tổng quan

Đã thêm trang mới **"Đơn vị"** với menu sidebar hiển thị danh sách tất cả các đơn vị, cho phép người dùng xem chi tiết danh sách cá nhân và tập thể được khen thưởng của từng đơn vị.

## ✨ Tính năng

### 1. **Sidebar Menu**
- Hiển thị danh sách đơn vị được phân loại theo 3 nhóm:
  - **Khối cơ quan** (12 đơn vị)
  - **Các khoa** (14 đơn vị)
  - **Đơn vị trực thuộc** (15 đơn vị)
- Hover effect và active state khi chọn đơn vị
- Responsive: Trên mobile sidebar hiển thị theo chiều dọc

### 2. **Thông tin Đơn vị**
Khi click vào một đơn vị, hiển thị:
- Tên đơn vị
- Mã đơn vị
- Loại đơn vị

### 3. **Thống kê nhanh** (4 cards)
- **Tổng hồ sơ**: Tổng số hồ sơ khen thưởng của đơn vị
- **Cá nhân**: Số lượng hồ sơ cá nhân
- **Tập thể**: Số lượng hồ sơ tập thể
- **Đã duyệt**: Số lượng hồ sơ đã được phê duyệt

### 4. **Hai Tab chi tiết**

#### Tab "Danh sách cá nhân"
Hiển thị bảng với các cột:
- STT
- Mã hồ sơ
- Họ tên (+ ngày sinh)
- Chức vụ
- Danh hiệu/Hình thức khen thưởng
- Năm khen thưởng
- Trạng thái (Đang nhập, Chờ duyệt, Đang duyệt, Đã duyệt, Từ chối)

#### Tab "Danh sách tập thể"
Hiển thị bảng với các cột:
- STT
- Mã hồ sơ
- Tên tập thể
- Danh hiệu/Hình thức khen thưởng
- Năm khen thưởng
- Số lượng thành viên
- Trạng thái

### 5. **Click để xem chi tiết**
- Click vào bất kỳ dòng nào trong bảng sẽ chuyển đến trang chi tiết hồ sơ

## 🛠️ Các file đã tạo/cập nhật

### Files mới:
1. **`app/templates/don_vi_detail.html`** - Template trang đơn vị chi tiết
2. **`app/static/js/don_vi_detail.js`** - JavaScript xử lý logic trang

### API Endpoint mới:
3. **`GET /api/don-vi/{don_vi_id}/thong-ke`** - Lấy thống kê của một đơn vị
   - Response:
     ```json
     {
       "don_vi": {
         "id": 1,
         "ma_don_vi": "VPT",
         "ten_don_vi": "Văn phòng Trường",
         "loai_don_vi": "khoi_co_quan"
       },
       "statistics": {
         "total": 25,
         "personal": 20,
         "collective": 5,
         "approved": 15
       }
     }
     ```

### Files đã cập nhật:
4. **`main.py`** - Thêm route `/don-vi-chi-tiet`
5. **`app/templates/base.html`** - Cập nhật navigation menu
6. **`app/api/don_vi.py`** - Thêm endpoint thống kê

## 🚀 Cách sử dụng

### 1. Truy cập trang
- Từ menu chính, click vào **"Đơn vị"** (icon building)
- Hoặc truy cập trực tiếp: `http://localhost:8000/don-vi-chi-tiet`

### 2. Chọn đơn vị
- Click vào bất kỳ đơn vị nào trong sidebar
- Đơn vị được chọn sẽ được highlight màu xanh

### 3. Xem thông tin
- Thống kê hiển thị ngay trên 4 cards màu sắc
- Chuyển giữa tab "Cá nhân" và "Tập thể" để xem danh sách tương ứng

### 4. Xem chi tiết hồ sơ
- Click vào bất kỳ dòng nào trong bảng
- Sẽ chuyển đến trang hồ sơ chi tiết với ID tương ứng

## 📱 Responsive Design

### Desktop (> 768px)
- Sidebar cố định bên trái (280px)
- Main content hiển thị bên phải
- Hiển thị đầy đủ tất cả thông tin

### Mobile (≤ 768px)
- Sidebar hiển thị full width phía trên
- Main content hiển thị full width phía dưới
- Bảng có thể scroll ngang

## 🎨 UI/UX Features

### 1. **Color-coded Statistics Cards**
- **Primary (Blue)**: Tổng hồ sơ
- **Success (Green)**: Cá nhân
- **Info (Light blue)**: Tập thể
- **Warning (Yellow)**: Đã duyệt

### 2. **Status Badges**
- Đang nhập: Secondary (gray)
- Chờ duyệt: Warning (yellow)
- Đang duyệt: Info (blue)
- Đã duyệt: Success (green)
- Từ chối: Danger (red)

### 3. **Interactive Elements**
- Hover effect trên menu items
- Cursor pointer khi hover vào table rows
- Active state cho đơn vị được chọn
- Loading spinner khi đang tải dữ liệu

### 4. **Empty States**
- "Chọn đơn vị để xem thông tin" khi chưa chọn
- "Chưa có hồ sơ..." khi đơn vị chưa có dữ liệu

## 🔐 Phân quyền

- **Admin & Lãnh đạo**: Xem được tất cả đơn vị
- **User thường**: Chỉ xem được đơn vị của mình và hồ sơ do mình tạo
  (Note: Hiện tại API cho phép xem tất cả, cần cập nhật endpoint `GET /api/don-vi/` để filter theo quyền nếu cần)

## 🐛 Xử lý lỗi

- Nếu không tải được danh sách đơn vị: Show toast error
- Nếu không tải được thống kê: Show toast error
- Nếu không tải được danh sách hồ sơ: Hiển thị message "Lỗi khi tải dữ liệu" trong bảng

## 📊 Performance

- Lazy loading: Chỉ tải dữ liệu đơn vị khi click
- Limit 1000 records mỗi tab (có thể thêm pagination nếu cần)
- Sử dụng async/await cho tất cả API calls

## 🔄 Tích hợp

Trang này tích hợp với các module hiện có:
- **API Đơn vị** (`/api/don-vi/`)
- **API Hồ sơ** (`/api/ho-so/`)
- Navigation menu chung
- Authentication system

## 🎯 Lợi ích

1. **Dễ dàng tra cứu**: Tìm hồ sơ theo đơn vị nhanh chóng
2. **Tổng quan nhanh**: Thống kê ngay trên màn hình
3. **Phân loại rõ ràng**: Chia theo cá nhân/tập thể
4. **UX tốt**: Interface trực quan, dễ sử dụng

## 📝 Ghi chú phát triển

### Có thể mở rộng:
- [ ] Thêm filter theo năm, trạng thái trong từng tab
- [ ] Thêm pagination cho table khi có nhiều records
- [ ] Export danh sách theo đơn vị ra Excel
- [ ] Thêm biểu đồ thống kê chi tiết
- [ ] Thêm tính năng so sánh giữa các đơn vị

### Code structure:
```
app/
├── templates/
│   └── don_vi_detail.html      # Template trang
├── static/js/
│   └── don_vi_detail.js         # Logic JavaScript
└── api/
    └── don_vi.py                # API endpoints (đã thêm /thong-ke)
```

## ✅ Test checklist

- [x] Sidebar hiển thị đầy đủ 41 đơn vị
- [x] Click vào đơn vị load được thống kê
- [x] Tab cá nhân hiển thị đúng dữ liệu
- [x] Tab tập thể hiển thị đúng dữ liệu
- [x] Click vào row chuyển đến trang chi tiết
- [ ] Responsive trên mobile
- [ ] Loading state hiển thị đúng
- [ ] Error handling khi API lỗi

---

**Ngày tạo:** 5/3/2026  
**Tác giả:** GitHub Copilot  
**Version:** 1.0.0
