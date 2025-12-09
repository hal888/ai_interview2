<template>
  <div class="resume-container">
    <h1>简历解析与智能优化</h1>
    
    <!-- 上传加载遮盖层 -->
    <div v-if="isUploading" class="upload-overlay">
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <h3>简历上传中...</h3>
        <p>正在分析您的简历，请稍候</p>
      </div>
    </div>
    
    <div class="resume-upload-section">
      <div class="upload-card">
        <div class="upload-icon"></div>
        <h2>上传您的简历</h2>
        <p>支持 PDF、DOCX、JPG/PNG 格式，单文件 ≤ 10MB</p>
        
        <div class="upload-options">
          <div class="file-input-container">
            <input type="file" id="resume-file" accept=".pdf,.docx,.jpg,.jpeg,.png" @change="handleFileUpload" :disabled="isUploading" />
            <label for="resume-file" class="file-input-label" :class="{ 'disabled': isUploading }">
              <span class="file-icon">📁</span>
              选择文件
            </label>
          </div>
          
          <div class="drag-drop-area" @dragover.prevent @drop.prevent="handleDragDrop" :class="{ 'disabled': isUploading }">
            <span>或拖拽文件到此处</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="resumeData" class="resume-analysis-section">
      <h2>简历分析结果</h2>
      
      <div class="analysis-header">
        <div class="resume-score">
          <h3>简历评分</h3>
          <div class="score-circle">
            <span class="score-value">{{ resumeData.score }}</span>
            <span class="score-max">/100</span>
          </div>
          <p class="score-description">{{ getScoreDescription(resumeData.score) }}</p>
        </div>
      </div>

      <div class="analysis-content">
        <div class="diagnosis-section">
          <h3>智能诊断</h3>
          <div class="diagnosis-list">
            <div v-for="(item, index) in resumeData.diagnosis" :key="index" class="diagnosis-item">
              <div class="diagnosis-type" :class="item.type">{{ item.type }}</div>
              <div class="diagnosis-content">
                <h4>{{ item.title }}</h4>
                <p>{{ item.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="optimization-section">
          <h3>智能优化建议</h3>
          <div class="optimization-tabs">
            <button 
              v-for="tab in optimizationTabs" 
              :key="tab" 
              :class="['tab-btn', { active: activeTab === tab }]" 
              @click="activeTab = tab"
            >
              {{ tab }}
            </button>
          </div>

          <div class="optimization-content">
            <div v-if="activeTab === 'STAR法则重写'" class="star-rewrite">
              <h4>STAR法则优化建议</h4>
              <div v-if="resumeData.starRewrite && resumeData.starRewrite.length > 0" class="star-list">
                <div v-for="(item, index) in resumeData.starRewrite" :key="index" class="star-item optimized">
                  <div class="star-section">
                    <span class="star-label">情境(S)：</span>
                    <span class="star-content">{{ item.situation || '无' }}</span>
                  </div>
                  <div class="star-section">
                    <span class="star-label">任务(T)：</span>
                    <span class="star-content">{{ item.task || '无' }}</span>
                  </div>
                  <div class="star-section">
                    <span class="star-label">行动(A)：</span>
                    <span class="star-content">{{ item.action || '无' }}</span>
                  </div>
                  <div class="star-section">
                    <span class="star-label">结果(R)：</span>
                    <span class="star-content">{{ item.result || '无' }}</span>
                  </div>
                </div>
              </div>
              <div v-else class="star-placeholder">
                <p>暂无STAR法则优化建议</p>
              </div>
            </div>

            <div v-if="activeTab === '关键词注入'" class="keyword-injection">
              <h4>关键词优化建议</h4>
              <div class="keyword-list">
                <div class="keyword-item" v-for="(keyword, index) in resumeData.keywords" :key="index">
                  <span class="keyword">{{ keyword }}</span>
                  <span class="keyword-type">{{ getKeywordType(keyword) }}</span>
                </div>
              </div>
              <p class="keyword-tip">建议在简历中自然融入以上关键词，提升ATS系统匹配度</p>
            </div>
          </div>
        </div>

        <div class="preview-section">
          <h3>优化后简历预览</h3>
          <div class="preview-content">
            <div v-if="resumeData.optimizedResume" class="preview-text">
              <div class="resume-preview" v-html="formattedResume"></div>
            </div>
            <div v-else class="preview-placeholder">
              <span>简历预览区域</span>
            </div>
            <div class="preview-actions">
              <button class="btn primary-btn" @click="downloadResume">下载优化后简历</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { jsPDF } from 'jspdf'
import html2canvas from 'html2canvas'

const resumeData = ref(null)
const activeTab = ref('STAR法则重写')
const optimizationTabs = ['STAR法则重写', '关键词注入']
const isUploading = ref(false)

// 页面加载时自动获取最新的简历优化内容
onMounted(async () => {
  try {
    // 从localStorage获取userId，如果没有则生成一个新的
    let userId = localStorage.getItem('userId')
    if (!userId) {
      userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      localStorage.setItem('userId', userId)
    }
    
    // 调用后端API获取最新的简历数据
    const response = await axios.post('http://127.0.0.1:5000/api/resume/get', {
      userId: userId
    })
    
    // 如果返回了简历数据，填充到页面上
    if (response.data && response.data.optimizedResume) {
      resumeData.value = response.data
      // 保存resumeId到localStorage
      if (response.data.resumeId) {
        localStorage.setItem('resumeId', response.data.resumeId)
      }
    }
  } catch (error) {
    // 如果没有找到数据或其他错误，忽略，等待用户上传新简历
    console.log('获取最新简历失败:', error)
  }
})

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    uploadResume(file)
  }
}

const handleDragDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (file) {
    uploadResume(file)
  }
}

const uploadResume = (file) => {
  isUploading.value = true
  
  // 从localStorage获取userId，如果没有则生成一个新的
  let userId = localStorage.getItem('userId')
  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    localStorage.setItem('userId', userId)
  }
  
  // 创建FormData对象
  const formData = new FormData()
  formData.append('file', file)
  formData.append('userId', userId) // 添加userId到请求中
  
  // 调用后端API
  axios.post('http://127.0.0.1:5000/api/resume/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  .then(response => {
    resumeData.value = response.data
    // 保存resumeId到localStorage
    if (response.data.resumeId) {
      localStorage.setItem('resumeId', response.data.resumeId)
    }
    // 保存userId到localStorage，确保后续请求使用相同的userId
    if (response.data.userId) {
      localStorage.setItem('userId', response.data.userId)
    }
  })
  .catch(error => {
    console.error('简历分析失败:', error)
    alert('简历分析失败，请重试')
  })
  .finally(() => {
    isUploading.value = false
  })
}

const getScoreDescription = (score) => {
  if (score >= 90) return '优秀的简历，具有很强的竞争力'
  if (score >= 80) return '良好的简历，需要一些小的优化'
  if (score >= 70) return '中等的简历，有改进空间'
  if (score >= 60) return '基础的简历，需要较多优化'
  return '较差的简历，建议重新撰写'
}

const getKeywordType = (keyword) => {
  const techKeywords = ['JavaScript', 'Vue', 'React', 'Node.js', 'RESTful API', '数据库设计', '性能优化']
  return techKeywords.includes(keyword) ? '技术关键词' : '软技能关键词'
}

