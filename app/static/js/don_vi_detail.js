/**
 * Đơn vị Detail Page
 * Hiển thị menu đơn vị và danh sách khen thưởng theo đơn vị
 */

let currentUnitId = null;
let allUnits = [];
let currentUser = null;

// Khởi tạo trang
document.addEventListener('DOMContentLoaded', async function() {
    // Check authentication
    if (!checkAuth()) {
        window.location.href = '/login';
        return;
    }
    
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
    
    // Initialize mobile sidebar toggle
    initMobileSidebar();
    
    await loadAllUnits();
});

/**
 * Initialize mobile sidebar toggle
 */
function initMobileSidebar() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarToggleDesktop = document.getElementById('sidebarToggleDesktop');
    const sidebarShowBtn = document.getElementById('sidebarShowBtn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const mainContent = document.querySelector('.main-content');
    
    // Mobile toggle
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('show');
            overlay.classList.toggle('show');
        });
    }
    
    // Desktop toggle (ẩn sidebar)
    if (sidebarToggleDesktop) {
        sidebarToggleDesktop.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('expanded');
            
            // Toggle show button visibility
            if (sidebar.classList.contains('collapsed')) {
                sidebarShowBtn.classList.add('show');
            } else {
                sidebarShowBtn.classList.remove('show');
            }
            
            // Change icon
            const icon = sidebarToggleDesktop.querySelector('i');
            if (sidebar.classList.contains('collapsed')) {
                icon.className = 'bi bi-chevron-right';
            } else {
                icon.className = 'bi bi-chevron-left';
            }
        });
    }
    
    // Desktop show button (hiện sidebar khi đã ẩn)
    if (sidebarShowBtn) {
        sidebarShowBtn.addEventListener('click', () => {
            sidebar.classList.remove('collapsed');
            mainContent.classList.remove('expanded');
            sidebarShowBtn.classList.remove('show');
            
            // Reset icon
            const icon = sidebarToggleDesktop?.querySelector('i');
            if (icon) {
                icon.className = 'bi bi-chevron-left';
            }
        });
    }
    
    if (overlay) {
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
        });
    }
}

/**
 * Load all units and populate sidebar
 */
async function loadAllUnits() {
    try {
        const response = await apiCall('/don-vi/', 'GET');
        allUnits = response;
        
        // Phân loại đơn vị
        const khoiCoQuan = allUnits.filter(u => u.loai_don_vi === 'khoi_co_quan');
        const khoa = allUnits.filter(u => u.loai_don_vi === 'khoa');
        const donViTrucThuoc = allUnits.filter(u => u.loai_don_vi === 'don_vi_truc_thuoc');
        
        // Render sidebar
        renderUnitList('khoiCoQuanList', khoiCoQuan);
        renderUnitList('khoaList', khoa);
        renderUnitList('donViTrucThuocList', donViTrucThuoc);
        
    } catch (error) {
        console.error('Error loading units:', error);
        showToast('Không thể tải danh sách đơn vị', 'error');
    }
}

/**
 * Render unit list in sidebar
 */
function renderUnitList(containerId, units) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    if (units.length === 0) {
        container.innerHTML = '<div class="list-group-item text-muted small">Không có dữ liệu</div>';
        return;
    }
    
    container.innerHTML = units.map(unit => `
        <a href="#" 
           class="list-group-item list-group-item-action" 
           onclick="selectUnit(${unit.id}, this); return false;">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <div class="fw-medium">${unit.ten_don_vi}</div>
                    <small class="text-muted">${unit.ma_don_vi}</small>
                </div>
                <i class="bi bi-chevron-right text-muted"></i>
            </div>
        </a>
    `).join('');
}

/**
 * Select and load unit details
 */
