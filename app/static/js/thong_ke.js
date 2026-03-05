// Statistics and reports

let unitChart, yearChart;

// Check authentication
if (!checkAuth()) {
    window.location.href = '/login';
}

// Load data on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadFilters();
    await loadStatistics();
});

// Load filters
async function loadFilters() {
    try {
        // Load years
        const currentYear = new Date().getFullYear();
        const yearSelect = document.getElementById('filterYear');
        for (let year = currentYear; year >= currentYear - 10; year--) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearSelect.appendChild(option);
        }
        
        // Load units
        const units = await apiCall('/don-vi/', { params: { limit: 1000 } });
        const unitSelect = document.getElementById('filterUnit');
        units.forEach(unit => {
            const option = document.createElement('option');
            option.value = unit.id;
            option.textContent = unit.ten_don_vi;
            unitSelect.appendChild(option);
        });
        
    } catch (error) {
        showError('Lỗi khi tải dữ liệu');
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const year = document.getElementById('filterYear').value;
        const unitId = document.getElementById('filterUnit').value;
        
        // Load unit statistics
        const params = {};
        if (year) params.nam = year;
        
        const unitStats = await apiCall('/thong-ke/theo-don-vi', { params });
        renderUnitStats(unitStats);
        
        // Load year statistics
        const yearParams = {};
        if (unitId) yearParams.don_vi_id = unitId;
        
        const yearStats = await apiCall('/thong-ke/theo-nam', { params: yearParams });
        renderYearStats(yearStats);
        
    } catch (error) {
        showError('Lỗi khi tải thống kê');
    }
}

// Render unit statistics
function renderUnitStats(data) {
    if (!data || data.length === 0) {
        document.getElementById('unitStatsTable').innerHTML = '<tr><td colspan="4" class="text-center text-muted">Không có dữ liệu</td></tr>';
        if (unitChart) unitChart.destroy();
        return;
    }
    
    // Render table
    const tbody = document.getElementById('unitStatsTable');
    tbody.innerHTML = data.map(item => `
        <tr>
            <td>${item.don_vi}</td>
            <td class="text-center">${item.ca_nhan}</td>
            <td class="text-center">${item.tap_the}</td>
            <td class="text-center"><strong>${item.so_luong}</strong></td>
        </tr>
    `).join('');
    
    // Render chart
    const ctx = document.getElementById('unitStatsChart');
    const labels = data.slice(0, 10).map(item => item.don_vi);
    const values = data.slice(0, 10).map(item => item.so_luong);
    
    if (unitChart) {
        unitChart.destroy();
    }
    
    unitChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Số lượng hồ sơ',
                data: values,
                backgroundColor: '#0d6efd'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Render year statistics
function renderYearStats(data) {
    if (!data || data.length === 0) {
        document.getElementById('yearStatsTable').innerHTML = '<tr><td colspan="4" class="text-center text-muted">Không có dữ liệu</td></tr>';
        if (yearChart) yearChart.destroy();
        return;
    }
    
    // Render table
    const tbody = document.getElementById('yearStatsTable');
    tbody.innerHTML = data.map(item => `
        <tr>
            <td>${item.nam}</td>
            <td class="text-center">${item.ca_nhan}</td>
            <td class="text-center">${item.tap_the}</td>
            <td class="text-center"><strong>${item.so_luong}</strong></td>
        </tr>
    `).join('');
    
    // Render chart
    const ctx = document.getElementById('yearStatsChart');
    const labels = data.map(item => item.nam);
    const caNhan = data.map(item => item.ca_nhan);
    const tapThe = data.map(item => item.tap_the);
    
    if (yearChart) {
        yearChart.destroy();
    }
    
    yearChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Cá nhân',
                    data: caNhan,
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Tập thể',
                    data: tapThe,
                    borderColor: '#198754',
                    backgroundColor: 'rgba(25, 135, 84, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Export to Excel
async function exportExcel() {
    try {
        const year = document.getElementById('filterYear').value;
        const unitId = document.getElementById('filterUnit').value;
        
        // Build query params
        const params = new URLSearchParams();
        if (year) params.append('nam', year);
        if (unitId) params.append('don_vi_id', unitId);
        
        // Get token
        const token = localStorage.getItem('token');
        
        // Download file
        const response = await fetch(`/api/export/report-excel?${params.toString()}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Lỗi khi xuất file Excel');
        }
        
        // Get filename from header or use default
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'bao_cao_thong_ke.xlsx';
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename=(.+)/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }
        
        // Download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showToast('Xuất file Excel thành công', 'success');
        
    } catch (error) {
        console.error('Export Excel error:', error);
        showError('Lỗi khi xuất file Excel');
    }
}

// Export to Word
async function exportWord() {
    try {
        const year = document.getElementById('filterYear').value;
        const unitId = document.getElementById('filterUnit').value;
        
        // Build query params
        const params = new URLSearchParams();
        if (year) params.append('nam', year);
        if (unitId) params.append('don_vi_id', unitId);
        
        // Get token
        const token = localStorage.getItem('token');
        
        // Download file
        const response = await fetch(`/api/export/report-word?${params.toString()}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Lỗi khi xuất file Word');
        }
        
        // Get filename from header or use default
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'bao_cao_thong_ke.docx';
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename=(.+)/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }
        
        // Download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showToast('Xuất file Word thành công', 'success');
        
    } catch (error) {
        console.error('Export Word error:', error);
        showError('Lỗi khi xuất file Word');
    }
}

// Export to PDF
async function exportPDF() {
    try {
        const year = document.getElementById('filterYear').value;
        const unitId = document.getElementById('filterUnit').value;
        
        // Build query params
        const params = new URLSearchParams();
        if (year) params.append('nam', year);
        if (unitId) params.append('don_vi_id', unitId);
        
        // Get token
        const token = localStorage.getItem('token');
        
        // Download file
        const response = await fetch(`/api/export/report-pdf?${params.toString()}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Lỗi khi xuất file PDF');
        }
        
        // Get filename from header or use default
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'bao_cao_thong_ke.pdf';
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename=(.+)/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }
        
        // Download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showToast('Xuất file PDF thành công', 'success');
        
    } catch (error) {
        console.error('Export PDF error:', error);
        showError('Lỗi khi xuất file PDF');
    }
}
