// API处理函数

class API {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl;
    }
    
    // 提交视频生成请求
    async generateVideo(prompt, style) {
        try {
            const response = await fetch(`${this.baseUrl}/api/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt, style })
            });
            
            if (!response.ok) {
                throw new Error('提交生成请求失败');
            }
            
            return await response.json();
        } catch (error) {
            console.error('API错误:', error);
            throw error;
        }
    }
    
    // 检查生成任务状态
    async checkJobStatus(jobId) {
        try {
            const response = await fetch(`${this.baseUrl}/api/jobs/${jobId}`);
            
            if (!response.ok) {
                throw new Error('检查任务状态失败');
            }
            
            return await response.json();
        } catch (error) {
            console.error('API错误:', error);
            throw error;
        }
    }
}

// 创建全局API实例
const api = new API();
