# Quick Test - Tính năng Menu Đơn vị

## Test ngay

```powershell
# 1. Đảm bảo đã cài packages
pip install -r requirements.txt

# 2. Chạy server
python main.py

# 3. Truy cập
# http://localhost:8000/don-vi-chi-tiet
```

## Test cases

### 1. Test hiển thị sidebar
- ✅ Mở trang `/don-vi-chi-tiet`
- ✅ Kiểm tra 3 phần: Khối cơ quan, Các khoa, Đơn vị trực thuộc
- ✅ Kiểm tra số lượng đơn vị hiển thị đúng

### 2. Test chọn đơn vị
- ✅ Click vào "Văn phòng Trường"
- ✅ Kiểm tra active state (background xanh)
- ✅ Kiểm tra header hiển thị tên đơn vị
- ✅ Kiểm tra 4 cards thống kê có số liệu

### 3. Test tabs
- ✅ Tab "Danh sách cá nhân" active mặc định
- ✅ Click tab "Danh sách tập thể"
- ✅ Kiểm tra table render đúng

### 4. Test click vào hồ sơ
- ✅ Click vào một row trong table
- ✅ Kiểm tra redirect đến `/ho-so?id=xxx`

### 5. Test empty state
- ✅ Chọn đơn vị chưa có hồ sơ nào
- ✅ Kiểm tra message "Chưa có hồ sơ..."

## API Tests

### Test endpoint mới
```bash
# 1. Login để lấy token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# 2. Test thống kê đơn vị (thay YOUR_TOKEN)
curl -X GET http://localhost:8000/api/don-vi/1/thong-ke \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Expected response
```json
{
  "don_vi": {
    "id": 1,
    "ma_don_vi": "VPT",
    "ten_don_vi": "Văn phòng Trường",
    "loai_don_vi": "khoi_co_quan"
  },
  "statistics": {
    "total": 0,
    "personal": 0,
    "collective": 0,
    "approved": 0
  }
}
```

## Browser Console Tests

Mở DevTools (F12) và chạy:

```javascript
// 1. Test load units
loadAllUnits().then(units => console.log('Units loaded:', units));

// 2. Test select unit
selectUnit(1);

// 3. Test load statistics
loadUnitDetails(1);
```

## Checklist hoàn thành

- [x] Template HTML đã tạo
- [x] JavaScript đã tạo
- [x] API endpoint đã thêm
- [x] Route đã thêm vào main.py
- [x] Navigation menu đã cập nhật
- [ ] Server chạy thành công
- [ ] Trang hiển thị đúng
- [ ] Click chọn đơn vị hoạt động
- [ ] Thống kê hiển thị đúng
- [ ] Tables hiển thị dữ liệu

## Troubleshooting

### Lỗi "Module not found"
```powershell
pip install -r requirements.txt
```

### Lỗi kết nối database
```powershell
python test_connection.py
```

### Trang trắng / không load
- Kiểm tra Console (F12) xem có lỗi JavaScript
- Kiểm tra Network tab xem API calls
- Kiểm tra file `app.js` đã load chưa

### API trả về 401
- Đăng nhập lại
- Kiểm tra token trong localStorage

---

**Chạy test:** `python main.py` và truy cập http://localhost:8000/don-vi-chi-tiet
