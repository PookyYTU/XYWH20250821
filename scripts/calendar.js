// 日历组件功能 - 小雨微寒

class Calendar {
    constructor() {
        this.calendar = document.getElementById('calendar');
        this.calendarTitle = document.getElementById('calendarTitle');
        this.prevMonthBtn = document.getElementById('prevMonth');
        this.nextMonthBtn = document.getElementById('nextMonth');
        
        this.currentDate = new Date();
        this.currentMonth = this.currentDate.getMonth();
        this.currentYear = this.currentDate.getFullYear();
        
        // 特殊日期
        this.loveStartDate = new Date('2024-04-05');
        this.birthdayDate = new Date('2000-07-08');
        
        // 月份名称
        this.monthNames = [
            '一月', '二月', '三月', '四月', '五月', '六月',
            '七月', '八月', '九月', '十月', '十一月', '十二月'
        ];
        
        // 星期名称
        this.weekdays = ['日', '一', '二', '三', '四', '五', '六'];
        
        this.init();
    }
    
    init() {
        if (!this.calendar || !this.calendarTitle) {
            console.warn('日历元素未找到');
            return;
        }
        
        this.setupEventListeners();
        this.render();
        
        console.log('日历组件初始化完成');
    }
    
    setupEventListeners() {
        if (this.prevMonthBtn) {
            this.prevMonthBtn.addEventListener('click', () => {
                this.previousMonth();
            });
        }
        
        if (this.nextMonthBtn) {
            this.nextMonthBtn.addEventListener('click', () => {
                this.nextMonth();
            });
        }
    }
    
    previousMonth() {
        this.currentMonth--;
        if (this.currentMonth < 0) {
            this.currentMonth = 11;
            this.currentYear--;
        }
        this.render();
    }
    
    nextMonth() {
        this.currentMonth++;
        if (this.currentMonth > 11) {
            this.currentMonth = 0;
            this.currentYear++;
        }
        this.render();
    }
    
    render() {
        this.updateTitle();
        this.renderCalendar();
    }
    
    updateTitle() {
        if (this.calendarTitle) {
            this.calendarTitle.textContent = `${this.currentYear}年${this.monthNames[this.currentMonth]}`;
        }
    }
    
    renderCalendar() {
        if (!this.calendar) return;
        
        this.calendar.innerHTML = '';
        
        // 添加星期标题
        this.renderWeekdays();
        
        // 获取当月第一天和最后一天
        const firstDay = new Date(this.currentYear, this.currentMonth, 1);
        const lastDay = new Date(this.currentYear, this.currentMonth + 1, 0);
        
        // 计算需要显示的日期范围
        const startDate = new Date(firstDay);
        startDate.setDate(startDate.getDate() - firstDay.getDay());
        
        const endDate = new Date(lastDay);
        endDate.setDate(endDate.getDate() + (6 - lastDay.getDay()));
        
        // 渲染日期
        const currentDate = new Date(startDate);
        while (currentDate <= endDate) {
            this.renderDay(new Date(currentDate));
            currentDate.setDate(currentDate.getDate() + 1);
        }
    }
    
    renderWeekdays() {
        this.weekdays.forEach(weekday => {
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-weekday';
            dayElement.textContent = weekday;
            this.calendar.appendChild(dayElement);
        });
    }
    
    renderDay(date) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        
        const isCurrentMonth = date.getMonth() === this.currentMonth;
        const isToday = this.isToday(date);
        const isMarked = this.isMarkedDate(date);
        const hasNote = this.hasNote(date);
        
        // 设置样式类
        if (!isCurrentMonth) {
            dayElement.classList.add('other-month');
        }
        if (isToday) {
            dayElement.classList.add('today');
        }
        if (isMarked) {
            dayElement.classList.add('marked');
        }
        if (hasNote) {
            dayElement.classList.add('has-note');
        }
        
        dayElement.textContent = date.getDate();
        
        // 添加点击事件
        dayElement.addEventListener('click', () => {
            this.onDayClick(date);
        });
        
        // 添加工具提示
        const tooltip = this.getTooltip(date);
        if (tooltip) {
            dayElement.setAttribute('title', tooltip);
            dayElement.classList.add('tooltip');
            dayElement.setAttribute('data-tooltip', tooltip);
        }
        
