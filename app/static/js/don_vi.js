// Đơn vị management

// Check authentication
if (!checkAuth()) {
    window.location.href = '/login';
}

// Load data on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadDonVi();
});

// Load don vi
async function loadDonVi() {
    try {
        const loai = document.getElementById('filterLoai')?.value;
        const params = { limit: 1000 };
        if (loai) params.loai_don_vi = loai;
        
        const data = await apiCall('/don-vi/', { params });
        
        // Group by loai_don_vi
        const khoiCoQuan = data.filter(dv => dv.loai_don_vi === 'khoi_co_quan');
        const khoa = data.filter(dv => dv.loai_don_vi === 'khoa');
        const donViTrucThuoc = data.filter(dv => dv.loai_don_vi === 'don_vi_truc_thuoc');
        
        renderDonViList('khoiCoQuanList', khoiCoQuan);
        renderDonViList('khoaList', khoa);
        renderDonViList('donViTrucThuocList', donViTrucThuoc);
        
    } catch (error) {
        showError('Lỗi khi tải danh sách đơn vị');
    }
}

// Render don vi list
function renderDonViList(elementId, data) {
    const element = document.getElementById(elementId);
    
    if (!data || data.length === 0) {
        element.innerHTML = '<div class="list-group-item text-muted text-center">Không có dữ liệu</div>';
        return;
    }
    
    element.innerHTML = data.map(item => `
        <div class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
            <div class="flex-grow-1">
                <strong>${item.ma_don_vi}</strong> - ${item.ten_don_vi}
                ${item.mo_ta ? `<br><small class="text-muted">${item.mo_ta}</small>` : ''}
            </div>
            <div class="btn-group">
                <button class="btn btn-sm btn-outline-primary" onclick="editDonVi(${item.id})" title="Chỉnh sửa">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteDonVi(${item.id})" title="Xóa">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// Open create modal
function openCreateModal() {
    document.getElementById('modalTitle').textContent = 'Thêm đơn vị';
    document.getElementById('donViForm').reset();
    document.getElementById('donViId').value = '';
    
    const modal = new bootstrap.Modal(document.getElementById('donViModal'));
    modal.show();
}

// Edit don vi
async function editDonVi(id) {
    try {
        const donVi = await apiCall(`/don-vi/${id}`);
        
        document.getElementById('modalTitle').textContent = 'Chỉnh sửa đơn vị';
        document.getElementById('donViId').value = donVi.id;
        document.getElementById('maDonVi').value = donVi.ma_don_vi;
        document.getElementById('tenDonVi').value = donVi.ten_don_vi;
        document.getElementById('loaiDonVi').value = donVi.loai_don_vi;
        document.getElementById('moTa').value = donVi.mo_ta || '';
        
        const modal = new bootstrap.Modal(document.getElementById('donViModal'));
        modal.show();
    } catch (error) {
        showError('Lỗi khi tải thông tin đơn vị');
    }
}

// Save don vi
async function saveDonVi() {
    const id = document.getElementById('donViId').value;
    const data = {
        ma_don_vi: document.getElementById('maDonVi').value,
        ten_don_vi: document.getElementById('tenDonVi').value,
        loai_don_vi: document.getElementById('loaiDonVi').value,
        mo_ta: document.getElementById('moTa').value
    };
    
    // Validate
    if (!data.ma_don_vi || !data.ten_don_vi || !data.loai_don_vi) {
        showError('Vui lòng điền đầy đủ thông tin bắt buộc');
        return;
    }
    
    try {
        if (id) {
            // Update
            await apiCall(`/don-vi/${id}`, 'PUT', data);
            showSuccess('Cập nhật đơn vị thành công');
        } else {
            // Create
            await apiCall('/don-vi/', 'POST', data);
            showSuccess('Thêm đơn vị thành công');
        }
        
        // Close modal and reload
        const modal = bootstrap.Modal.getInstance(document.getElementById('donViModal'));
        modal.hide();
        await loadDonVi();
    } catch (error) {
        showError('Lỗi khi lưu đơn vị: ' + (error.response?.data?.detail || error.message));
    }
}

// Delete don vi
let deleteId = null;
function deleteDonVi(id) {
    deleteId = id;
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}

// Confirm delete
async function confirmDelete() {
    if (!deleteId) return;
    
    try {
        await apiCall(`/don-vi/${deleteId}`, 'DELETE');
        showSuccess('Xóa đơn vị thành công');
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
        modal.hide();
        deleteId = null;
        
        await loadDonVi();
    } catch (error) {
        showError('Lỗi khi xóa đơn vị: ' + (error.response?.data?.detail || error.message));
    }
}
