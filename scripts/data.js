// 数据管理功能 - 小雨微寒

class DataManager {
    constructor() {
        this.storageKeys = {
            foodRecords: 'foodRecords',
            movieRecords: 'movieRecords',
            calendarNotes: 'calendarNotes',
            musicPlayerState: 'musicPlayerState',
            musicPlayerPosition: 'musicPlayerPosition',
            appSettings: 'appSettings'
        };
        
        this.defaultSettings = {
            theme: 'light',
            autoplay: false,
            notifications: true,
            dataBackup: true,
            lastBackup: null
        };
        
        this.init();
    }
    
    init() {
        this.initializeStorage();
        this.setupAutoBackup();
        console.log('数据管理器初始化完成');
    }
    
    // 初始化存储
    initializeStorage() {
        // 检查并初始化各种数据
        Object.values(this.storageKeys).forEach(key => {
            if (!localStorage.getItem(key)) {
                switch(key) {
                    case 'foodRecords':
                    case 'movieRecords':
                        localStorage.setItem(key, JSON.stringify([]));
                        break;
                    case 'calendarNotes':
                        localStorage.setItem(key, JSON.stringify({}));
                        break;
                    case 'appSettings':
                        localStorage.setItem(key, JSON.stringify(this.defaultSettings));
                        break;
                }
            }
        });
        
        // 数据迁移和修复
        this.migrateData();
        this.repairData();
    }
    
    // 数据迁移
    migrateData() {
        const version = this.getDataVersion();
        
        if (version < 1.1) {
            // 示例：添加新的字段
            this.migrateTo1_1();
        }
        
        this.setDataVersion('1.1');
    }
    
    migrateTo1_1() {
        // 为美食记录添加新字段
        const foodRecords = this.getFoodRecords();
        const updatedRecords = foodRecords.map(record => ({
            ...record,
            tags: record.tags || [],
            images: record.images || []
        }));
        this.saveFoodRecords(updatedRecords);
        
        // 为电影记录添加新字段
        const movieRecords = this.getMovieRecords();
        const updatedMovies = movieRecords.map(record => ({
            ...record,
            genre: record.genre || '',
            director: record.director || '',
            actors: record.actors || []
        }));
        this.saveMovieRecords(updatedMovies);
    }
    
    // 数据修复
    repairData() {
        try {
            // 修复损坏的JSON数据
            Object.values(this.storageKeys).forEach(key => {
                const data = localStorage.getItem(key);
                if (data) {
                    try {
                        JSON.parse(data);
                    } catch (e) {
                        console.warn(`修复损坏的数据: ${key}`);
                        localStorage.removeItem(key);
                        this.initializeStorage();
                    }
                }
            });
            
            // 修复数据一致性
            this.repairDataConsistency();
            
        } catch (error) {
            console.error('数据修复失败:', error);
        }
    }
    
    repairDataConsistency() {
        // 确保所有记录都有必需的字段
        const foodRecords = this.getFoodRecords();
        const repairedFood = foodRecords.filter(record => 
            record.id && record.name && record.date
        );
        if (repairedFood.length !== foodRecords.length) {
            this.saveFoodRecords(repairedFood);
        }
        
        const movieRecords = this.getMovieRecords();
        const repairedMovies = movieRecords.filter(record => 
            record.id && record.name && record.date
        );
        if (repairedMovies.length !== movieRecords.length) {
            this.saveMovieRecords(repairedMovies);
        }
    }
    
    // 获取数据版本
    getDataVersion() {
        return parseFloat(localStorage.getItem('dataVersion') || '1.0');
    }
    
    setDataVersion(version) {
        localStorage.setItem('dataVersion', version);
    }
    
    // 美食记录相关方法
    getFoodRecords() {
        try {
            return JSON.parse(localStorage.getItem(this.storageKeys.foodRecords) || '[]');
        } catch (e) {
            console.error('获取美食记录失败:', e);
            return [];
        }
    }
    
    saveFoodRecords(records) {
        try {
            localStorage.setItem(this.storageKeys.foodRecords, JSON.stringify(records));
            this.updateBackupTimestamp();
            return true;
        } catch (e) {
            console.error('保存美食记录失败:', e);
            return false;
        }
    }
    