// 格式化简历内容
const formattedResume = computed(() => {
  if (!resumeData.value?.optimizedResume) return ''
  
  let resume = resumeData.value.optimizedResume
  
  // 替换Markdown标题为HTML标题
  resume = resume.replace(/^# (.*$)/gm, '<h1 class="resume-section">$1</h1>')
  resume = resume.replace(/^## (.*$)/gm, '<h2 class="resume-subsection">$1</h2>')
  resume = resume.replace(/^### (.*$)/gm, '<h3 class="resume-item-title">$1</h3>')
  
  // 替换列表项
  resume = resume.replace(/^- (.*$)/gm, '<li class="resume-list-item">$1</li>')
  resume = resume.replace(/(<li class="resume-list-item">.*?)(<\/li>)/gs, '<ul class="resume-list">$1$2</ul>')
  
  // 替换段落
  resume = resume.replace(/^(?!<h|<ul|<li).*$/gm, '<p class="resume-paragraph">$&</p>')
  
  return resume
})

// 下载简历功能 - PDF格式
const downloadResume = async () => {
  if (!resumeData.value?.optimizedResume) return
  
  try {
    // 获取简历预览元素
    const resumeElement = document.querySelector('.resume-preview')
    if (!resumeElement) return
    
    // 使用html2canvas将HTML转换为canvas
    const canvas = await html2canvas(resumeElement, {
      scale: 2, // 提高清晰度
      useCORS: true,
      backgroundColor: '#ffffff',
      logging: false
    })
    
    // 计算PDF尺寸
    const imgData = canvas.toDataURL('image/png')
    const imgWidth = 210 // A4宽度，单位mm
    const imgHeight = (canvas.height * imgWidth) / canvas.width
    
    // 创建PDF
    const doc = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })
    
    let position = 0
    
    // 添加图片到PDF
    doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
    
    // 保存PDF文件
    doc.save('optimized_resume.pdf')
  } catch (error) {
    console.error('生成PDF失败:', error)
    alert('生成PDF失败，请重试')
  }
}


</script>

<style scoped>
.resume-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.resume-container h1 {
  font-size: 2.5rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.resume-upload-section {
  display: flex;
  justify-content: center;
  margin-bottom: 50px;
}

.upload-card {
  background-color: white;
  padding: 60px 40px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 600px;
  width: 100%;
  border: 2px dashed #667eea;
}

.upload-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 20px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23667eea"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>');
  background-size: contain;
  background-repeat: no-repeat;
}

.upload-card h2 {
  font-size: 1.8rem;
  margin-bottom: 10px;
  color: #333;
}

.upload-card p {
  color: #666;
  margin-bottom: 30px;
}

.upload-options {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.file-input-container {
  position: relative;
}

#resume-file {
  display: none;
}

.file-input-label {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  background-color: #667eea;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.file-input-label:hover {
  background-color: #5568d3;
  transform: translateY(-2px);
}

.file-icon {
  font-size: 1.2rem;
}

.drag-drop-area {
  width: 100%;
  padding: 30px;
  border: 2px dashed #ddd;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.drag-drop-area:hover {
  border-color: #667eea;
  background-color: #f0f4ff;
}

.resume-analysis-section {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.resume-analysis-section h2 {
  font-size: 2rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.analysis-header {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}

.resume-score {
  text-align: center;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: conic-gradient(#667eea 0deg 270deg, #e0e0e0 270deg 360deg);
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto 20px;
  position: relative;
}

.score-circle::before {
  content: '';
  position: absolute;
  width: 130px;
  height: 130px;
  border-radius: 50%;
  background-color: white;
}

.score-value {
  font-size: 3rem;
  font-weight: bold;
  color: #667eea;
  position: relative;
  z-index: 1;
}

.score-max {
  font-size: 1.5rem;
  color: #999;
  position: relative;
  z-index: 1;
}

.score-description {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.diagnosis-section h3,
.optimization-section h3,
.preview-section h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid #667eea;
  padding-bottom: 10px;
}

.diagnosis-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.diagnosis-item {
  display: flex;
  gap: 15px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.diagnosis-type {
  font-weight: bold;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  white-space: nowrap;
}

.diagnosis-type.警告 {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
}

.diagnosis-type.错误 {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.diagnosis-type.建议 {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.diagnosis-content h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 1.1rem;
}

.diagnosis-content p {
  margin: 0;
  color: #666;
}

.optimization-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tab-btn {
  padding: 10px 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  border-color: #667eea;
}

.tab-btn.active {
  background-color: #667eea;
  color: white;
  border-color: #667eea;
}

.optimization-content {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.star-rewrite h4,
.keyword-injection h4 {
  margin-top: 0;
  color: #333;
  font-size: 1.2rem;
}

.star-example {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.star-item {
  padding: 15px;
  background-color: white;
  border-radius: 5px;
  border-left: 4px solid #667eea;
}

.star-item.optimized {
  border-left-color: #42b883;
}

.star-item strong {
  color: #333;
}

.star-label {
  font-weight: bold;
  color: #667eea;
}

.keyword-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.keyword-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 15px;
  background-color: white;
  border-radius: 20px;
  border: 1px solid #e0e0e0;
}

.keyword {
  font-weight: bold;
  color: #667eea;
}

.keyword-type {
  font-size: 0.8rem;
  color: #999;
}

.keyword-tip {
  color: #666;
  font-style: italic;
}

.preview-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.preview-placeholder {
  width: 100%;
  height: 400px;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #999;
  border-radius: 5px;
  border: 2px dashed #ddd;
}

.preview-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-start;
}

.btn {
  padding: 12px 25px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.primary-btn {
  background-color: #42b883;
  color: white;
}

.primary-btn:hover {
  background-color: #369f70;
  transform: translateY(-2px);
}

.secondary-btn {
  background-color: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.secondary-btn:hover {
  background-color: #667eea;
  color: white;
  transform: translateY(-2px);
}

/* 上传加载遮盖层样式 */
.upload-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.loading-container {
  text-align: center;
  padding: 40px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 90%;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  margin: 0 auto 20px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.5rem;
}

.loading-container p {
  color: #666;
  margin: 0;
  font-size: 1rem;
}

/* 禁用状态样式 */
.file-input-label.disabled,
.drag-drop-area.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.file-input-label.disabled:hover {
  background-color: #667eea;
  transform: none;
}

.drag-drop-area.disabled:hover {
  border-color: #ddd;
  background-color: transparent;
}

/* 简历预览样式 */
.preview-text {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  max-height: 500px;
  overflow-y: auto;
}

/* 格式化简历样式 */
.resume-preview {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  line-height: 1.8;
  color: #333;
  background-color: #fafafa;
  padding: 30px;
  border-radius: 5px;
  min-height: 400px;
}

.resume-section {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
  margin: 20px 0 15px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #3498db;
  text-align: left;
}

.resume-subsection {
  font-size: 18px;
  font-weight: bold;
  color: #34495e;
  margin: 18px 0 12px 0;
  padding-left: 10px;
  border-left: 4px solid #3498db;
  text-align: left;
}

.resume-item-title {
  font-size: 16px;
  font-weight: bold;
  color: #2c3e50;
  margin: 15px 0 8px 0;
  text-align: left;
}

.resume-paragraph {
  margin: 10px 0;
  text-align: left;
  line-height: 1.8;
}

.resume-list {
  margin: 10px 0 10px 20px;
  padding-left: 20px;
}

.resume-list-item {
  margin: 6px 0;
  list-style-type: disc;
  color: #34495e;
}

.preview-text pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  line-height: 1.6;
  color: #333;
  margin: 0;
}

/* STAR法则重写样式 */
.star-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.star-section {
  margin-bottom: 10px;
  line-height: 1.6;
  display: flex;
  align-items: flex-start;
}

.star-label {
  font-weight: bold;
  color: #667eea;
  width: 80px;
  flex-shrink: 0;
  text-align: right;
  padding-right: 15px;
}

.star-content {
  flex: 1;
  text-align: left;
}

.star-placeholder {
  background-color: white;
  padding: 40px;
  border-radius: 8px;
  text-align: center;
  color: #999;
  border: 1px dashed #e0e0e0;
}

/* 智能诊断样式优化 */
.diagnosis-item {
  display: flex;
  gap: 15px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  align-items: flex-start;
}

.diagnosis-type {
  font-weight: bold;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  white-space: nowrap;
  flex-shrink: 0;
  margin-top: 4px;
}

.diagnosis-content {
  flex: 1;
}

@media (max-width: 768px) {
  .resume-container {
    padding: 10px;
  }
  
  .resume-container h1 {
    font-size: 2rem;
  }
  
  .upload-card {
    padding: 40px 20px;
  }
  
  .resume-analysis-section {
    padding: 20px;
  }
  
  .diagnosis-item {
    flex-direction: column;
    gap: 10px;
  }
  
  .diagnosis-type {
    align-self: flex-start;
  }
  
  .preview-placeholder {
    height: 300px;
  }
  
  .preview-actions {
    flex-direction: column;
  }
  
  .loading-container {
    padding: 30px 20px;
  }
  
  .loading-spinner {
    width: 50px;
    height: 50px;
  }
}
</style>