        this.calendar.appendChild(dayElement);
    }
    
    isToday(date) {
        const today = new Date();
        return date.toDateString() === today.toDateString();
    }
    
    isMarkedDate(date) {
        // 检查是否在恋爱开始日期之后
        if (date < this.loveStartDate) {
            return false;
        }
        
        // 检查是否不是未来日期
        const today = new Date();
        today.setHours(23, 59, 59, 999); // 设置为今天的最后一刻
        
        return date <= today;
    }
    
    hasNote(date) {
        const dateString = this.formatDate(date);
        const notes = JSON.parse(localStorage.getItem('calendarNotes')) || {};
        return notes[dateString] && notes[dateString].trim().length > 0;
    }
    
    getTooltip(date) {
        const tooltips = [];
        
        // 检查是否是特殊日期
        if (this.isSameDate(date, this.loveStartDate)) {
            tooltips.push('💕 我们在一起的日子');
        }
        
        if (this.isSameDate(date, new Date(date.getFullYear(), this.birthdayDate.getMonth(), this.birthdayDate.getDate()))) {
            tooltips.push('🎂 生日');
        }
        
        // 检查是否有备注
        const dateString = this.formatDate(date);
        const notes = JSON.parse(localStorage.getItem('calendarNotes')) || {};
        if (notes[dateString]) {
            tooltips.push(`📝 ${notes[dateString].substring(0, 20)}${notes[dateString].length > 20 ? '...' : ''}`);
        }
        
        // 检查是否是标记日期
        if (this.isMarkedDate(date)) {
            tooltips.push('💗 一起度过的日子');
        }
        
        return tooltips.join('\n');
    }
    
    isSameDate(date1, date2) {
        return date1.getFullYear() === date2.getFullYear() &&
               date1.getMonth() === date2.getMonth() &&
               date1.getDate() === date2.getDate();
    }
    
    onDayClick(date) {
        const dateString = this.formatDate(date);
        
        // 打开备注模态框
        if (window.openNoteModal) {
            window.openNoteModal(dateString);
        } else {
            // 备用方案：使用prompt
            const notes = JSON.parse(localStorage.getItem('calendarNotes')) || {};
            const currentNote = notes[dateString] || '';
            
            const newNote = prompt(
                `为 ${this.formatDisplayDate(date)} 添加备注：`,
                currentNote
            );
            
            if (newNote !== null) {
                if (newNote.trim()) {
                    notes[dateString] = newNote.trim();
                } else {
                    delete notes[dateString];
                }
                
                localStorage.setItem('calendarNotes', JSON.stringify(notes));
                this.render(); // 重新渲染日历
                
                if (window.showMessage) {
                    window.showMessage('备注保存成功！', 'success');
                }
            }
        }
    }
    
    formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
    
    formatDisplayDate(date) {
        const year = date.getFullYear();
        const month = this.monthNames[date.getMonth()];
        const day = date.getDate();
        return `${year}年${month}${day}日`;
    }
    
    // 公共方法
    goToDate(date) {
        this.currentYear = date.getFullYear();
        this.currentMonth = date.getMonth();
        this.render();
    }
    
    goToToday() {
        const today = new Date();
        this.goToDate(today);
    }
    
    updateCalendarDisplay() {
        // 重新渲染日历以更新备注显示
        this.render();
    }
    
    // 获取统计信息
    getStats() {
        const notes = JSON.parse(localStorage.getItem('calendarNotes')) || {};
        const today = new Date();
        const totalDays = Math.floor((today - this.loveStartDate) / (1000 * 60 * 60 * 24));
        
        return {
            totalDays: totalDays,
            notesCount: Object.keys(notes).length,
            loveStartDate: this.loveStartDate,
            birthdayDate: this.birthdayDate
        };
    }
    
    // 导出备注数据
    exportNotes() {
        const notes = JSON.parse(localStorage.getItem('calendarNotes')) || {};
        const exportData = {
            exportDate: new Date().toISOString(),
            loveStartDate: this.loveStartDate.toISOString(),
            birthdayDate: this.birthdayDate.toISOString(),
            notes: notes
        };
        
        const dataStr = JSON.stringify(exportData, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `calendar-notes-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        if (window.showMessage) {
            window.showMessage('备注数据导出成功！', 'success');
        }
    }
    
    // 导入备注数据
    importNotes(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const importData = JSON.parse(e.target.result);
                
                if (importData.notes && typeof importData.notes === 'object') {
                    localStorage.setItem('calendarNotes', JSON.stringify(importData.notes));
                    this.render();
                    
                    if (window.showMessage) {
                        window.showMessage('备注数据导入成功！', 'success');
                    }
                } else {
                    throw new Error('无效的数据格式');
                }
            } catch (error) {
                console.error('导入失败:', error);
                if (window.showMessage) {
                    window.showMessage('导入失败，请检查文件格式', 'error');
                }
            }
        };
        reader.readAsText(file);
    }
}

// 初始化日历
function initializeCalendar() {
    // 等待DOM加载完成
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.calendar = new Calendar();
        });
    } else {
        window.calendar = new Calendar();
    }
}

// 更新日历显示（供外部调用）
function updateCalendarDisplay() {
    if (window.calendar) {
        window.calendar.updateCalendarDisplay();
    }
}

// 导出给主脚本使用
window.initializeCalendar = initializeCalendar;
window.updateCalendarDisplay = updateCalendarDisplay;

// 如果直接加载此脚本，自动初始化
if (typeof window !== 'undefined') {
    initializeCalendar();
}