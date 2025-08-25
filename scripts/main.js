// 主要功能脚本 - 小雨微寒

// 全局变量
let currentSection = 'home';
// 注意：不再使用全局数组，改用API
// let foodRecords = JSON.parse(localStorage.getItem('foodRecords')) || [];
// let movieRecords = JSON.parse(localStorage.getItem('movieRecords')) || [];
// let calendarNotes = JSON.parse(localStorage.getItem('calendarNotes')) || {};
// let fileRecords = JSON.parse(localStorage.getItem('fileRecords')) || [];

// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 应用初始化
async function initializeApp() {
    setupNavigation();
    setupTimeCounter();
    setupModals();
    
    // 等待API服务初始化
    await waitForApiService();
    
    // 初始化数据显示
    await updateFoodGrid();
    await updateMovieGrid();
    
    initializeCalendar();
    initializeMusicPlayer();
    setupMobileMenu();
    initializeFileManager();
    
    // 设置默认显示首页
    showSection('home');
    
    console.log('小雨微寒应用初始化完成');
}

// 等待API服务初始化
async function waitForApiService() {
    let attempts = 0;
    const maxAttempts = 10;
    
    while (attempts < maxAttempts && !window.apiService) {
        await new Promise(resolve => setTimeout(resolve, 100));
        attempts++;
    }
    
    if (window.apiService) {
        // 检查API连接
        try {
            await dataManager.checkApiHealth();
            console.log('🚀 API服务连接成功');
        } catch (error) {
            console.warn('⚠️ API服务不可用，将使用本地模式');
        }
    } else {
        console.warn('⚠️ API服务未初始化，将使用本地模式');
    }
}

// 导航设置
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetSection = this.getAttribute('href').substring(1);
            showSection(targetSection);
            
            // 更新活动状态
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // 移动端关闭菜单
            const navMenu = document.querySelector('.nav-menu');
            const navToggle = document.querySelector('.nav-toggle');
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });
}

