<template>
  <div class="question-bank-container">
    <h1>智能题库与定向突击</h1>
    
    <!-- 生成题库遮盖层 -->
    <div v-if="isGenerating" class="generate-overlay">
      <div class="generate-loading">
        <div class="loading-spinner"></div>
        <h3>题库生成中...</h3>
        <p>正在基于您的简历内容生成个性化面试问题，请稍候</p>
      </div>
    </div>
    
    <div class="question-config-section">
      <div class="config-card">
        <h2>配置题库</h2>
        
        <div class="config-options">
          <div class="option-group">
            <label>题目数量</label>
            <div class="option-buttons">
              <button 
                v-for="count in questionCounts" 
                :key="count" 
                :class="['option-btn', { active: selectedCount === count }]" 
                @click="selectedCount = count"
              >
                {{ count }}题
              </button>
            </div>
            <p class="option-desc">{{ getCountDescription(selectedCount) }}</p>
          </div>

          <div class="option-group">
            <label>题型分布</label>
            <div class="question-types">
              <div class="type-item">
                <span class="type-label">高频必问题</span>
                <span class="type-percentage">30%</span>
              </div>
              <div class="type-item">
                <span class="type-label">简历深挖题</span>
                <span class="type-percentage">25%</span>
              </div>
              <div class="type-item">
                <span class="type-label">专业技能题</span>
                <span class="type-percentage">25%</span>
              </div>
              <div class="type-item">
                <span class="type-label">行为/情景题</span>
                <span class="type-percentage">20%</span>
              </div>
            </div>
          </div>

          <div class="option-group">
            <label>自定义话题（可选）</label>
            <input 
              type="text" 
              v-model="customTopic" 
              placeholder="输入特定话题，如'Spring Cloud'、'危机公关'"
              :disabled="isGenerating"
            />
            <p class="option-desc">系统将结合您的简历背景和指定话题生成相关问题</p>
          </div>

          <button 
            class="generate-btn" 
            @click="generateQuestions"
            :disabled="isGenerating"
          >
            <span class="btn-icon">🎯</span>
            {{ isGenerating ? '生成中...' : '生成题库' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="questions.length > 0" class="questions-section">
      <h2>智能题库</h2>
      
      <div class="questions-header">
        <div class="questions-info">
          <span class="total-count">{{ questions.length }}题</span>
          <span class="topic-tag" v-if="customTopic">话题：{{ customTopic }}</span>
        </div>
        <div class="questions-actions">
          <button class="action-btn" @click="exportQuestions">
            <span class="action-icon">📥</span>
            导出题库
          </button>
        </div>
      </div>

      <div class="questions-list">
        <div 
          v-for="(question, index) in questions" 
          :key="index" 
          class="question-item"
        >
          <div class="question-header">
            <div class="question-number">{{ index + 1 }}</div>
            <div class="question-type-badge">{{ question.type }}</div>
            <button class="tts-btn" @click="toggleTTS(index)">
              <span class="tts-icon">{{ question.isPlaying ? '⏸️' : '🔊' }}</span>
            </button>
          </div>
          <div class="question-content">
            {{ question.content }}
          </div>
          <div class="question-footer">
            <button class="expand-btn" @click="toggleAnswer(index)">
              <span class="expand-icon">{{ question.showAnswer ? '▼' : '▶️' }}</span>
              {{ question.showAnswer ? '收起答案' : '查看参考答案' }}
            </button>
          </div>
          
          <div v-if="question.showAnswer" class="answer-section">
            <div class="answer-header">
              <h4>参考答案</h4>
            </div>
            <div class="answer-content">
              {{ question.answer }}
            </div>
            <div class="answer-analysis">
              <h5>面试官意图</h5>
              <p>{{ question.analysis }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

const router = useRouter()


const selectedCount = ref(10)
const customTopic = ref('')
const questions = ref([])
const isGenerating = ref(false)

// 页面加载时自动获取已生成的题库数据
onMounted(async () => {
  try {
    // 从localStorage获取userId
    const userId = localStorage.getItem('userId')
    
    // 如果没有userId，不自动加载数据（等待用户第一次生成）
    if (!userId) return
    
    // 调用后端API获取已生成的题库数据
    await fetchQuestionBank()
  } catch (error) {
    console.log('获取已生成题库失败:', error)
    // 忽略错误，等待用户手动生成
  }
})

// 根据选择的数量获取题库数据
const fetchQuestionBank = async () => {
  try {
    // 从localStorage获取userId
    const userId = localStorage.getItem('userId')
    
    // 如果没有userId，不获取数据
    if (!userId) return
    
    // 调用后端API获取已生成的题库数据，不传递resumeId参数
    const response = await axios.post('http://127.0.0.1:5000/api/question-bank/get', {
      userId: userId,
      count: selectedCount.value  // 传递选择的题目数量
    })
    
    // 如果返回了题库数据，填充到页面上
    if (response.data && response.data.questions && response.data.questions.length > 0) {
      questions.value = response.data.questions.map(q => ({
        ...q,
        showAnswer: false,
        isPlaying: false
      }))
    } else {
      // 如果没有找到数据，清空当前显示
      questions.value = []
    }
  } catch (error) {
    console.log('获取已生成题库失败:', error)
    // 检查是否是用户不存在的错误
    if (error.response && error.response.data && error.response.data.error === 'User not found') {
      alert('请先上传简历进行优化，然后再生成题库')
      router.push('/resume')
    }
    // 其他错误忽略，等待用户手动生成
  }
}

const questionCounts = [10, 30, 50, 100]

const getCountDescription = (count) => {
  if (count === 10) return '极简模式，适合快速体验或重点突破'
  if (count === 30) return '快速模式，适合时间紧张的用户'
  if (count === 50) return '标准模式，平衡深度和广度'
  if (count === 100) return '压测模式，全面覆盖所有可能问题'
  return ''
}

// 监听题目数量变化，自动获取相应数量的题目
watch(selectedCount, () => {
  fetchQuestionBank()
})

const generateQuestions = () => {
  isGenerating.value = true
  
  // 从localStorage获取userId，如果没有则生成一个新的
  let userId = localStorage.getItem('userId')
  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    localStorage.setItem('userId', userId)
  }
  
  console.log('topic:', customTopic.value)
  console.log('userId:', userId)
  
  // 调用后端API，不传递resumeId参数
  axios.post('http://127.0.0.1:5000/api/question-bank/generate', {
    count: selectedCount.value,
    topic: customTopic.value,
    userId: userId
  })
  .then(response => {
    // 格式化问题数据，添加showAnswer和isPlaying字段
    questions.value = response.data.questions.map(q => ({
      ...q,
      showAnswer: false,
      isPlaying: false
    }))
    // 保存userId到localStorage，确保后续请求使用相同的userId
    if (response.data.userId) {
      localStorage.setItem('userId', response.data.userId)
    }
    // 保存resumeId到localStorage（如果后端返回了新的resumeId）
    if (response.data.resumeId) {
      localStorage.setItem('resumeId', response.data.resumeId)
    }
  })
  .catch(error => {
    console.error('生成题库失败:', error)
    alert('生成题库失败，请重试')
  })
  .finally(() => {
    isGenerating.value = false
  })
}

const toggleAnswer = (index) => {
  questions.value[index].showAnswer = !questions.value[index].showAnswer
}

const toggleTTS = (index) => {
  questions.value[index].isPlaying = !questions.value[index].isPlaying
  // 这里可以添加实际的TTS逻辑
}

const exportQuestions = async () => {
  if (questions.value.length === 0) {
    alert('请先生成题库')
    return
  }

  try {
    // 创建PDF文档
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })

    // 定义页面配置
    const pageWidth = 210 // A4宽度，单位mm
    const pageHeight = 297 // A4高度，单位mm
    const margin = 15 // 页边距，单位mm
    const contentWidth = pageWidth - 2 * margin // 内容宽度
    const contentHeight = pageHeight - 2 * margin // 内容高度
    let currentPage = 1

    // 定义每页面显示的题目数量
    const questionsPerPage = 2
    let currentY = margin // 当前Y坐标

    // 创建一个临时容器来渲染单页内容
    const tempContainer = document.createElement('div')
    tempContainer.style.position = 'absolute'
    tempContainer.style.top = '-9999px'
    tempContainer.style.left = '-9999px'
    tempContainer.style.width = `${pageWidth}mm`
    tempContainer.style.padding = `${margin}mm`
    tempContainer.style.backgroundColor = '#ffffff'
    tempContainer.style.fontFamily = 'SimSun, Songti SC, serif'
    tempContainer.style.fontSize = '12px'
    tempContainer.style.lineHeight = '1.6'
    tempContainer.style.color = '#333333'
    tempContainer.style.boxSizing = 'border-box'
    document.body.appendChild(tempContainer)

    // 生成首页标题和信息
    const renderTitlePage = () => {
      tempContainer.innerHTML = ''
      
      // 生成标题
      const title = document.createElement('h1')
      title.textContent = '智能面试题库'
      title.style.textAlign = 'center'
      title.style.marginBottom = '20px'
      title.style.fontSize = '24px'
      title.style.color = '#2c3e50'
      tempContainer.appendChild(title)

      // 生成话题信息
      if (customTopic.value) {
        const topicInfo = document.createElement('div')
        topicInfo.textContent = `话题：${customTopic.value}`
        topicInfo.style.textAlign = 'center'
        topicInfo.style.marginBottom = '20px'
        topicInfo.style.color = '#666666'
        tempContainer.appendChild(topicInfo)
      }

      // 生成统计信息
      const stats = document.createElement('div')
      stats.textContent = `共 ${questions.value.length} 道题目`
      stats.style.textAlign = 'center'
      stats.style.marginBottom = '30px'
      stats.style.color = '#666666'
      tempContainer.appendChild(stats)

      // 生成说明文字
      const instructions = document.createElement('div')
      instructions.textContent = '本题库基于您的简历内容生成，涵盖高频必问题、简历深挖题、专业技能题和行为/情景题等类型，可用于面试前的针对性练习。'
      instructions.style.textAlign = 'center'
      instructions.style.color = '#666666'
      instructions.style.marginTop = '50px'
      tempContainer.appendChild(instructions)
    }

    // 渲染单页题目内容
    const renderQuestionsPage = (startIndex, endIndex) => {
      tempContainer.innerHTML = ''
      
      // 生成页码
      const pageNumber = document.createElement('div')
      pageNumber.textContent = `第 ${currentPage} 页`
      pageNumber.style.textAlign = 'right'
      pageNumber.style.marginBottom = '10px'
      pageNumber.style.fontSize = '10px'
      pageNumber.style.color = '#666666'
      tempContainer.appendChild(pageNumber)
      
      // 生成题目列表
      for (let i = startIndex; i < endIndex && i < questions.value.length; i++) {
        const question = questions.value[i]
        const questionBlock = document.createElement('div')
        questionBlock.style.marginBottom = '25px'
        questionBlock.style.borderBottom = '1px solid #e0e0e0'
        questionBlock.style.paddingBottom = '15px'

        // 题号和类型
        const questionHeader = document.createElement('div')
        questionHeader.style.display = 'flex'
        questionHeader.style.justifyContent = 'space-between'
        questionHeader.style.alignItems = 'center'
        questionHeader.style.marginBottom = '10px'

        const questionNumber = document.createElement('span')
        questionNumber.textContent = `${i + 1}.`
        questionNumber.style.fontWeight = 'bold'
        questionNumber.style.fontSize = '14px'
        questionHeader.appendChild(questionNumber)

        const questionType = document.createElement('span')
        questionType.textContent = question.type
        questionType.style.backgroundColor = '#f0f4ff'
        questionType.style.color = '#667eea'
        questionType.style.padding = '3px 10px'
        questionType.style.borderRadius = '12px'
        questionType.style.fontSize = '11px'
        questionType.style.fontWeight = 'bold'
        questionHeader.appendChild(questionType)

        questionBlock.appendChild(questionHeader)

        // 问题内容
        const questionContent = document.createElement('div')
        questionContent.textContent = question.content
        questionContent.style.marginBottom = '12px'
        questionContent.style.fontSize = '13px'
        questionBlock.appendChild(questionContent)

        // 参考答案
        const answerSection = document.createElement('div')
        answerSection.style.marginBottom = '8px'

        const answerLabel = document.createElement('div')
        answerLabel.textContent = '参考答案：'
        answerLabel.style.fontWeight = 'bold'
        answerLabel.style.marginBottom = '4px'
        answerLabel.style.fontSize = '12px'
        answerSection.appendChild(answerLabel)

        const answerContent = document.createElement('div')
        answerContent.textContent = question.answer
        answerContent.style.marginLeft = '10px'
        answerContent.style.color = '#555555'
        answerContent.style.fontSize = '11px'
        answerSection.appendChild(answerContent)

        questionBlock.appendChild(answerSection)

        // 面试官意图
        const analysisSection = document.createElement('div')

        const analysisLabel = document.createElement('div')
        analysisLabel.textContent = '面试官意图：'
        analysisLabel.style.fontWeight = 'bold'
        analysisLabel.style.marginBottom = '4px'
        analysisLabel.style.fontSize = '12px'
        analysisSection.appendChild(analysisLabel)

        const analysisContent = document.createElement('div')
        analysisContent.textContent = question.analysis
        analysisContent.style.marginLeft = '10px'
        analysisContent.style.color = '#555555'
        analysisContent.style.fontSize = '11px'
        analysisSection.appendChild(analysisContent)

        questionBlock.appendChild(analysisSection)

        tempContainer.appendChild(questionBlock)
      }
    }

    // 渲染首页
    renderTitlePage()
    
    // 将首页转换为canvas并添加到PDF
    const titleCanvas = await html2canvas(tempContainer, {
      scale: 2,
      useCORS: true,
      backgroundColor: '#ffffff',
      logging: false
    })
    const titleImgData = titleCanvas.toDataURL('image/png')
    pdf.addImage(titleImgData, 'PNG', 0, 0, pageWidth, pageHeight)
    currentPage++

    // 分页渲染题目
    for (let i = 0; i < questions.value.length; i += questionsPerPage) {
      // 添加新页面（除了首页）
      if (i > 0) {
        pdf.addPage()
      }
      
      // 渲染当前页题目
      renderQuestionsPage(i, i + questionsPerPage)
      
      // 将当前页转换为canvas并添加到PDF
      const pageCanvas = await html2canvas(tempContainer, {
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false
      })
      const pageImgData = pageCanvas.toDataURL('image/png')
      pdf.addImage(pageImgData, 'PNG', 0, 0, pageWidth, pageHeight)
      currentPage++
    }

    // 保存PDF文件
    pdf.save('智能面试题库.pdf')

    // 清理临时容器
    document.body.removeChild(tempContainer)
  } catch (error) {
    console.error('导出PDF失败:', error)
    alert('导出PDF失败，请重试')
  }
}


