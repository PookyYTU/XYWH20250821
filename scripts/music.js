// 音乐播放器功能 - 小雨微寒

class MusicPlayer {
    constructor() {
        this.audio = document.getElementById('audioPlayer');
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.progressFill = document.getElementById('progressFill');
        this.musicPlayer = document.getElementById('musicPlayer');
        
        this.isDragging = false;
        this.isPlaying = false;
        this.dragOffset = { x: 0, y: 0 };
        
        this.init();
    }
    
    init() {
        if (!this.audio || !this.playPauseBtn) {
            console.warn('音乐播放器元素未找到');
            return;
        }
        
        this.setupEventListeners();
        this.setupDragAndDrop();
        this.loadPlayerState();
        
        console.log('音乐播放器初始化完成');
    }
    
    setupEventListeners() {
        // 播放/暂停按钮
        this.playPauseBtn.addEventListener('click', () => {
            this.togglePlayPause();
        });
        
        // 音频事件
        this.audio.addEventListener('loadedmetadata', () => {
            this.updateProgress();
        });
        
        this.audio.addEventListener('timeupdate', () => {
            this.updateProgress();
        });
        
        this.audio.addEventListener('ended', () => {
            this.onSongEnd();
        });
        
        this.audio.addEventListener('error', (e) => {
            console.error('音频加载错误:', e);
            this.showPlayerError();
        });
        
        // 进度条点击
        if (this.progressFill && this.progressFill.parentElement) {
            this.progressFill.parentElement.addEventListener('click', (e) => {
                this.seekTo(e);
            });
        }
        
        // 键盘快捷键
        document.addEventListener('keydown', (e) => {
            if (e.target.tagName.toLowerCase() !== 'input' && 
                e.target.tagName.toLowerCase() !== 'textarea') {
                this.handleKeyboard(e);
            }
        });
        
        // 页面可见性变化时暂停/恢复（可选）
        document.addEventListener('visibilitychange', () => {
            if (document.hidden && this.isPlaying) {
                // 页面隐藏时可以选择暂停
                // this.pause();
            }
        });
    }
    
    setupDragAndDrop() {
        if (!this.musicPlayer) return;
        
        // 整个播放器都可以拖拽
        // 鼠标事件
        this.musicPlayer.addEventListener('mousedown', (e) => {
            this.startDrag(e);
        });
        
        document.addEventListener('mousemove', (e) => {
            this.drag(e);
        });
        
        document.addEventListener('mouseup', () => {
            this.endDrag();
        });
        
        // 触摸事件（移动端）
        this.musicPlayer.addEventListener('touchstart', (e) => {
            this.startDrag(e.touches[0]);
        });
        
        document.addEventListener('touchmove', (e) => {
            if (this.isDragging) {
                e.preventDefault();
                this.drag(e.touches[0]);
            }
        });
        
        document.addEventListener('touchend', () => {
            this.endDrag();
        });
    }
    
    startDrag(e) {
        this.isDragging = true;
        const rect = this.musicPlayer.getBoundingClientRect();
        this.dragOffset.x = e.clientX - rect.left;
        this.dragOffset.y = e.clientY - rect.top;
        
        this.musicPlayer.style.transition = 'none';
        this.musicPlayer.style.cursor = 'grabbing';
        
        // 防止文本选择
        document.body.style.userSelect = 'none';
    }
    
    drag(e) {
        if (!this.isDragging) return;
        
        const x = e.clientX - this.dragOffset.x;
        const y = e.clientY - this.dragOffset.y;
        
        // 限制在视窗内
        const maxX = window.innerWidth - this.musicPlayer.offsetWidth;
        const maxY = window.innerHeight - this.musicPlayer.offsetHeight;
        
        const constrainedX = Math.max(0, Math.min(x, maxX));
        const constrainedY = Math.max(0, Math.min(y, maxY));
        
        this.musicPlayer.style.left = constrainedX + 'px';
        this.musicPlayer.style.top = constrainedY + 'px';
        this.musicPlayer.style.right = 'auto';
        this.musicPlayer.style.bottom = 'auto';
    }
    
    endDrag() {
        if (!this.isDragging) return;
        
        this.isDragging = false;
        this.musicPlayer.style.transition = '';
        this.musicPlayer.style.cursor = '';
        document.body.style.userSelect = '';
        
        // 保存位置
        this.savePlayerPosition();
    }
    
