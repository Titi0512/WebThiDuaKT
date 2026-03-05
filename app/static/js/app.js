// API Base URL
const API_URL = '/api';

// Axios configuration
axios.defaults.baseURL = API_URL;
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Add token to all requests
axios.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    error => Promise.reject(error)
);

// Handle unauthorized responses
axios.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Helper function for API calls
async function apiCall(url, methodOrOptions = 'GET', data = null) {
    try {
        let config = {
            url,
            method: 'GET'
        };
        
        // Handle both old and new calling styles
        if (typeof methodOrOptions === 'string') {
            // New style: apiCall(url, 'GET', data)
            config.method = methodOrOptions;
            if (data) {
                config.data = data;
            }
        } else if (typeof methodOrOptions === 'object') {
            // Old style: apiCall(url, { method: 'POST', data: {...}, params: {...} })
            config = { url, ...methodOrOptions };
        }
        
        const response = await axios(config);
        return response.data;
    } catch (error) {
        console.error('API Error:', error);
        if (error.response) {
            console.error('Response data:', error.response.data);
            console.error('Response status:', error.response.status);
        }
        throw error;
    }
}

// Check authentication
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
}

// Get current user from localStorage
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    if (userStr) {
        try {
            return JSON.parse(userStr);
        } catch (error) {
            console.error('Error parsing user data:', error);
            return null;
        }
    }
    return null;
}

// Load user info
async function loadUserInfo() {
    try {
        const user = await apiCall('/auth/me');
        localStorage.setItem('user', JSON.stringify(user));
        
        // Update UI
        const userName = document.getElementById('userName');
        if (userName) {
            userName.textContent = user.ho_ten;
        }
        
        // Show/hide nav items based on auth
        const userNav = document.getElementById('userNav');
        const loginNav = document.getElementById('loginNav');
        if (userNav) userNav.style.display = 'block';
        if (loginNav) loginNav.style.display = 'none';
        
        // Show/hide admin-only menu items using class toggle
        const adminMenuItems = document.querySelectorAll('.admin-only');
        adminMenuItems.forEach(item => {
            if (user.role === 'admin') {
                item.classList.add('show-admin');
            } else {
                item.classList.remove('show-admin');
            }
        });
        
        return user;
    } catch (error) {
        console.error('Error loading user info:', error);
        const userNav = document.getElementById('userNav');
        const loginNav = document.getElementById('loginNav');
        if (userNav) userNav.style.display = 'none';
        if (loginNav) loginNav.style.display = 'block';
        return null;
    }
}

// Toast notification
function showToast(message, type = 'info') {
    // Create toast container if not exists
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast
    const toastId = 'toast-' + Date.now();
    const bgClass = {
        'success': 'bg-success',
        'error': 'bg-danger',
        'warning': 'bg-warning',
        'info': 'bg-info'
    }[type] || 'bg-info';
    
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center text-white ${bgClass} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast, { autohide: true, delay: 3000 });
    bsToast.show();
    
    // Remove toast after hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Show error message
function showError(message) {
    showToast(message, 'error');
}

// Show success message
function showSuccess(message) {
    showToast(message, 'success');
}

// Format date
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN');
}

// Format datetime
function formatDateTime(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString('vi-VN');
}

// Format number
function formatNumber(number) {
    if (!number) return '0';
    return new Intl.NumberFormat('vi-VN').format(number);
}

// Confirm dialog
function confirmDialog(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Load user info if logged in
    const token = localStorage.getItem('token');
    if (token) {
        loadUserInfo();
    } else {
        // Show login nav
        const userNav = document.getElementById('userNav');
        const loginNav = document.getElementById('loginNav');
        if (userNav) userNav.style.display = 'none';
        if (loginNav) loginNav.style.display = 'block';
    }
    
    // Highlight active nav item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
