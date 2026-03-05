// Hồ sơ khen thưởng management

let currentHoSoId = null;
let donViList = [];
let danhHieuList = [];
let hinhThucList = [];

// Check authentication
if (!checkAuth()) {
    window.location.href = '/login';
}

// Load data on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadFilters();
    await loadHoSo();
    setupFilterHandlers();
    
    // Check for URL parameters to pre-fill form
    checkUrlParameters();
});

// Load filters
async function loadFilters() {
    try {
        // Load years
        const currentYear = new Date().getFullYear();
        const yearSelect = document.getElementById('filterNam');
        for (let year = currentYear; year >= currentYear - 10; year--) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearSelect.appendChild(option);
        }
        
        // Load don vi
        donViList = await apiCall('/don-vi/', { params: { limit: 1000 } });
        
        // Load danh hieu
        danhHieuList = await apiCall('/danh-hieu/', { params: { limit: 1000 } });
        
        // Load hinh thuc
        hinhThucList = await apiCall('/hinh-thuc/', { params: { limit: 1000 } });
        
        // Populate selects
        populateSelect('donViId', donViList, 'id', 'ten_don_vi');
        populateSelect('danhHieuId', danhHieuList, 'id', 'ten_danh_hieu', true);
        populateSelect('hinhThucId', hinhThucList, 'id', 'ten_hinh_thuc', true);
        
    } catch (error) {
        showError('Lỗi khi tải dữ liệu');
    }
}

// Setup filter handlers
function setupFilterHandlers() {
    document.getElementById('filterLoaiHoSo').addEventListener('change', loadHoSo);
    document.getElementById('filterTrangThai').addEventListener('change', loadHoSo);
    document.getElementById('filterNam').addEventListener('change', loadHoSo);
    
    let searchTimeout;
    document.getElementById('searchText').addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => loadHoSo(), 500);
    });
}

// Load ho so list
async function loadHoSo() {
    try {
        const loaiHoSo = document.getElementById('filterLoaiHoSo').value;
        const trangThai = document.getElementById('filterTrangThai').value;
        const nam = document.getElementById('filterNam').value;
        const search = document.getElementById('searchText').value;
        
        const params = { limit: 100 };
        if (loaiHoSo) params.loai_ho_so = loaiHoSo;
        if (trangThai) params.trang_thai = trangThai;
        if (nam) params.nam_khen_thuong = nam;
        if (search) params.search = search;
        
        const data = await apiCall('/ho-so/', { params });
        
        renderHoSoTable(data);
    } catch (error) {
        showError('Lỗi khi tải danh sách hồ sơ');
    }
}

