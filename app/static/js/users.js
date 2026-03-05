// User Management JavaScript

// Check authentication
if (!checkAuth()) {
    window.location.href = '/login';
}

// Check if user is admin
const currentUser = getCurrentUser();
if (currentUser.role !== 'admin') {
    showError('Bạn không có quyền truy cập trang này');
    window.location.href = '/dashboard';
}

// Global variables
let allUnits = [];
let allUsers = [];
let userModal, resetPasswordModal, confirmDeleteModal;

// Load data on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Initialize modals
    userModal = new bootstrap.Modal(document.getElementById('userModal'));
    resetPasswordModal = new bootstrap.Modal(document.getElementById('resetPasswordModal'));
    confirmDeleteModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
    
    // Load initial data
    await loadUnits();
    await loadUsers();
});

// Load all units for dropdown
async function loadUnits() {
    try {
        allUnits = await apiCall('/don-vi/', { params: { limit: 1000 } });
        
        // Populate unit filter dropdown
        const filterUnit = document.getElementById('filterUnit');
        const donViId = document.getElementById('donViId');
        
        const options = allUnits.map(unit => 
            `<option value="${unit.id}">${unit.ten_don_vi}</option>`
        ).join('');
        
        filterUnit.innerHTML = '<option value="">Tất cả đơn vị</option>' + options;
        donViId.innerHTML = '<option value="">-- Chọn đơn vị --</option>' + options;
    } catch (error) {
        showError('Lỗi khi tải danh sách đơn vị');
    }
}

// Load users with filters
async function loadUsers() {
    try {
        const filterRole = document.getElementById('filterRole').value;
        const filterUnit = document.getElementById('filterUnit').value;
        const filterStatus = document.getElementById('filterStatus').value;
        
        // Load all users
        allUsers = await apiCall('/users/', { params: { limit: 1000 } });
        
        // Apply filters
        let filteredUsers = allUsers;
        
        if (filterRole) {
            filteredUsers = filteredUsers.filter(user => user.role === filterRole);
        }
        
        if (filterUnit) {
            filteredUsers = filteredUsers.filter(user => user.don_vi_id === parseInt(filterUnit));
        }
        
        if (filterStatus === 'active') {
            filteredUsers = filteredUsers.filter(user => user.is_active);
        } else if (filterStatus === 'inactive') {
            filteredUsers = filteredUsers.filter(user => !user.is_active);
        }
        
        renderUsersTable(filteredUsers);
    } catch (error) {
        showError('Lỗi khi tải danh sách tài khoản');
        console.error(error);
    }
}