// 显示指定部分
function showSection(sectionId) {
    // 只处理存在的部分
    const validSections = ['home', 'food', 'movies', 'calendar', 'files'];
    if (!validSections.includes(sectionId)) {
        console.warn('无效的部分ID:', sectionId);
        return;
    }
    
    // 隐藏所有部分
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.remove('active'));
    
    // 显示目标部分
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        currentSection = sectionId;
        
        // 更新导航状态
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${sectionId}`) {
                link.classList.add('active');
            }
        });
        
        // 滚动到顶部
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// 移动端菜单设置
function setupMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
        
        // 点击菜单外部关闭菜单
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
    }
}

// 时光计数器设置
function setupTimeCounter() {
    const loveStartDate = new Date('2024-04-05');
    const birthdayDate = new Date('2000-07-08');
    
    function updateCounters() {
        const now = new Date();
        
        // 计算相恋天数
        const loveDays = Math.floor((now - loveStartDate) / (1000 * 60 * 60 * 24));
        const loveDaysElement = document.getElementById('lovedays');
        if (loveDaysElement) {
            loveDaysElement.textContent = loveDays;
        }
        
        // 计算到下一个生日的天数
        const thisYear = now.getFullYear();
        let nextBirthday = new Date(thisYear, birthdayDate.getMonth(), birthdayDate.getDate());
        
        // 如果今年的生日已过，计算明年的
        if (nextBirthday < now) {
            nextBirthday = new Date(thisYear + 1, birthdayDate.getMonth(), birthdayDate.getDate());
        }
        
        const birthdayDays = Math.ceil((nextBirthday - now) / (1000 * 60 * 60 * 24));
        const birthdayElement = document.getElementById('birthday');
        if (birthdayElement) {
            birthdayElement.textContent = birthdayDays;
        }
    }
    
    // 立即更新一次
    updateCounters();
    
    // 每天更新一次
    setInterval(updateCounters, 24 * 60 * 60 * 1000);
}

// 模态框设置
function setupModals() {
    // 点击模态框外部关闭
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });
    
    // ESC键关闭模态框
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const activeModal = document.querySelector('.modal.active');
            if (activeModal) {
                activeModal.classList.remove('active');
            }
        }
    });
    
    // 表单提交处理
    setupFoodForm();
    setupMovieForm();
    setupNoteForm();
}

// 美食表单设置
function setupFoodForm() {
    const form = document.getElementById('foodForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const foodRecord = {
                name: document.getElementById('foodName').value,
                location: document.getElementById('foodLocation').value,
                price: parseFloat(document.getElementById('foodPrice').value),
                rating: parseInt(document.getElementById('foodRating').value),
                date: document.getElementById('foodDate').value,
                notes: document.getElementById('foodNotes').value
            };
            
            try {
                const success = await dataManager.addFoodRecord(foodRecord);
                if (success) {
                    await updateFoodGrid();
                    closeFoodModal();
                    showMessage('美食记录添加成功！', 'success');
                    form.reset();
                } else {
                    showMessage('美食记录添加失败，请重试', 'error');
                }
            } catch (error) {
                console.error('添加美食记录失败:', error);
                showMessage('美食记录添加失败：' + error.message, 'error');
            }
        });
    }
}

// 电影表单设置
function setupMovieForm() {
    const form = document.getElementById('movieForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const movieRecord = {
                name: document.getElementById('movieName').value,
                cinema: document.getElementById('movieCinema').value,
                date: document.getElementById('movieDate').value,
                rating: parseInt(document.getElementById('movieRating').value),
                review: document.getElementById('movieReview').value
            };
            
            try {
                const success = await dataManager.addMovieRecord(movieRecord);
                if (success) {
                    await updateMovieGrid();
                    closeMovieModal();
                    showMessage('电影记录添加成功！', 'success');
                    form.reset();
                } else {
                    showMessage('电影记录添加失败，请重试', 'error');
                }
            } catch (error) {
                console.error('添加电影记录失败:', error);
                showMessage('电影记录添加失败：' + error.message, 'error');
            }
        });
    }
}

// 备注表单设置
function setupNoteForm() {
    const form = document.getElementById('noteForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const selectedDate = document.getElementById('selectedDate').value;
            const noteContent = document.getElementById('noteContent').value;
            
            if (selectedDate && noteContent.trim()) {
                try {
                    const success = await dataManager.addCalendarNote(selectedDate, noteContent.trim());
                    if (success) {
                        updateCalendarDisplay();
                        closeNoteModal();
                        showMessage('备注保存成功！', 'success');
                    } else {
                        showMessage('备注保存失败，请重试', 'error');
                    }
                } catch (error) {
                    console.error('保存备注失败:', error);
                    showMessage('备注保存失败：' + error.message, 'error');
                }
            } else {
                showMessage('请输入备注内容', 'warning');
            }
                form.reset();
            }
        });
    }
}

// 更新美食网格
async function updateFoodGrid() {
    const grid = document.getElementById('foodGrid');
    if (!grid) return;
    
    try {
        const foodRecords = await dataManager.getFoodRecords({ limit: 50, sort_order: 'desc' });
        
        if (foodRecords.length === 0) {
            grid.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-utensils"></i>
                    <h3>还没有美食记录</h3>
                    <p>开始记录你们一起品尝的美食吧！</p>
                </div>
            `;
            return;
        }
        
        grid.innerHTML = foodRecords.map(record => createFoodCard(record)).join('');
    } catch (error) {
        console.error('加载美食记录失败:', error);
        grid.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>加载失败</h3>
                <p>无法加载美食记录，请刷新页面重试</p>
            </div>
        `;
    }
}

// 创建美食卡片
function createFoodCard(record) {
    const stars = '⭐'.repeat(record.rating);
    const formattedDate = new Date(record.date).toLocaleDateString('zh-CN');
    
    return `
        <div class="card" onclick="viewFoodDetail(${record.id})">
            <div class="card-header">
                <h3 class="card-title">${record.name}</h3>
                <span class="card-date">${formattedDate}</span>
            </div>
            <div class="card-content">
                <div class="card-info">
                    <div class="card-info-item">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>${record.location}</span>
                    </div>
                    <div class="card-info-item">
                        <i class="fas fa-yen-sign"></i>
                        <span>¥${record.price.toFixed(2)}</span>
                    </div>
                    <div class="card-rating">
                        <span>${stars}</span>
                    </div>
                </div>
                ${record.notes ? `<p class="card-description">${record.notes}</p>` : ''}
            </div>
            <div class="card-actions">
                <button class="card-action-btn" onclick="event.stopPropagation(); editFood(${record.id})">
                    <i class="fas fa-edit"></i> 编辑
                </button>
                <button class="card-action-btn delete" onclick="event.stopPropagation(); deleteFood(${record.id})">
                    <i class="fas fa-trash"></i> 删除
                </button>
            </div>
        </div>
    `;
}

async function updateMovieGrid() {
    const grid = document.getElementById('movieGrid');
    if (!grid) return;
    
    try {
        const movieRecords = await dataManager.getMovieRecords({ limit: 50, sort_order: 'desc' });
        
        if (movieRecords.length === 0) {
            grid.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-film"></i>
                    <h3>还没有电影记录</h3>
                    <p>开始记录你们一起观看的电影吧！</p>
                </div>
            `;
            return;
        }
        
        grid.innerHTML = movieRecords.map(record => createMovieCard(record)).join('');
    } catch (error) {
        console.error('加载电影记录失败:', error);
        grid.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>加载失败</h3>
                <p>无法加载电影记录，请刷新页面重试</p>
            </div>
        `;
    }
}

// 创建电影卡片
function createMovieCard(record) {
    const stars = '⭐'.repeat(record.rating);
    const formattedDate = new Date(record.date).toLocaleDateString('zh-CN');
    
    return `
        <div class="card" onclick="viewMovieDetail(${record.id})">
            <div class="card-header">
                <h3 class="card-title">${record.name}</h3>
                <span class="card-date">${formattedDate}</span>
            </div>
            <div class="card-content">
                <div class="card-info">
                    <div class="card-info-item">
                        <i class="fas fa-building"></i>
                        <span>${record.cinema}</span>
                    </div>
                    <div class="card-rating">
                        <span>${stars}</span>
                    </div>
                </div>
                ${record.review ? `<p class="card-description">${record.review}</p>` : ''}
            </div>
            <div class="card-actions">
                <button class="card-action-btn" onclick="event.stopPropagation(); editMovie(${record.id})">
                    <i class="fas fa-edit"></i> 编辑
                </button>
                <button class="card-action-btn delete" onclick="event.stopPropagation(); deleteMovie(${record.id})">
                    <i class="fas fa-trash"></i> 删除
                </button>
            </div>
        </div>
    `;
}

// 模态框控制函数
function openFoodModal() {
    const modal = document.getElementById('foodModal');
    if (modal) {
        modal.classList.add('active');
        // 设置默认日期为今天
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('foodDate').value = today;
    }
}

function closeFoodModal() {
    const modal = document.getElementById('foodModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

function openMovieModal() {
    const modal = document.getElementById('movieModal');
    if (modal) {
        modal.classList.add('active');
        // 设置默认日期为今天
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('movieDate').value = today;
    }
}

function closeMovieModal() {
    const modal = document.getElementById('movieModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

async function openNoteModal(date) {
    const modal = document.getElementById('noteModal');
    if (modal) {
        modal.classList.add('active');
        document.getElementById('selectedDate').value = date;
        
        // 加载当前备注
        try {
            const noteData = await dataManager.getNoteByDate(date);
            const content = noteData ? noteData.content : '';
            document.getElementById('noteContent').value = content;
        } catch (error) {
            console.warn('加载备注失败:', error);
            // 使用本地存储作为备用
            const calendarNotes = JSON.parse(localStorage.getItem('calendarNotes')) || {};
            document.getElementById('noteContent').value = calendarNotes[date] || '';
        }
    }
}

function closeNoteModal() {
    const modal = document.getElementById('noteModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// 记录操作函数
async function deleteFood(id) {
    if (confirm('确定要删除这条美食记录吗？')) {
        try {
            const success = await dataManager.deleteFoodRecord(id);
            if (success) {
                await updateFoodGrid();
                showMessage('美食记录已删除', 'success');
            } else {
                showMessage('删除失败，请重试', 'error');
            }
        } catch (error) {
            console.error('删除美食记录失败:', error);
            showMessage('删除失败：' + error.message, 'error');
        }
    }
}

async function deleteMovie(id) {
    if (confirm('确定要删除这条电影记录吗？')) {
        try {
            const success = await dataManager.deleteMovieRecord(id);
            if (success) {
                await updateMovieGrid();
                showMessage('电影记录已删除', 'success');
            } else {
                showMessage('删除失败，请重试', 'error');
            }
        } catch (error) {
            console.error('删除电影记录失败:', error);
            showMessage('删除失败：' + error.message, 'error');
        }
    }
}

function editFood(id) {
    const record = foodRecords.find(r => r.id === id);
    if (record) {
        // 填充表单
        document.getElementById('foodName').value = record.name;
        document.getElementById('foodLocation').value = record.location;
        document.getElementById('foodPrice').value = record.price;
        document.getElementById('foodRating').value = record.rating;
        document.getElementById('foodDate').value = record.date;
        document.getElementById('foodNotes').value = record.notes || '';
        
        // 删除原记录
        deleteFood(id);
        
        // 打开模态框
        openFoodModal();
    }
}

function editMovie(id) {
    const record = movieRecords.find(r => r.id === id);
    if (record) {
        // 填充表单
        document.getElementById('movieName').value = record.name;
        document.getElementById('movieCinema').value = record.cinema;
        document.getElementById('movieDate').value = record.date;
        document.getElementById('movieRating').value = record.rating;
        document.getElementById('movieReview').value = record.review || '';
        
        // 删除原记录
        deleteMovie(id);
        
        // 打开模态框
        openMovieModal();
    }
}

function viewFoodDetail(id) {
    const record = foodRecords.find(r => r.id === id);
    if (record) {
        const stars = '⭐'.repeat(record.rating);
        const formattedDate = new Date(record.date).toLocaleDateString('zh-CN');
        
        // 创建详情模态框
        const detailModal = document.createElement('div');
        detailModal.className = 'modal active';
        detailModal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>美食详情</h3>
                    <button class="close-btn" onclick="this.closest('.modal').remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="detail-content">
                    <div class="detail-image">
                        <i class="fas fa-utensils detail-icon"></i>
                    </div>
                    <div class="detail-info">
                        <h4>${record.name}</h4>
                        <div class="detail-grid">
                            <div class="detail-item">
                                <label>地点：</label>
                                <span>${record.location}</span>
                            </div>
                            <div class="detail-item">
                                <label>价格：</label>
                                <span>¥${record.price.toFixed(2)}</span>
                            </div>
                            <div class="detail-item">
                                <label>评分：</label>
                                <span>${stars}</span>
                            </div>
                            <div class="detail-item">
                                <label>日期：</label>
                                <span>${formattedDate}</span>
                            </div>
                            ${record.notes ? `
                            <div class="detail-item full-width">
                                <label>备注：</label>
                                <p>${record.notes}</p>
                            </div>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(detailModal);
        
        // 点击背景关闭
        detailModal.addEventListener('click', function(e) {
            if (e.target === detailModal) {
                detailModal.remove();
            }
        });
    }
}