// Render table
function renderHoSoTable(data) {
    const tbody = document.getElementById('hoSoTable');
    
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">Không có dữ liệu</td></tr>';
        return;
    }
    
    const statusBadges = {
        'nhap': 'secondary',
        'cho_duyet': 'warning',
        'dang_xu_ly': 'info',
        'da_duyet': 'success',
        'tu_choi': 'danger'
    };
    
    const statusLabels = {
        'nhap': 'Nháp',
        'cho_duyet': 'Chờ duyệt',
        'dang_xu_ly': 'Đang xử lý',
        'da_duyet': 'Đã duyệt',
        'tu_choi': 'Từ chối'
    };
    
    tbody.innerHTML = data.map(item => {
        const donVi = donViList.find(dv => dv.id === item.don_vi_id);
        const ten = item.loai_ho_so === 'ca_nhan' ? item.ho_ten : item.ten_tap_the;
        
        return `
            <tr>
                <td><strong>${item.ma_ho_so}</strong></td>
                <td><span class="badge bg-${item.loai_ho_so === 'ca_nhan' ? 'primary' : 'success'}">${item.loai_ho_so === 'ca_nhan' ? 'Cá nhân' : 'Tập thể'}</span></td>
                <td>${ten || ''}</td>
                <td>${donVi ? donVi.ten_don_vi : ''}</td>
                <td>${item.nam_khen_thuong}</td>
                <td><span class="badge bg-${statusBadges[item.trang_thai]}">${statusLabels[item.trang_thai]}</span></td>
                <td>${formatDate(item.created_at)}</td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="viewHoSo(${item.id})">
                        <i class="bi bi-eye"></i>
                    </button>
                    ${item.trang_thai === 'nhap' ? `
                    <button class="btn btn-sm btn-primary" onclick="editHoSo(${item.id})">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteHoSo(${item.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                    ` : ''}
                </td>
            </tr>
        `;
    }).join('');
}

// Toggle loai ho so fields
function toggleLoaiHoSo() {
    const loaiHoSo = document.getElementById('loaiHoSo').value;
    const caNhanFields = document.getElementById('caNhanFields');
    const tapTheFields = document.getElementById('tapTheFields');
    
    if (loaiHoSo === 'ca_nhan') {
        caNhanFields.style.display = 'block';
        tapTheFields.style.display = 'none';
        document.getElementById('hoTen').required = true;
        document.getElementById('tenTapThe').required = false;
    } else if (loaiHoSo === 'tap_the') {
        caNhanFields.style.display = 'none';
        tapTheFields.style.display = 'block';
        document.getElementById('hoTen').required = false;
        document.getElementById('tenTapThe').required = true;
    } else {
        caNhanFields.style.display = 'none';
        tapTheFields.style.display = 'none';
    }
}

// Populate select
function populateSelect(selectId, data, valueField, textField, addEmpty = false) {
    const select = document.getElementById(selectId);
    select.innerHTML = '';
    
    if (addEmpty) {
        select.appendChild(new Option('-- Chọn --', ''));
    }
    
    data.forEach(item => {
        select.appendChild(new Option(item[textField], item[valueField]));
    });
}

// Open create modal
function openCreateModal(prefilledData = {}) {
    currentHoSoId = null;
    document.getElementById('hoSoModalTitle').textContent = 'Tạo hồ sơ khen thưởng';
    document.getElementById('hoSoForm').reset();
    document.getElementById('hoSoId').value = '';
    document.getElementById('namKhenThuong').value = new Date().getFullYear();
    
    // Hide upload section for new records
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('fileList').innerHTML = '';
    
    // Pre-fill with provided data
    if (prefilledData.don_vi_id) {
        document.getElementById('donViId').value = prefilledData.don_vi_id;
    }
    if (prefilledData.loai_ho_so) {
        document.getElementById('loaiHoSo').value = prefilledData.loai_ho_so;
    }
    
    toggleLoaiHoSo();
    
    const modal = new bootstrap.Modal(document.getElementById('hoSoModal'));
    modal.show();
}

// Edit ho so
async function editHoSo(id) {
    try {
        const hoSo = await apiCall(`/ho-so/${id}`);
        
        currentHoSoId = id;
        document.getElementById('hoSoModalTitle').textContent = 'Chỉnh sửa hồ sơ';
        document.getElementById('hoSoId').value = id;
        document.getElementById('loaiHoSo').value = hoSo.loai_ho_so;
        document.getElementById('hoTen').value = hoSo.ho_ten || '';
        document.getElementById('capBac').value = hoSo.cap_bac || '';
        document.getElementById('chucVu').value = hoSo.chuc_vu || '';
        document.getElementById('tenTapThe').value = hoSo.ten_tap_the || '';
        document.getElementById('donViId').value = hoSo.don_vi_id;
        document.getElementById('danhHieuId').value = hoSo.danh_hieu_id || '';
        document.getElementById('hinhThucId').value = hoSo.hinh_thuc_id || '';
        document.getElementById('namKhenThuong').value = hoSo.nam_khen_thuong;
        document.getElementById('thanhTich').value = hoSo.thanh_tich;
        document.getElementById('ghiChu').value = hoSo.ghi_chu || '';
        
        toggleLoaiHoSo();
        
        // Show upload section and load files
        document.getElementById('uploadSection').style.display = 'block';
        loadFiles(id, hoSo.file_dinh_kem);
        
        const modal = new bootstrap.Modal(document.getElementById('hoSoModal'));
        modal.show();
    } catch (error) {
        showError('Lỗi khi tải thông tin hồ sơ');
    }
}

// Save ho so
async function saveHoSo() {
    try {
        const form = document.getElementById('hoSoForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        const data = {
            loai_ho_so: document.getElementById('loaiHoSo').value,
            ho_ten: document.getElementById('hoTen').value || null,
            cap_bac: document.getElementById('capBac').value || null,
            chuc_vu: document.getElementById('chucVu').value || null,
            ten_tap_the: document.getElementById('tenTapThe').value || null,
            don_vi_id: parseInt(document.getElementById('donViId').value),
            danh_hieu_id: document.getElementById('danhHieuId').value ? parseInt(document.getElementById('danhHieuId').value) : null,
            hinh_thuc_id: document.getElementById('hinhThucId').value ? parseInt(document.getElementById('hinhThucId').value) : null,
            nam_khen_thuong: parseInt(document.getElementById('namKhenThuong').value),
            thanh_tich: document.getElementById('thanhTich').value,
            ghi_chu: document.getElementById('ghiChu').value || null
        };
        
        if (currentHoSoId) {
            await apiCall(`/ho-so/${currentHoSoId}`, {
                method: 'PUT',
                data
            });
            showSuccess('Cập nhật hồ sơ thành công');
        } else {
            await apiCall('/ho-so/', {
                method: 'POST',
                data
            });
            showSuccess('Tạo hồ sơ thành công');
        }
        
        bootstrap.Modal.getInstance(document.getElementById('hoSoModal')).hide();
        await loadHoSo();
    } catch (error) {
        showError(error.response?.data?.detail || 'Lỗi khi lưu hồ sơ');
    }
}

// Delete ho so
async function deleteHoSo(id) {
    if (!confirm('Bạn có chắc chắn muốn xóa hồ sơ này?')) return;
    
    try {
        await apiCall(`/ho-so/${id}`, { method: 'DELETE' });
        showSuccess('Xóa hồ sơ thành công');
        await loadHoSo();
    } catch (error) {
        showError('Lỗi khi xóa hồ sơ');
    }
}

// View ho so (placeholder)
function viewHoSo(id) {
    showToast('Chức năng xem chi tiết đang phát triển', 'info');
}

/**
 * Check URL parameters for pre-filling the form
 */
function checkUrlParameters() {
    const urlParams = new URLSearchParams(window.location.search);
    const donViId = urlParams.get('don_vi_id');
    const loaiHoSo = urlParams.get('loai_ho_so');
    
    // If both parameters exist, open create modal with pre-filled data
    if (donViId && loaiHoSo) {
        const prefilledData = {
            don_vi_id: parseInt(donViId),
            loai_ho_so: loaiHoSo
        };
        
        // Wait a bit for filters to load
        setTimeout(() => {
            openCreateModal(prefilledData);
            
            // Clean URL (remove query params)
            const newUrl = window.location.pathname;
            window.history.replaceState({}, document.title, newUrl);
        }, 500);
    }
}

// ============= FILE UPLOAD FUNCTIONS =============

// Load files for ho so
function loadFiles(hoSoId, fileData) {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';
    
    if (!fileData) {
        fileList.innerHTML = '<p class="text-muted small mb-0">Chưa có file đính kèm</p>';
        return;
    }
    
    let files;
    try {
        files = typeof fileData === 'string' ? JSON.parse(fileData) : fileData;
    } catch (e) {
        files = [];
    }
    
    if (!files || files.length === 0) {
        fileList.innerHTML = '<p class="text-muted small mb-0">Chưa có file đính kèm</p>';
        return;
    }
    
    const fileListHtml = files.map(file => {
        const isImage = file.filename.match(/\.(jpg|jpeg|png|gif)$/i);
        const icon = isImage ? 'bi-image' : 'bi-file-earmark';
        const fileSize = formatFileSize(file.size);
        
        return `
            <div class="d-flex align-items-center justify-content-between p-2 border rounded mb-2">
                <div class="d-flex align-items-center">
                    <i class="bi ${icon} me-2 text-primary"></i>
                    <div>
                        <a href="${file.url}" target="_blank" class="text-decoration-none">
                            ${file.filename}
                        </a>
                        <small class="text-muted d-block">${fileSize}</small>
                    </div>
                </div>
                <button type="button" class="btn btn-sm btn-outline-danger" 
                        onclick="deleteFile(${hoSoId}, '${file.stored_name}')">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        `;
    }).join('');
    
    fileList.innerHTML = fileListHtml;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Upload file
async function uploadFile(hoSoId, file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`/api/ho-so/${hoSoId}/upload`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }
        
        return await response.json();
    } catch (error) {
        throw error;
    }
}