// Render users table
function renderUsersTable(users) {
    const tbody = document.getElementById('usersTableBody');
    
    if (!users || users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">Không có dữ liệu</td></tr>';
        return;
    }
    
    const roleLabels = {
        'admin': '<span class="badge bg-danger">Quản trị viên</span>',
        'lanh_dao': '<span class="badge bg-warning text-dark">Lãnh đạo</span>',
        'can_bo': '<span class="badge bg-info">Cán bộ</span>',
        'user': '<span class="badge bg-primary">Người dùng</span>',
        'view_only': '<span class="badge bg-secondary">Chỉ xem</span>'
    };
    
    tbody.innerHTML = users.map(user => {
        const unit = allUnits.find(u => u.id === user.don_vi_id);
        const unitName = unit ? unit.ten_don_vi : 'N/A';
        const statusBadge = user.is_active 
            ? '<span class="badge bg-success">Hoạt động</span>'
            : '<span class="badge bg-secondary">Đã khóa</span>';
        
        const isCurrentUser = user.id === currentUser.id;
        const disableActions = isCurrentUser ? 'disabled' : '';
        
        return `
            <tr>
                <td><strong>${user.username}</strong></td>
                <td>${user.ho_ten || ''}</td>
                <td>${unitName}</td>
                <td>${roleLabels[user.role] || user.role}</td>
                <td>${statusBadge}</td>
                <td>${user.email || ''}</td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="editUser(${user.id})" title="Chỉnh sửa">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-warning" onclick="openResetPasswordModal(${user.id}, '${user.username}')" title="Đặt lại mật khẩu">
                            <i class="bi bi-key"></i>
                        </button>
                        <button class="btn btn-outline-${user.is_active ? 'secondary' : 'success'}" 
                                onclick="toggleUserStatus(${user.id})" 
                                title="${user.is_active ? 'Khóa tài khoản' : 'Kích hoạt tài khoản'}"
                                ${disableActions}>
                            <i class="bi bi-${user.is_active ? 'lock' : 'unlock'}"></i>
                        </button>
                        <button class="btn btn-outline-danger" 
                                onclick="openDeleteModal(${user.id}, '${user.username}')" 
                                title="Xóa"
                                ${disableActions}>
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// Open user modal for create/edit
function openUserModal(userId = null) {
    const form = document.getElementById('userForm');
    form.reset();
    
    const modalTitle = document.getElementById('userModalTitle');
    const passwordGroup = document.getElementById('passwordGroup');
    const passwordField = document.getElementById('password');
    const usernameField = document.getElementById('username');
    
    if (userId) {
        // Edit mode
        modalTitle.textContent = 'Chỉnh sửa tài khoản';
        passwordGroup.style.display = 'none';
        passwordField.removeAttribute('required');
        usernameField.setAttribute('readonly', true);
        
        // Load user data
        const user = allUsers.find(u => u.id === userId);
        if (user) {
            document.getElementById('userId').value = user.id;
            document.getElementById('username').value = user.username;
            document.getElementById('hoTen').value = user.ho_ten || '';
            document.getElementById('email').value = user.email || '';
            document.getElementById('capBac').value = user.cap_bac || '';
            document.getElementById('chucVu').value = user.chuc_vu || '';
            document.getElementById('donViId').value = user.don_vi_id || '';
            document.getElementById('role').value = user.role;
        }
    } else {
        // Create mode
        modalTitle.textContent = 'Thêm tài khoản';
        passwordGroup.style.display = 'block';
        passwordField.setAttribute('required', true);
        usernameField.removeAttribute('readonly');
    }
    
    userModal.show();
}

// Edit user
function editUser(userId) {
    openUserModal(userId);
}

// Save user (create or update)
async function saveUser() {
    const form = document.getElementById('userForm');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const userId = document.getElementById('userId').value;
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const hoTen = document.getElementById('hoTen').value.trim();
    const email = document.getElementById('email').value.trim();
    const capBac = document.getElementById('capBac').value.trim();
    const chucVu = document.getElementById('chucVu').value.trim();
    const donViId = parseInt(document.getElementById('donViId').value);
    const role = document.getElementById('role').value;
    
    // Validate
    if (!username || !email || !donViId || !role) {
        showError('Vui lòng điền đầy đủ thông tin bắt buộc');
        return;
    }
    
    if (!userId && !password) {
        showError('Vui lòng nhập mật khẩu');
        return;
    }
    
    if (password && password.length < 6) {
        showError('Mật khẩu phải có ít nhất 6 ký tự');
        return;
    }
    
    try {
        if (userId) {
            // Update user
            const updateData = {
                email,
                ho_ten: hoTen,
                cap_bac: capBac || null,
                chuc_vu: chucVu || null,
                don_vi_id: donViId,
                role
            };
            
            await apiCall(`/users/${userId}`, {
                method: 'PUT',
                data: updateData
            });
            
            showSuccess('Cập nhật tài khoản thành công');
        } else {
            // Create user
            const createData = {
                username,
                password,
                email,
                ho_ten: hoTen,
                cap_bac: capBac || null,
                chuc_vu: chucVu || null,
                don_vi_id: donViId,
                role
            };
            
            await apiCall('/users/', {
                method: 'POST',
                data: createData
            });
            
            showSuccess('Thêm tài khoản thành công');
        }
        
        userModal.hide();
        await loadUsers();
    } catch (error) {
        showError(error.response?.data?.detail || 'Có lỗi xảy ra');
        console.error(error);
    }
}

// Open reset password modal
function openResetPasswordModal(userId, username) {
    document.getElementById('resetUserId').value = userId;
    document.getElementById('resetUsername').textContent = username;
    document.getElementById('newPassword').value = '';
    document.getElementById('confirmPassword').value = '';
    
    resetPasswordModal.show();
}

// Reset password
async function resetPassword() {
    const userId = document.getElementById('resetUserId').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (!newPassword || newPassword.length < 6) {
        showError('Mật khẩu phải có ít nhất 6 ký tự');
        return;
    }
    
    if (newPassword !== confirmPassword) {
        showError('Mật khẩu xác nhận không khớp');
        return;
    }
    
    try {
        await apiCall(`/users/${userId}/reset-password`, {
            method: 'POST',
            params: { new_password: newPassword }
        });
        
        showSuccess('Đặt lại mật khẩu thành công');
        resetPasswordModal.hide();
    } catch (error) {
        showError(error.response?.data?.detail || 'Có lỗi xảy ra');
        console.error(error);
    }
}

// Toggle user status (activate/deactivate)
async function toggleUserStatus(userId) {
    const user = allUsers.find(u => u.id === userId);
    if (!user) return;
    
    const action = user.is_active ? 'khóa' : 'kích hoạt';
    
    if (!confirm(`Bạn có chắc chắn muốn ${action} tài khoản "${user.username}"?`)) {
        return;
    }
    
    try {
        await apiCall(`/users/${userId}/toggle-status`, {
            method: 'POST'
        });
        
        showSuccess(`${action.charAt(0).toUpperCase() + action.slice(1)} tài khoản thành công`);
        await loadUsers();
    } catch (error) {
        showError(error.response?.data?.detail || 'Có lỗi xảy ra');
        console.error(error);
    }
}

// Open delete confirmation modal
function openDeleteModal(userId, username) {
    document.getElementById('deleteUserId').value = userId;
    document.getElementById('deleteUsername').textContent = username;
    confirmDeleteModal.show();
}

// Confirm delete
async function confirmDelete() {
    const userId = document.getElementById('deleteUserId').value;
    
    try {
        await apiCall(`/users/${userId}`, {
            method: 'DELETE'
        });
        
        showSuccess('Xóa tài khoản thành công');
        confirmDeleteModal.hide();
        await loadUsers();
    } catch (error) {
        showError(error.response?.data?.detail || 'Có lỗi xảy ra');
        console.error(error);
    }
}
