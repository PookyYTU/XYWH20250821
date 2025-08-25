// API服务模块 - 小雨微寒
// api.js

class ApiService {
    constructor() {
        // 根据环境设置API基础URL
        this.baseURL = this.getBaseURL();
        console.log('API Base URL:', this.baseURL);
    }
    
    getBaseURL() {
        // 检测当前环境
        const hostname = window.location.hostname;
        const port = window.location.port;
        
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            // 本地开发环境
            return 'http://localhost:8000';
        } else if (hostname === '47.105.52.49') {
            // 生产环境
            return `http://${hostname}`;
        } else {
            // 默认情况
            return `http://${hostname}:8000`;
        }
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}/api${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            throw error;
        }
    }
    
    // 美食记录相关API
    async getFoodRecords(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = `/food${queryString ? '?' + queryString : ''}`;
        return await this.request(endpoint);
    }
    
    async createFoodRecord(data) {
        return await this.request('/food/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    async updateFoodRecord(id, data) {
        return await this.request(`/food/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    async deleteFoodRecord(id) {
        return await this.request(`/food/${id}`, {
            method: 'DELETE'
        });
    }
    
    async getFoodStats() {
        return await this.request('/food/stats/summary');
    }
    
    // 电影记录相关API
    async getMovieRecords(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = `/movie${queryString ? '?' + queryString : ''}`;
        return await this.request(endpoint);
    }
    
    async createMovieRecord(data) {
        return await this.request('/movie/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    async updateMovieRecord(id, data) {
        return await this.request(`/movie/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    async deleteMovieRecord(id) {
        return await this.request(`/movie/${id}`, {
            method: 'DELETE'
        });
    }
    
    async getMovieStats() {
        return await this.request('/movie/stats/summary');
    }
    
    // 日历备注相关API
    async getCalendarNotes(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = `/calendar${queryString ? '?' + queryString : ''}`;
        return await this.request(endpoint);
    }
    
    async getNoteByDate(date) {
        return await this.request(`/calendar/${date}`);
    }
    
    async createOrUpdateNote(date, content) {
        return await this.request(`/calendar/${date}`, {
            method: 'PUT',
            body: JSON.stringify({ content })
        });
    }
    
    async deleteNote(date) {
        return await this.request(`/calendar/${date}`, {
            method: 'DELETE'
        });
    }
    
    async getMonthNotes(year, month) {
        return await this.request(`/calendar/month/${year}/${month}`);
    }
    
    // 文件管理相关API
    async getFileRecords(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = `/files${queryString ? '?' + queryString : ''}`;
        return await this.request(endpoint);
    }
    
    async uploadFile(file, description = '', category = '') {
        const formData = new FormData();
        formData.append('file', file);
        if (description) formData.append('description', description);
        if (category) formData.append('custom_category', category);
        
        return await this.request('/files/upload', {
            method: 'POST',
            headers: {}, // 让浏览器设置Content-Type
            body: formData
        });
    }
    
    async updateFileInfo(id, data) {
        return await this.request(`/files/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    async deleteFile(id) {
        return await this.request(`/files/${id}`, {
            method: 'DELETE'
        });
    }
    
    async getFileStats() {
        return await this.request('/files/stats/summary');
    }
    
    getDownloadUrl(fileId) {
        return `${this.baseURL}/api/files/download/${fileId}`;
    }
    
    // 健康检查
    async healthCheck() {
        return await this.request('/health');
    }
}

// 创建全局API服务实例
const apiService = new ApiService();

// 导出到全局作用域
window.apiService = apiService;