// Delete file
async function deleteFile(hoSoId, filename) {
    if (!confirm('Bạn có chắc muốn xóa file này?')) {
        return;
    }
    
    try {
        await apiCall(`/ho-so/${hoSoId}/upload/${filename}`, {
            method: 'DELETE'
        });
        
        showSuccess('Xóa file thành công');
        
        // Reload files
        const hoSo = await apiCall(`/ho-so/${hoSoId}`);
        loadFiles(hoSoId, hoSo.file_dinh_kem);
        
    } catch (error) {
        showError('Lỗi khi xóa file: ' + error.message);
    }
}

// Handle file upload input change
document.addEventListener('DOMContentLoaded', () => {
    const fileUpload = document.getElementById('fileUpload');
    if (fileUpload) {
        fileUpload.addEventListener('change', async (e) => {
            const files = e.target.files;
            if (!files || files.length === 0 || !currentHoSoId) return;
            
            for (let file of files) {
                try {
                    showSuccess(`Đang upload ${file.name}...`);
                    await uploadFile(currentHoSoId, file);
                    showSuccess(`Upload ${file.name} thành công`);
                } catch (error) {
                    showError(`Lỗi upload ${file.name}: ${error.message}`);
                }
            }
            
            // Clear input
            fileUpload.value = '';
            
            // Reload files
            const hoSo = await apiCall(`/ho-so/${currentHoSoId}`);
            loadFiles(currentHoSoId, hoSo.file_dinh_kem);
        });
    }
});