function viewMovieDetail(id) {
    const record = movieRecords.find(r => r.id === id);
    if (record) {
        const stars = '⭐'.repeat(record.rating);
        const formattedDate = new Date(record.date).toLocaleDateString('zh-CN');
        
        // 创建详情模态框
        const detailModal = document.createElement('div');
        detailModal.className = 'modal active';
        detailModal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>电影详情</h3>
                    <button class="close-btn" onclick="this.closest('.modal').remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="detail-content">
                    <div class="detail-image">
                        <i class="fas fa-film detail-icon"></i>
                    </div>
                    <div class="detail-info">
                        <h4>${record.name}</h4>
                        <div class="detail-grid">
                            <div class="detail-item">
                                <label>影院：</label>
                                <span>${record.cinema}</span>
                            </div>
                            <div class="detail-item">
                                <label>观影日期：</label>
                                <span>${formattedDate}</span>
                            </div>
                            <div class="detail-item">
                                <label>评分：</label>
                                <span>${stars}</span>
                            </div>
                            ${record.review ? `
                            <div class="detail-item full-width">
                                <label>影评：</label>
                                <p>${record.review}</p>
                            </div>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(detailModal);
        
        // 点击背景关闭
        detailModal.addEventListener('click', function(e) {
            if (e.target === detailModal) {
                detailModal.remove();
            }
        });
    }
}

// 消息提示
function showMessage(text, type = 'success') {
    // 移除现有消息
    const existingMessage = document.querySelector('.message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // 创建新消息
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;
    
    document.body.appendChild(message);
    
    // 3秒后自动移除
    setTimeout(() => {
        if (message.parentNode) {
            message.remove();
        }
    }, 3000);
}

// 导出供HTML调用的函数
window.showSection = showSection;
window.openFoodModal = openFoodModal;
window.closeFoodModal = closeFoodModal;
window.openMovieModal = openMovieModal;
window.closeMovieModal = closeMovieModal;
window.openNoteModal = openNoteModal;
window.closeNoteModal = closeNoteModal;
window.deleteFood = deleteFood;
window.deleteMovie = deleteMovie;
window.editFood = editFood;
window.editMovie = editMovie;
window.viewFoodDetail = viewFoodDetail;
window.viewMovieDetail = viewMovieDetail;
window.openFileModal = openFileModal;
window.closeFileModal = closeFileModal;
window.deleteFile = deleteFile;
window.downloadFile = downloadFile;

// 文件管理功能
function initializeFileManager() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('fileUploadArea');
    const uploadPlaceholder = uploadArea.querySelector('.upload-placeholder');
    
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }
    
    if (uploadPlaceholder) {
        // 拖拽上传功能
        uploadPlaceholder.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });
        
        uploadPlaceholder.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
        });
        
        uploadPlaceholder.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            const files = e.dataTransfer.files;
            handleFiles(files);
        });
        
        // 点击上传
        uploadPlaceholder.addEventListener('click', function() {
            fileInput.click();
        });
    }
    
    updateFileGrid();
    setupFileForm();
}

function handleFileSelect(e) {
    const files = e.target.files;
    handleFiles(files);
}

function handleFiles(files) {
    for (let file of files) {
        // 简单的文件信息暂存
        const fileData = {
            id: Date.now() + Math.random(),
            name: file.name,
            size: file.size,
            type: file.type,
            category: getFileCategory(file.type),
            uploadDate: new Date().toISOString(),
            description: '',
            url: URL.createObjectURL(file) // 临时URL，实际项目中需要上传到服务器
        };
        
        // 打开文件信息弹窗
        currentFileData = fileData;
        document.getElementById('fileName').value = file.name.split('.')[0];
        document.getElementById('fileCategory').value = fileData.category;
        openFileModal();
    }
}

function getFileCategory(mimeType) {
    if (mimeType.startsWith('image/')) return 'image';
    if (mimeType.startsWith('audio/')) return 'audio';
    if (mimeType.startsWith('video/')) return 'video';
    if (mimeType.includes('document') || mimeType.includes('pdf') || mimeType.includes('text')) return 'document';
    return 'other';
}

let currentFileData = null;

function setupFileForm() {
    const form = document.getElementById('fileForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (currentFileData) {
                currentFileData.name = document.getElementById('fileName').value;
                currentFileData.description = document.getElementById('fileDescription').value;
                currentFileData.category = document.getElementById('fileCategory').value;
                
                fileRecords.unshift(currentFileData);
                localStorage.setItem('fileRecords', JSON.stringify(fileRecords));
                
                updateFileGrid();
                closeFileModal();
                showMessage('文件保存成功！', 'success');
                form.reset();
                currentFileData = null;
            }
        });
    }
}

function updateFileGrid() {
    const grid = document.getElementById('filesGrid');
    if (!grid) return;
    
    if (fileRecords.length === 0) {
        grid.innerHTML = `
            <div class="empty-files">
                <i class="fas fa-folder-open"></i>
                <h3>还没有文件</h3>
                <p>上传一些文件来开始使用文件暂存功能吧！</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = fileRecords.map(file => createFileCard(file)).join('');
}

function createFileCard(file) {
    const formattedDate = new Date(file.uploadDate).toLocaleDateString('zh-CN');
    const formattedSize = formatFileSize(file.size);
    
    return `
        <div class="file-card">
            <div class="file-header">
                <div class="file-icon ${file.category}">
                    <i class="fas fa-${getFileIcon(file.category)}"></i>
                </div>
                <div class="file-info">
                    <div class="file-name">${file.name}</div>
                    <div class="file-meta">
                        <span><i class="fas fa-calendar"></i> ${formattedDate}</span>
                        <span><i class="fas fa-hdd"></i> ${formattedSize}</span>
                    </div>
                </div>
            </div>
            ${file.description ? `<div class="file-description">${file.description}</div>` : ''}
            <div class="file-actions">
                <button class="file-action-btn download" onclick="downloadFile(${file.id})">
                    <i class="fas fa-download"></i> 下载
                </button>
                <button class="file-action-btn delete" onclick="deleteFile(${file.id})">
                    <i class="fas fa-trash"></i> 删除
                </button>
            </div>
        </div>
    `;
}

function getFileIcon(category) {
    const icons = {
        image: 'image',
        document: 'file-alt',
        audio: 'music',
        video: 'video',
        other: 'file'
    };
    return icons[category] || 'file';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function openFileModal() {
    const modal = document.getElementById('fileModal');
    if (modal) {
        modal.classList.add('active');
    }
}

function closeFileModal() {
    const modal = document.getElementById('fileModal');
    if (modal) {
        modal.classList.remove('active');
    }
    currentFileData = null;
}

function deleteFile(id) {
    if (confirm('确定要删除这个文件吗？')) {
        const file = fileRecords.find(f => f.id === id);
        if (file && file.url) {
            URL.revokeObjectURL(file.url); // 释放临时URL
        }
        
        fileRecords = fileRecords.filter(file => file.id !== id);
        localStorage.setItem('fileRecords', JSON.stringify(fileRecords));
        updateFileGrid();
        showMessage('文件已删除', 'success');
    }
}

function downloadFile(id) {
    const file = fileRecords.find(f => f.id === id);
    if (file && file.url) {
        const link = document.createElement('a');
        link.href = file.url;
        link.download = file.name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        showMessage('文件下载已开始', 'success');
    } else {
        showMessage('文件不存在或已损坏', 'error');
    }
}