    togglePlayPause() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }
    
    play() {
        const playPromise = this.audio.play();
        
        if (playPromise !== undefined) {
            playPromise
                .then(() => {
                    this.isPlaying = true;
                    this.updatePlayButton();
                    this.savePlayerState();
                })
                .catch((error) => {
                    console.error('播放失败:', error);
                    this.showPlayerError('播放失败，请检查音频文件');
                });
        }
    }
    
    pause() {
        this.audio.pause();
        this.isPlaying = false;
        this.updatePlayButton();
        this.savePlayerState();
    }
    
    setVolume(volume) {
        this.audio.volume = Math.max(0, Math.min(1, volume));
        this.savePlayerState();
    }
    
    seekTo(e) {
        if (!this.audio.duration) return;
        
        const progressBar = e.currentTarget;
        const rect = progressBar.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        const seekTime = percent * this.audio.duration;
        
        this.audio.currentTime = seekTime;
    }
    
    updateProgress() {
        if (!this.audio.duration || !this.progressFill) return;
        
        const percent = (this.audio.currentTime / this.audio.duration) * 100;
        this.progressFill.style.width = percent + '%';
    }
    
    updatePlayButton() {
        if (!this.playPauseBtn) return;
        
        const icon = this.playPauseBtn.querySelector('i');
        if (icon) {
            icon.className = this.isPlaying ? 'fas fa-pause' : 'fas fa-play';
        }
    }
    
    onSongEnd() {
        this.isPlaying = false;
        this.updatePlayButton();
        
        // 重置进度条
        if (this.progressFill) {
            this.progressFill.style.width = '0%';
        }
        
        // 重置播放位置
        this.audio.currentTime = 0;
        
        this.savePlayerState();
    }
    
    handleKeyboard(e) {
        switch(e.code) {
            case 'Space':
                e.preventDefault();
                this.togglePlayPause();
                break;
            case 'ArrowUp':
                e.preventDefault();
                this.adjustVolume(0.1);
                break;
            case 'ArrowDown':
                e.preventDefault();
                this.adjustVolume(-0.1);
                break;
            case 'ArrowLeft':
                e.preventDefault();
                this.seekRelative(-10);
                break;
            case 'ArrowRight':
                e.preventDefault();
                this.seekRelative(10);
                break;
        }
    }
    
    adjustVolume(delta) {
        const newVolume = Math.max(0, Math.min(1, this.audio.volume + delta));
        this.setVolume(newVolume);
    }
    
    seekRelative(seconds) {
        if (!this.audio.duration) return;
        
        const newTime = Math.max(0, Math.min(this.audio.duration, this.audio.currentTime + seconds));
        this.audio.currentTime = newTime;
    }
    
    showPlayerError(message = '音频播放出错') {
        // 创建错误提示
        const errorMsg = document.createElement('div');
        errorMsg.className = 'message error';
        errorMsg.textContent = message;
        document.body.appendChild(errorMsg);
        
        setTimeout(() => {
            if (errorMsg.parentNode) {
                errorMsg.remove();
            }
        }, 3000);
        
        // 禁用播放按钮
        if (this.playPauseBtn) {
            this.playPauseBtn.disabled = true;
            setTimeout(() => {
                this.playPauseBtn.disabled = false;
            }, 2000);
        }
    }
    
    savePlayerState() {
        const state = {
            volume: this.audio.volume,
            isPlaying: this.isPlaying,
            currentTime: this.audio.currentTime
        };
        localStorage.setItem('musicPlayerState', JSON.stringify(state));
    }
    
    loadPlayerState() {
        const savedState = localStorage.getItem('musicPlayerState');
        if (savedState) {
            try {
                const state = JSON.parse(savedState);
                
                // 恢复音量
                if (typeof state.volume === 'number') {
                    this.setVolume(state.volume);
                }
                
                // 恢复播放位置（可选）
                if (typeof state.currentTime === 'number' && state.currentTime > 0) {
                    this.audio.addEventListener('loadedmetadata', () => {
                        this.audio.currentTime = Math.min(state.currentTime, this.audio.duration);
                    }, { once: true });
                }
                
            } catch (e) {
                console.warn('加载播放器状态失败:', e);
            }
        }
        
        // 设置默认音量
        if (!savedState) {
            this.setVolume(0.5);
        }
    }
    
    savePlayerPosition() {
        const rect = this.musicPlayer.getBoundingClientRect();
        const position = {
            left: rect.left,
            top: rect.top
        };
        localStorage.setItem('musicPlayerPosition', JSON.stringify(position));
    }
    
    loadPlayerPosition() {
        const savedPosition = localStorage.getItem('musicPlayerPosition');
        if (savedPosition) {
            try {
                const position = JSON.parse(savedPosition);
                
                // 检查位置是否在视窗内
                const maxX = window.innerWidth - this.musicPlayer.offsetWidth;
                const maxY = window.innerHeight - this.musicPlayer.offsetHeight;
                
                if (position.left >= 0 && position.left <= maxX &&
                    position.top >= 0 && position.top <= maxY) {
                    
                    this.musicPlayer.style.left = position.left + 'px';
                    this.musicPlayer.style.top = position.top + 'px';
                    this.musicPlayer.style.right = 'auto';
                    this.musicPlayer.style.bottom = 'auto';
                }
            } catch (e) {
                console.warn('加载播放器位置失败:', e);
            }
        }
    }
    
    // 公共方法
    getCurrentTime() {
        return this.audio.currentTime;
    }
    
    getDuration() {
        return this.audio.duration;
    }
    
    getVolume() {
        return this.audio.volume;
    }
    
    isPlayerPlaying() {
        return this.isPlaying;
    }
}

// 初始化音乐播放器
function initializeMusicPlayer() {
    // 等待DOM加载完成
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.musicPlayer = new MusicPlayer();
        });
    } else {
        window.musicPlayer = new MusicPlayer();
    }
}

// 导出给主脚本使用
window.initializeMusicPlayer = initializeMusicPlayer;

// 如果直接加载此脚本，自动初始化
if (typeof window !== 'undefined') {
    initializeMusicPlayer();
}