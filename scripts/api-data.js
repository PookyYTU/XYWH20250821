// 数据管理功能 - 小雨微寒 (使用后端API)

class ApiDataManager {
    constructor() {
        this.isOnline = navigator.onLine;
        this.setupOnlineListener();
        this.localStorageKeys = {
            musicPlayerState: 'musicPlayerState',
            musicPlayerPosition: 'musicPlayerPosition',
            appSettings: 'appSettings',
            // 离线缓存
            offlineFoodRecords: 'offlineFoodRecords',
            offlineMovieRecords: 'offlineMovieRecords',
            offlineCalendarNotes: 'offlineCalendarNotes'
        };
        
        this.defaultSettings = {
            theme: 'light',
            autoplay: false,
            notifications: true,
            useApi: true
        };
        
        this.init();
    }
    
    init() {
        console.log('API数据管理器初始化完成');
    }
    
    setupOnlineListener() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            console.log('网络已连接，将使用API');
        });
        
        window.addEventListener('offline', () => {
            this.isOnline = false;
            console.log('网络已断开，将使用本地存储');
        });
    }
    
    // 通用API调用方法
    async callApi(apiMethod, ...args) {
        if (this.isOnline && window.apiService) {
            try {
                return await apiMethod.apply(window.apiService, args);
            } catch (error) {
                console.error('API调用失败:', error);
                throw error;
            }
        } else {
            throw new Error('网络不可用或API服务未加载');
        }
    }
    
    // 美食记录相关方法
    async getFoodRecords(params = {}) {
        try {
            const response = await this.callApi(window.apiService.getFoodRecords, params);
            return response.data || [];
        } catch (error) {
            console.warn('使用离线数据:', error.message);
            return this.getOfflineFoodRecords();
        }
    }
    
    async addFoodRecord(record) {
        try {
            const response = await this.callApi(window.apiService.createFoodRecord, record);
            return response.success;
        } catch (error) {
            console.warn('保存到离线存储:', error.message);
            return this.saveOfflineFoodRecord(record);
        }
    }
    
    async updateFoodRecord(id, record) {
        try {
            const response = await this.callApi(window.apiService.updateFoodRecord, id, record);
            return response.success;
        } catch (error) {
            console.warn('更新离线数据失败:', error.message);
            return false;
        }
    }
    
    async deleteFoodRecord(id) {
        try {
            const response = await this.callApi(window.apiService.deleteFoodRecord, id);
            return response.success;
        } catch (error) {
            console.warn('删除离线数据失败:', error.message);
            return false;
        }
    }
    
    // 电影记录相关方法
    async getMovieRecords(params = {}) {
        try {
            const response = await this.callApi(window.apiService.getMovieRecords, params);
            return response.data || [];
        } catch (error) {
            console.warn('使用离线数据:', error.message);
            return this.getOfflineMovieRecords();
        }
    }
    
    async addMovieRecord(record) {
        try {
            const response = await this.callApi(window.apiService.createMovieRecord, record);
            return response.success;
        } catch (error) {
            console.warn('保存到离线存储:', error.message);
            return this.saveOfflineMovieRecord(record);
        }
    }
    
    async updateMovieRecord(id, record) {
        try {
            const response = await this.callApi(window.apiService.updateMovieRecord, id, record);
            return response.success;
        } catch (error) {
            console.warn('更新离线数据失败:', error.message);
            return false;
        }
    }
    
    async deleteMovieRecord(id) {
        try {
            const response = await this.callApi(window.apiService.deleteMovieRecord, id);
            return response.success;
        } catch (error) {
            console.warn('删除离线数据失败:', error.message);
            return false;
        }
    }
    
    // 日历备注相关方法
    async getCalendarNotes(params = {}) {
        try {
            const response = await this.callApi(window.apiService.getCalendarNotes, params);
            return response.data || [];
        } catch (error) {
            console.warn('使用离线数据:', error.message);
            return this.getOfflineCalendarNotes();
        }
    }
    
    async getNoteByDate(date) {\n        try {\n            const response = await this.callApi(window.apiService.getNoteByDate, date);\n            return response.data;\n        } catch (error) {\n            console.warn('使用离线数据:', error.message);\n            const notes = this.getOfflineCalendarNotes();\n            return notes[date] || null;\n        }\n    }\n    \n    async addCalendarNote(date, content) {\n        try {\n            const response = await this.callApi(window.apiService.createOrUpdateNote, date, content);\n            return response.success;\n        } catch (error) {\n            console.warn('保存到离线存储:', error.message);\n            return this.saveOfflineCalendarNote(date, content);\n        }\n    }\n    \n    async deleteCalendarNote(date) {\n        try {\n            const response = await this.callApi(window.apiService.deleteNote, date);\n            return response.success;\n        } catch (error) {\n            console.warn('删除离线数据失败:', error.message);\n            return false;\n        }\n    }\n    \n    async getMonthNotes(year, month) {\n        try {\n            const response = await this.callApi(window.apiService.getMonthNotes, year, month);\n            return response.data?.notes || {};\n        } catch (error) {\n            console.warn('使用离线数据:', error.message);\n            const allNotes = this.getOfflineCalendarNotes();\n            const monthNotes = {};\n            const prefix = `${year}-${month.toString().padStart(2, '0')}-`;\n            \n            Object.keys(allNotes).forEach(date => {\n                if (date.startsWith(prefix)) {\n                    monthNotes[date] = allNotes[date];\n                }\n            });\n            \n            return monthNotes;\n        }\n    }\n    \n    // 文件管理相关方法\n    async getFileRecords(params = {}) {\n        try {\n            const response = await this.callApi(window.apiService.getFileRecords, params);\n            return response.data || [];\n        } catch (error) {\n            console.warn('获取文件列表失败:', error.message);\n            return [];\n        }\n    }\n    \n    async uploadFile(file, description = '', category = '') {\n        try {\n            const response = await this.callApi(window.apiService.uploadFile, file, description, category);\n            return response;\n        } catch (error) {\n            console.error('文件上传失败:', error.message);\n            throw error;\n        }\n    }\n    \n    async deleteFile(id) {\n        try {\n            const response = await this.callApi(window.apiService.deleteFile, id);\n            return response.success;\n        } catch (error) {\n            console.error('文件删除失败:', error.message);\n            return false;\n        }\n    }\n    \n    // 离线存储方法\n    getOfflineFoodRecords() {\n        try {\n            return JSON.parse(localStorage.getItem(this.localStorageKeys.offlineFoodRecords) || '[]');\n        } catch (e) {\n            return [];\n        }\n    }\n    \n    saveOfflineFoodRecord(record) {\n        try {\n            const records = this.getOfflineFoodRecords();\n            const newRecord = {\n                ...record,\n                id: Date.now(),\n                created_at: new Date().toISOString()\n            };\n            records.unshift(newRecord);\n            localStorage.setItem(this.localStorageKeys.offlineFoodRecords, JSON.stringify(records));\n            return true;\n        } catch (e) {\n            console.error('保存离线美食记录失败:', e);\n            return false;\n        }\n    }\n    \n    getOfflineMovieRecords() {\n        try {\n            return JSON.parse(localStorage.getItem(this.localStorageKeys.offlineMovieRecords) || '[]');\n        } catch (e) {\n            return [];\n        }\n    }\n    \n    saveOfflineMovieRecord(record) {\n        try {\n            const records = this.getOfflineMovieRecords();\n            const newRecord = {\n                ...record,\n                id: Date.now(),\n                created_at: new Date().toISOString()\n            };\n            records.unshift(newRecord);\n            localStorage.setItem(this.localStorageKeys.offlineMovieRecords, JSON.stringify(records));\n            return true;\n        } catch (e) {\n            console.error('保存离线电影记录失败:', e);\n            return false;\n        }\n    }\n    \n    getOfflineCalendarNotes() {\n        try {\n            return JSON.parse(localStorage.getItem(this.localStorageKeys.offlineCalendarNotes) || '{}');\n        } catch (e) {\n            return {};\n        }\n    }\n    \n    saveOfflineCalendarNote(date, content) {\n        try {\n            const notes = this.getOfflineCalendarNotes();\n            if (content.trim()) {\n                notes[date] = content.trim();\n            } else {\n                delete notes[date];\n            }\n            localStorage.setItem(this.localStorageKeys.offlineCalendarNotes, JSON.stringify(notes));\n            return true;\n        } catch (e) {\n            console.error('保存离线日历备注失败:', e);\n            return false;\n        }\n    }\n    \n    // 应用设置\n    getSettings() {\n        try {\n            const settings = JSON.parse(localStorage.getItem(this.localStorageKeys.appSettings) || '{}');\n            return { ...this.defaultSettings, ...settings };\n        } catch (e) {\n            return this.defaultSettings;\n        }\n    }\n    \n    saveSettings(settings) {\n        try {\n            const currentSettings = this.getSettings();\n            const newSettings = { ...currentSettings, ...settings };\n            localStorage.setItem(this.localStorageKeys.appSettings, JSON.stringify(newSettings));\n            return true;\n        } catch (e) {\n            console.error('保存设置失败:', e);\n            return false;\n        }\n    }\n    \n    // 健康检查\n    async checkApiHealth() {\n        try {\n            const response = await this.callApi(window.apiService.healthCheck);\n            return response.status === 'healthy';\n        } catch (error) {\n            console.warn('API健康检查失败:', error.message);\n            return false;\n        }\n    }\n}\n\n// 创建全局数据管理器实例（保持向后兼容）\nconst dataManager = new ApiDataManager();\n\n// 为了向后兼容，保留旧的DataManager类名\nconst DataManager = ApiDataManager;\n\n// 导出到全局作用域\nwindow.dataManager = dataManager;\nwindow.DataManager = DataManager;