    addFoodRecord(record) {
        const records = this.getFoodRecords();
        const newRecord = {
            ...record,
            id: record.id || Date.now(),
            createdAt: record.createdAt || new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        records.unshift(newRecord);
        return this.saveFoodRecords(records);
    }
    
    updateFoodRecord(id, updates) {
        const records = this.getFoodRecords();
        const index = records.findIndex(r => r.id === id);
        if (index !== -1) {
            records[index] = {
                ...records[index],
                ...updates,
                updatedAt: new Date().toISOString()
            };
            return this.saveFoodRecords(records);
        }
        return false;
    }
    
    deleteFoodRecord(id) {
        const records = this.getFoodRecords();
        const filteredRecords = records.filter(r => r.id !== id);
        return this.saveFoodRecords(filteredRecords);
    }
    
    // 电影记录相关方法
    getMovieRecords() {
        try {
            return JSON.parse(localStorage.getItem(this.storageKeys.movieRecords) || '[]');
        } catch (e) {
            console.error('获取电影记录失败:', e);
            return [];
        }
    }
    
    saveMovieRecords(records) {
        try {
            localStorage.setItem(this.storageKeys.movieRecords, JSON.stringify(records));
            this.updateBackupTimestamp();
            return true;
        } catch (e) {
            console.error('保存电影记录失败:', e);
            return false;
        }
    }
    
    addMovieRecord(record) {
        const records = this.getMovieRecords();
        const newRecord = {
            ...record,
            id: record.id || Date.now(),
            createdAt: record.createdAt || new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        records.unshift(newRecord);
        return this.saveMovieRecords(records);
    }
    
    updateMovieRecord(id, updates) {
        const records = this.getMovieRecords();
        const index = records.findIndex(r => r.id === id);
        if (index !== -1) {
            records[index] = {
                ...records[index],
                ...updates,
                updatedAt: new Date().toISOString()
            };
            return this.saveMovieRecords(records);
        }
        return false;
    }
    
    deleteMovieRecord(id) {
        const records = this.getMovieRecords();
        const filteredRecords = records.filter(r => r.id !== id);
        return this.saveMovieRecords(filteredRecords);
    }
    
    // 日历备注相关方法
    getCalendarNotes() {
        try {
            return JSON.parse(localStorage.getItem(this.storageKeys.calendarNotes) || '{}');
        } catch (e) {
            console.error('获取日历备注失败:', e);
            return {};
        }
    }
    
    saveCalendarNotes(notes) {
        try {
            localStorage.setItem(this.storageKeys.calendarNotes, JSON.stringify(notes));
            this.updateBackupTimestamp();
            return true;
        } catch (e) {
            console.error('保存日历备注失败:', e);
            return false;
        }
    }
    
    addCalendarNote(date, note) {
        const notes = this.getCalendarNotes();
        if (note.trim()) {
            notes[date] = note.trim();
        } else {
            delete notes[date];
        }
        return this.saveCalendarNotes(notes);
    }
    
    deleteCalendarNote(date) {
        const notes = this.getCalendarNotes();
        delete notes[date];
        return this.saveCalendarNotes(notes);
    }
    
    // 应用设置相关方法
    getSettings() {
        try {
            const settings = JSON.parse(localStorage.getItem(this.storageKeys.appSettings) || '{}');
            return { ...this.defaultSettings, ...settings };
        } catch (e) {
            console.error('获取设置失败:', e);
            return this.defaultSettings;
        }
    }
    
    saveSettings(settings) {
        try {
            const currentSettings = this.getSettings();
            const newSettings = { ...currentSettings, ...settings };
            localStorage.setItem(this.storageKeys.appSettings, JSON.stringify(newSettings));
            return true;
        } catch (e) {
            console.error('保存设置失败:', e);
            return false;
        }
    }
    
    // 数据统计
    getStatistics() {
        const foodRecords = this.getFoodRecords();
        const movieRecords = this.getMovieRecords();
        const calendarNotes = this.getCalendarNotes();
        
        // 基础统计
        const stats = {
            totalFoodRecords: foodRecords.length,
            totalMovieRecords: movieRecords.length,
            totalCalendarNotes: Object.keys(calendarNotes).length
        };
        
        // 美食统计
        if (foodRecords.length > 0) {
            stats.avgFoodRating = (foodRecords.reduce((sum, r) => sum + r.rating, 0) / foodRecords.length).toFixed(1);
            stats.totalFoodCost = foodRecords.reduce((sum, r) => sum + (r.price || 0), 0).toFixed(2);
            stats.topFoodLocations = this.getTopLocations(foodRecords);
        }
        
        // 电影统计
        if (movieRecords.length > 0) {
            stats.avgMovieRating = (movieRecords.reduce((sum, r) => sum + r.rating, 0) / movieRecords.length).toFixed(1);
            stats.topCinemas = this.getTopCinemas(movieRecords);
        }
        
        // 时间统计
        const loveStartDate = new Date('2024-04-05');
        const today = new Date();
        stats.daysTogether = Math.floor((today - loveStartDate) / (1000 * 60 * 60 * 24));
        
        return stats;
    }
    
    getTopLocations(foodRecords) {
        const locationCount = {};
        foodRecords.forEach(record => {
            const location = record.location;
            locationCount[location] = (locationCount[location] || 0) + 1;
        });
        
        return Object.entries(locationCount)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([location, count]) => ({ location, count }));
    }
    
    getTopCinemas(movieRecords) {
        const cinemaCount = {};
        movieRecords.forEach(record => {
            const cinema = record.cinema;
            cinemaCount[cinema] = (cinemaCount[cinema] || 0) + 1;
        });
        
        return Object.entries(cinemaCount)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([cinema, count]) => ({ cinema, count }));
    }
    
