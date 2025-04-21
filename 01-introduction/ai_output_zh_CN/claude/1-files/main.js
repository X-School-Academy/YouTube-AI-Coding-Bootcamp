// 主应用逻辑

class VideoGeneratorApp {
    constructor() {
        // 元素
        this.form = document.getElementById('generator-form');
        this.promptInput = document.getElementById('prompt');
        this.styleSelect = document.getElementById('style');
        this.generateBtn = document.getElementById('generate-btn');
        this.progressSection = document.getElementById('progress-section');
        this.progressBar = document.getElementById('progress-bar');
        this.progressMessage = document.getElementById('progress-message');
        this.videoSection = document.getElementById('video-section');
        this.newVideoBtn = document.getElementById('new-video-btn');
        
        // 状态
        this.currentJobId = null;
        this.pollInterval = null;
        
        // 初始化
        this.setupEventListeners();
    }
    
    // 设置事件监听器
    setupEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        
        if (this.newVideoBtn) {
            this.newVideoBtn.addEventListener('click', () => this.resetApp());
        }
    }
    
    // 处理表单提交
    async handleFormSubmit(event) {
        event.preventDefault();
        
        const prompt = this.promptInput.value.trim();
        const style = this.styleSelect.value;
        
        if (!prompt) {
            alert('请在生成视频之前输入提示词。');
            return;
        }
        
        try {
            // 禁用表单并显示进度
            this.setFormEnabled(false);
            this.showProgressSection();
            
            // 提交生成请求
            const response = await api.generateVideo(prompt, style);
            this.currentJobId = response.job_id;
            
            // 开始轮询任务状态
            this.startStatusPolling();
        } catch (error) {
            console.error('启动生成时出错:', error);
            alert('视频生成启动失败。请重试。');
            this.setFormEnabled(true);
            this.hideProgressSection();
        }
    }
    
    // 轮询任务状态
    startStatusPolling() {
        if (this.pollInterval) {
            clearInterval(this.pollInterval);
        }
        
        this.pollInterval = setInterval(async () => {
            try {
                const status = await api.checkJobStatus(this.currentJobId);
                this.updateProgress(status);
                
                if (['completed', 'failed'].includes(status.status)) {
                    clearInterval(this.pollInterval);
                    
                    if (status.status === 'completed') {
                        this.showVideo(status.video_url);
                    } else {
                        alert(`生成失败: ${status.message}`);
                        this.resetApp();
                    }
                }
            } catch (error) {
                console.error('检查状态时出错:', error);
                clearInterval(this.pollInterval);
                alert('检查生成状态失败。请重试。');
                this.resetApp();
            }
        }, 2000);
    }
    
    // 更新进度条和消息
    updateProgress(status) {
        this.progressBar.style.width = `${status.progress}%`;
        this.progressMessage.textContent = status.message;
    }
    
    // 显示生成的视频
    showVideo(videoUrl) {
        window.videoPlayer.loadVideo(videoUrl);
        this.hideProgressSection();
        this.showVideoSection();
    }
    
    // 将应用重置为初始状态
    resetApp() {
        // 清除表单
        this.form.reset();
        
        // 重置UI状态
        this.setFormEnabled(true);
        this.hideProgressSection();
        this.hideVideoSection();
        
        // 清除状态
        this.currentJobId = null;
        if (this.pollInterval) {
            clearInterval(this.pollInterval);
            this.pollInterval = null;
        }
    }
    
    // UI辅助方法
    setFormEnabled(enabled) {
        this.promptInput.disabled = !enabled;
        this.styleSelect.disabled = !enabled;
        this.generateBtn.disabled = !enabled;
    }
    
    showProgressSection() {
        this.progressSection.style.display = 'block';
        this.progressBar.style.width = '0%';
        this.progressMessage.textContent = '开始生成...';
    }
    
    hideProgressSection() {
        this.progressSection.style.display = 'none';
    }
    
    showVideoSection() {
        this.videoSection.style.display = 'block';
    }
    
    hideVideoSection() {
        this.videoSection.style.display = 'none';
    }
}

// 当DOM加载完成时初始化应用
document.addEventListener('DOMContentLoaded', () => {
    window.app = new VideoGeneratorApp();
});