</script>

<style scoped>
.question-bank-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.question-bank-container h1 {
  font-size: 2.5rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.config-card, .question-item {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.config-card h2, .questions-section h2 {
  font-size: 1.8rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.config-options {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.option-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.option-group label {
  font-weight: bold;
  color: #333;
  font-size: 1.1rem;
}

.option-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.option-btn {
  padding: 15px 30px;
  border: 2px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  font-size: 1.1rem;
  flex: 1;
  min-width: 120px;
}

.option-btn:hover {
  border-color: #667eea;
}

.option-btn.active {
  background-color: #667eea;
  color: white;
  border-color: #667eea;
}

.option-desc {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.question-types {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.type-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 5px;
}

.type-label {
  font-weight: bold;
  color: #333;
}

.type-percentage {
  color: #667eea;
  font-weight: bold;
}

.option-group input[type="text"] {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.option-group input[type="text"]:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.generate-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 18px 40px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: center;
}

.generate-btn:hover {
  background-color: #369f70;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(66, 184, 131, 0.3);
}

.btn-icon {
  font-size: 1.3rem;
}

.questions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
  flex-wrap: wrap;
  gap: 20px;
}

.questions-info {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.total-count {
  font-weight: bold;
  font-size: 1.1rem;
  color: #333;
}

.topic-tag {
  padding: 5px 15px;
  background-color: #667eea;
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
}

.questions-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.action-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.action-icon {
  font-size: 1.1rem;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-item {
  border-left: 4px solid #667eea;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.question-number {
  width: 30px;
  height: 30px;
  background-color: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  font-size: 0.9rem;
}

.question-type-badge {
  padding: 5px 15px;
  background-color: #f0f4ff;
  color: #667eea;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}

.tts-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 5px;
  color: #667eea;
  transition: all 0.3s ease;
}

.tts-btn:hover {
  transform: scale(1.1);
}

.tts-icon {
  display: inline-block;
}

.question-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
  margin-bottom: 20px;
}

.question-footer {
  display: flex;
  justify-content: flex-end;
}

.expand-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.expand-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.expand-icon {
  font-size: 0.9rem;
}

.answer-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.answer-header {
  margin-bottom: 15px;
}

.answer-header h4 {
  margin: 0;
  color: #333;
  font-size: 1.1rem;
  font-weight: bold;
}

.answer-content {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 5px;
  margin-bottom: 20px;
  line-height: 1.6;
  color: #333;
}

.answer-analysis {
  background-color: #e8f4f8;
  padding: 20px;
  border-radius: 5px;
}

.answer-analysis h5 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 1rem;
  font-weight: bold;
}

.answer-analysis p {
  margin: 0;
  line-height: 1.6;
  color: #666;
}

/* 生成题库遮盖层样式 */
.generate-overlay {
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

.generate-loading {
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

.generate-loading h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.5rem;
}

.generate-loading p {
  color: #666;
  margin: 0;
  font-size: 1rem;
}

/* 禁用状态样式 */
.option-btn:disabled,
.option-group input:disabled,
.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.generate-btn:disabled:hover {
  background-color: #42b883;
  transform: none;
}

@media (max-width: 768px) {
  .question-bank-container {
    padding: 10px;
  }
  
  .question-bank-container h1 {
    font-size: 2rem;
  }
  
  .config-card, .question-item {
    padding: 20px;
  }
  
  .questions-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .questions-actions {
    width: 100%;
    justify-content: flex-start;
  }
  
  .question-header {
    flex-wrap: wrap;
  }
  
  .generate-loading {
    padding: 30px 20px;
  }
  
  .loading-spinner {
    width: 50px;
    height: 50px;
  }
}
</style>