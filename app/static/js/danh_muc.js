// Danh mục management (Đơn vị, Danh hiệu, Hình thức)

// Check authentication
if (!checkAuth()) {
    window.location.href = '/login';
}

// Load data on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadAllData();
});

// Load all data
async function loadAllData() {
    await loadDonVi();
    await loadDanhHieu();
    await loadHinhThuc();
}

// ========== ĐƠN VỊ ==========

async function loadDonVi() {
    try {
        const data = await apiCall('/don-vi/', { params: { limit: 1000 } });
        renderDonViTable(data);
    } catch (error) {
        showError('Lỗi khi tải danh sách đơn vị');
    }
}

function renderDonViTable(data) {
    const tbody = document.getElementById('donViTableBody');
    
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Không có dữ liệu</td></tr>';
        return;
    }
    
    const loaiLabels = {
        'khoi_co_quan': 'Khối cơ quan',
        'khoa': 'Khoa',
        'don_vi_truc_thuoc': 'Đơn vị trực thuộc'
    };
    
    tbody.innerHTML = data.map(item => `
        <tr>
            <td><strong>${item.ma_don_vi}</strong></td>
            <td>${item.ten_don_vi}</td>
            <td><span class="badge bg-info">${loaiLabels[item.loai_don_vi]}</span></td>
            <td>${item.thu_tu}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editDonVi(${item.id})">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteDonVi(${item.id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function openDonViModal(id = null) {
    // Implementation for don vi modal
    showToast('Chức năng đang phát triển', 'info');
}

function editDonVi(id) {
    showToast('Chức năng đang phát triển', 'info');
}

function deleteDonVi(id) {
    showToast('Chức năng đang phát triển', 'info');
}

// ========== DANH HIỆU THI ĐUA ==========

async function loadDanhHieu() {
    try {
        const data = await apiCall('/danh-hieu/', { params: { limit: 1000 } });
        renderDanhHieuTable(data);
    } catch (error) {
        showError('Lỗi khi tải danh sách danh hiệu');
    }
}

function renderDanhHieuTable(data) {
    const tbody = document.getElementById('danhHieuTableBody');
    
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Không có dữ liệu</td></tr>';
        return;
    }
    
    tbody.innerHTML = data.map(item => `
        <tr>
            <td><strong>${item.ma_danh_hieu}</strong></td>
            <td>${item.ten_danh_hieu}</td>
            <td>${item.cap_khen_thuong || ''}</td>
            <td>${item.thu_tu}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editDanhHieu(${item.id})">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteDanhHieu(${item.id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function openDanhHieuModal(id = null) {
    showToast('Chức năng đang phát triển', 'info');
}

function editDanhHieu(id) {
    showToast('Chức năng đang phát triển', 'info');
}

function deleteDanhHieu(id) {
    showToast('Chức năng đang phát triển', 'info');
}

// ========== HÌNH THỨC KHEN THƯỞNG ==========

async function loadHinhThuc() {
    try {
        const data = await apiCall('/hinh-thuc/', { params: { limit: 1000 } });
        renderHinhThucTable(data);
    } catch (error) {
        showError('Lỗi khi tải danh sách hình thức');
    }
}

function renderHinhThucTable(data) {
    const tbody = document.getElementById('hinhThucTableBody');
    
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Không có dữ liệu</td></tr>';
        return;
    }
    
    tbody.innerHTML = data.map(item => `
        <tr>
            <td><strong>${item.ma_hinh_thuc}</strong></td>
            <td>${item.ten_hinh_thuc}</td>
            <td>${item.muc_thuong ? formatNumber(item.muc_thuong) + ' VNĐ' : ''}</td>
            <td>${item.cap_khen_thuong || ''}</td>
            <td>${item.thu_tu}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editHinhThuc(${item.id})">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteHinhThuc(${item.id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function openHinhThucModal(id = null) {
    showToast('Chức năng đang phát triển', 'info');
}

function editHinhThuc(id) {
    showToast('Chức năng đang phát triển', 'info');
}

function deleteHinhThuc(id) {
    showToast('Chức năng đang phát triển', 'info');
}