    // 数据导出
    exportAllData() {
        const exportData = {
            exportDate: new Date().toISOString(),
            version: this.getDataVersion(),
            data: {
                foodRecords: this.getFoodRecords(),
                movieRecords: this.getMovieRecords(),
                calendarNotes: this.getCalendarNotes(),
                settings: this.getSettings()
            },
            statistics: this.getStatistics()
        };
        
        return exportData;
    }
    
    downloadDataExport() {
        try {
            const exportData = this.exportAllData();
            const dataStr = JSON.stringify(exportData, null, 2);
            const blob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            
            const link = document.createElement('a');
            link.href = url;
            link.download = `xiaoyu-weihan-backup-${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
            
            this.updateBackupTimestamp();
            
            if (window.showMessage) {
                window.showMessage('数据导出成功！', 'success');
            }
            
            return true;
        } catch (error) {
            console.error('数据导出失败:', error);
            if (window.showMessage) {
                window.showMessage('数据导出失败', 'error');
            }
            return false;
        }
    }
    
    // 数据导入
    importData(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const importData = JSON.parse(e.target.result);
                
                if (this.validateImportData(importData)) {
                    this.performDataImport(importData);
                    
                    if (window.showMessage) {
                        window.showMessage('数据导入成功！', 'success');
                    }
                    
                    // 刷新页面以更新所有组件
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else {
                    throw new Error('无效的数据格式');
                }
            } catch (error) {
                console.error('数据导入失败:', error);
                if (window.showMessage) {
                    window.showMessage('数据导入失败，请检查文件格式', 'error');
                }
            }
        };
        reader.readAsText(file);
    }
    
    validateImportData(data) {
        return data &&
               data.data &&
               Array.isArray(data.data.foodRecords) &&
               Array.isArray(data.data.movieRecords) &&
               typeof data.data.calendarNotes === 'object';
    }
    
    performDataImport(importData) {
        const { data } = importData;
        
        // 备份当前数据
        this.createBackup();
        
        // 导入新数据
        this.saveFoodRecords(data.foodRecords || []);
        this.saveMovieRecords(data.movieRecords || []);
        this.saveCalendarNotes(data.calendarNotes || {});
        
        if (data.settings) {
            this.saveSettings(data.settings);
        }
        
        this.updateBackupTimestamp();
    }
    
    // 备份管理
    createBackup() {
        const backupData = this.exportAllData();
        const backupKey = `backup_${Date.now()}`;
        
        try {
            localStorage.setItem(backupKey, JSON.stringify(backupData));
            this.cleanOldBackups();
            return backupKey;
        } catch (e) {
            console.error('创建备份失败:', e);
            return null;
        }
    }
    
    cleanOldBackups() {
        const maxBackups = 5;
        const backupKeys = Object.keys(localStorage)
            .filter(key => key.startsWith('backup_'))
            .sort()
            .reverse();
        
        if (backupKeys.length > maxBackups) {
            backupKeys.slice(maxBackups).forEach(key => {
                localStorage.removeItem(key);
            });
        }
    }
    
    updateBackupTimestamp() {
        const settings = this.getSettings();
        settings.lastBackup = new Date().toISOString();
        this.saveSettings(settings);
    }
    
    setupAutoBackup() {
        const settings = this.getSettings();
        if (settings.dataBackup) {
            // 每天自动备份一次
            const lastBackup = settings.lastBackup ? new Date(settings.lastBackup) : null;
            const now = new Date();
            
            if (!lastBackup || (now - lastBackup) > 24 * 60 * 60 * 1000) {
                this.createBackup();
            }
        }
    }
    
    // 数据清理
    clearAllData() {
        if (confirm('确定要清除所有数据吗？此操作不可恢复！')) {
            Object.values(this.storageKeys).forEach(key => {
                localStorage.removeItem(key);
            });
            
            // 清理备份
            Object.keys(localStorage)
                .filter(key => key.startsWith('backup_'))
                .forEach(key => localStorage.removeItem(key));
            
            this.initializeStorage();
            
            if (window.showMessage) {
                window.showMessage('所有数据已清除', 'success');
            }
            
            // 刷新页面
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        }
    }
    
    // 获取存储使用情况
    getStorageUsage() {
        let totalSize = 0;
        const usage = {};
        
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key)) {
                const size = localStorage[key].length;
                totalSize += size;
                usage[key] = size;
            }
        }
        
        return {
            total: totalSize,
            totalKB: (totalSize / 1024).toFixed(2),
            items: usage,
            quota: this.getStorageQuota()
        };
    }
    
    getStorageQuota() {
        // 大多数浏览器的localStorage限制约为5-10MB
        return 5 * 1024 * 1024; // 5MB
    }
}

// 初始化数据管理器
function initializeDataManager() {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.dataManager = new DataManager();
        });
    } else {
        window.dataManager = new DataManager();
    }
}

// 导出给主脚本使用
window.initializeDataManager = initializeDataManager;

// 如果直接加载此脚本，自动初始化
if (typeof window !== 'undefined') {
    initializeDataManager();
}