async function selectUnit(unitId, clickedElement) {
    if (currentUnitId === unitId) return;
    
    currentUnitId = unitId;
    
    // Update active state in sidebar
    document.querySelectorAll('.sidebar .list-group-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Add active class to clicked element
    if (clickedElement) {
        clickedElement.classList.add('active');
    }
    
    // Hide empty state, show details
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('unitDetails').style.display = 'block';
    
    // Check if user can add records for this unit
    const actionButtons = document.getElementById('actionButtons');
    
    console.log('Checking permissions for unit:', unitId, typeof unitId); // Debug
    console.log('Current user:', currentUser); // Debug
    console.log('User don_vi_id:', currentUser?.don_vi_id, typeof currentUser?.don_vi_id); // Debug
    
    // Determine if user can add records
    let canAddRecords = false;
    
    if (!currentUser) {
        console.warn('No current user found');
        canAddRecords = false;
    } else if (currentUser.role === 'view_only') {
        console.log('User is VIEW_ONLY, hiding action buttons');
        canAddRecords = false;
    } else if (currentUser.role === 'admin' || currentUser.role === 'lanh_dao') {
        console.log('User is ADMIN/LANH_DAO, showing action buttons');
        canAddRecords = true;
    } else if (parseInt(currentUser.don_vi_id) === parseInt(unitId)) {
        console.log('User can manage their own unit, showing action buttons');
        canAddRecords = true;
    } else {
        console.log('User cannot manage this unit, hiding action buttons');
        canAddRecords = false;
    }
    
    // Show/hide action buttons
    if (actionButtons) {
        actionButtons.style.display = canAddRecords ? 'flex' : 'none';
    }
    
    // Close mobile sidebar after selection
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    if (sidebar) sidebar.classList.remove('show');
    if (overlay) overlay.classList.remove('show');
    
    // Load unit data
    await loadUnitDetails(unitId);
}

/**
 * Load unit details and statistics
 */
async function loadUnitDetails(unitId) {
    try {
        // Load statistics
        const stats = await apiCall(`/don-vi/${unitId}/thong-ke`, 'GET');
        
        // Update header
        document.getElementById('unitName').textContent = stats.don_vi.ten_don_vi;
        document.getElementById('unitCode').textContent = stats.don_vi.ma_don_vi;
        document.getElementById('unitType').textContent = getUnitTypeName(stats.don_vi.loai_don_vi);
        
        // Update statistics
        document.getElementById('totalRecords').textContent = stats.statistics.total;
        document.getElementById('personalRecords').textContent = stats.statistics.personal;
        document.getElementById('collectiveRecords').textContent = stats.statistics.collective;
        document.getElementById('approvedRecords').textContent = stats.statistics.approved;
        
        // Load records lists
        await loadPersonalRecords(unitId);
        await loadCollectiveRecords(unitId);
        
    } catch (error) {
        console.error('Error loading unit details:', error);
        showToast('Không thể tải thông tin đơn vị', 'error');
    }
}

/**
 * Load personal records for unit
 */
async function loadPersonalRecords(unitId) {
    const tbody = document.getElementById('personalTableBody');
    
    try {
        const records = await apiCall(`/ho-so/?don_vi_id=${unitId}&loai_ho_so=ca_nhan&limit=1000`, 'GET');
        
        if (records.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center text-muted py-4">
                        <i class="bi bi-inbox" style="font-size: 2rem;"></i>
                        <div class="mt-2">Chưa có hồ sơ cá nhân nào</div>
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = records.map((record, index) => `
            <tr onclick="viewRecord(${record.id})" style="cursor: pointer;">
                <td class="d-none d-md-table-cell">${index + 1}</td>
                <td><span class="badge bg-secondary">${record.ma_ho_so}</span></td>
                <td>
                    <strong>${record.ho_ten || '-'}</strong>
                    ${record.ngay_sinh ? `<br><small class="text-muted">${formatDate(record.ngay_sinh)}</small>` : ''}
                </td>
                <td class="d-none d-lg-table-cell">${record.chuc_vu || '-'}</td>
                <td class="d-none d-md-table-cell">
                    ${record.danh_hieu ? `<div><span class="badge badge-loai bg-info">${record.danh_hieu.ten_danh_hieu}</span></div>` : ''}
                    ${record.hinh_thuc ? `<div class="mt-1"><span class="badge badge-loai bg-success">${record.hinh_thuc.ten_hinh_thuc}</span></div>` : ''}
                </td>
                <td class="d-none d-sm-table-cell">${record.nam_khen_thuong}</td>
                <td>${getStatusBadge(record.trang_thai)}</td>
            </tr>
        `).join('');
        
    } catch (error) {
        console.error('Error loading personal records:', error);
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-danger py-4">
                    Lỗi khi tải dữ liệu
                </td>
            </tr>
        `;
    }
}

/**
 * Load collective records for unit
 */
async function loadCollectiveRecords(unitId) {
    const tbody = document.getElementById('collectiveTableBody');
    
    try {
        const records = await apiCall(`/ho-so/?don_vi_id=${unitId}&loai_ho_so=tap_the&limit=1000`, 'GET');
        
        if (records.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center text-muted py-4">
                        <i class="bi bi-inbox" style="font-size: 2rem;"></i>
                        <div class="mt-2">Chưa có hồ sơ tập thể nào</div>
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = records.map((record, index) => `
            <tr onclick="viewRecord(${record.id})" style="cursor: pointer;">
                <td class="d-none d-md-table-cell">${index + 1}</td>
                <td><span class="badge bg-secondary">${record.ma_ho_so}</span></td>
                <td>
                    <strong>${record.ten_tap_the || '-'}</strong>
                </td>
                <td class="d-none d-md-table-cell">
                    ${record.danh_hieu ? `<div><span class="badge badge-loai bg-info">${record.danh_hieu.ten_danh_hieu}</span></div>` : ''}
                    ${record.hinh_thuc ? `<div class="mt-1"><span class="badge badge-loai bg-success">${record.hinh_thuc.ten_hinh_thuc}</span></div>` : ''}
                </td>
                <td class="d-none d-sm-table-cell">${record.nam_khen_thuong}</td>
                <td class="d-none d-lg-table-cell">${record.so_luong_thanh_vien || '-'}</td>
                <td>${getStatusBadge(record.trang_thai)}</td>
            </tr>
        `).join('');
        
    } catch (error) {
        console.error('Error loading collective records:', error);
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-danger py-4">
                    Lỗi khi tải dữ liệu
                </td>
            </tr>
        `;
    }
}

/**
 * View record detail
 */
function viewRecord(recordId) {
    // Navigate to record detail page or open modal
    window.location.href = `/ho-so?id=${recordId}`;
}

/**
 * Get unit type display name
 */
function getUnitTypeName(type) {
    const types = {
        'khoi_co_quan': 'Khối cơ quan',
        'khoa': 'Khoa',
        'don_vi_truc_thuoc': 'Đơn vị trực thuộc'
    };
    return types[type] || type;
}

/**
 * Get status badge HTML
 */
function getStatusBadge(status) {
    const statusConfig = {
        'nhap': { class: 'secondary', text: 'Đang nhập', icon: 'pencil' },
        'cho_duyet': { class: 'warning', text: 'Chờ duyệt', icon: 'clock' },
        'dang_duyet': { class: 'info', text: 'Đang duyệt', icon: 'hourglass-split' },
        'da_duyet': { class: 'success', text: 'Đã duyệt', icon: 'check-circle' },
        'tu_choi': { class: 'danger', text: 'Từ chối', icon: 'x-circle' }
    };
    
    const config = statusConfig[status] || statusConfig['nhap'];
    return `<span class="badge bg-${config.class}">
        <i class="bi bi-${config.icon} me-1"></i>${config.text}
    </span>`;
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN');
}

/**
 * Add new personal record
 */
function addPersonalRecord() {
    if (!currentUnitId) {
        showToast('Vui lòng chọn đơn vị trước', 'warning');
        return;
    }
    
    // Check permission
    if (!currentUser || currentUser.role === 'view_only') {
        showToast('Bạn không có quyền thêm hồ sơ', 'error');
        return;
    }
    
    // USER and CAN_BO can only add for their own unit
    if ((currentUser.role === 'user' || currentUser.role === 'can_bo') && parseInt(currentUser.don_vi_id) !== parseInt(currentUnitId)) {
        showToast('Bạn chỉ có thể thêm hồ sơ cho đơn vị của mình', 'error');
        return;
    }
    
    // Navigate to ho-so page with pre-filled unit info
    window.location.href = `/ho-so?don_vi_id=${currentUnitId}&loai_ho_so=ca_nhan`;
}

/**
 * Add new collective record
 */
function addCollectiveRecord() {
    if (!currentUnitId) {
        showToast('Vui lòng chọn đơn vị trước', 'warning');
        return;
    }
    
    // Check permission
    if (!currentUser || currentUser.role === 'view_only') {
        showToast('Bạn không có quyền thêm hồ sơ', 'error');
        return;
    }
    
    // USER and CAN_BO can only add for their own unit
    if ((currentUser.role === 'user' || currentUser.role === 'can_bo') && parseInt(currentUser.don_vi_id) !== parseInt(currentUnitId)) {
        showToast('Bạn chỉ có thể thêm hồ sơ cho đơn vị của mình', 'error');
        return;
    }
    
    // Navigate to ho-so page with pre-filled unit info
    window.location.href = `/ho-so?don_vi_id=${currentUnitId}&loai_ho_so=tap_the`;
}