/**
 * Export functions
 */

// Get current filter parameters
function getExportParams() {
    const params = new URLSearchParams();
    
    const filterLoaiHoSo = document.getElementById('filterLoaiHoSo')?.value;
    const filterTrangThai = document.getElementById('filterTrangThai')?.value;
    const filterNam = document.getElementById('filterNam')?.value;
    
    if (filterLoaiHoSo) params.append('loai_ho_so', filterLoaiHoSo);
    if (filterTrangThai) params.append('trang_thai', filterTrangThai);
    if (filterNam) params.append('nam_khen_thuong', filterNam);
    
    return params.toString();
}

// Export to Excel
async function exportExcel() {
    try {
        const params = getExportParams();
        const token = localStorage.getItem('token');
        
        // Create download link
        const url = `/api/export/excel?${params}`;
        
        // Fetch with authorization
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

// Export to Word
async function exportWord() {
    try {
        const params = getExportParams();
        const token = localStorage.getItem('token');
        
        const url = `/api/export/word?${params}`;
        
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Xuất file thất bại');
        }
        
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `danh_sach_khen_thuong_${new Date().getTime()}.docx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        a.remove();
        
        showSuccess('Xuất file Word thành công');
    } catch (error) {
        showError('Lỗi xuất file Word: ' + error.message);
    }
}

// Export to PDF
async function exportPDF() {
    try {
        const params = getExportParams();
        const token = localStorage.getItem('token');
        
        const url = `/api/export/pdf?${params}`;
        
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Xuất file thất bại');
        }
        
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `danh_sach_khen_thuong_${new Date().getTime()}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        a.remove();
        
        showSuccess('Xuất file PDF thành công');
    } catch (error) {
        showError('Lỗi xuất file PDF: ' + error.message);
    }
}
