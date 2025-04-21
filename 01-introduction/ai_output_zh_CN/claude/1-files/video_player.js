// 视频播放器管理

class VideoPlayer {
    constructor(videoElementId) {
        this.videoElement = document.getElementById(videoElementId);
        this.downloadButton = document.getElementById('download-btn');
        this.setupEventListeners();
    }
    
    // 加载视频到播放器
    loadVideo(videoUrl) {
        this.videoElement.src = videoUrl;
        this.videoElement.load();
        this.videoUrl = videoUrl;
    }
    
    // 设置事件监听器
    setupEventListeners() {
        if (this.downloadButton) {
            this.downloadButton.addEventListener('click', () => this.downloadVideo());
        }
    }
    
    // 处理视频下载
    downloadVideo() {
        if (!this.videoUrl) return;
        
        // 创建临时锚元素
        const a = document.createElement('a');
        a.href = this.videoUrl;
        a.download = 'generated-video.mp4';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
}

// 当DOM加载完成时初始化视频播放器
document.addEventListener('DOMContentLoaded', () => {
    window.videoPlayer = new VideoPlayer('video-player');
});
