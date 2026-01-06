# Offer贝

基于AI技术的面试辅助系统，帮助用户准备面试，提高面试成功率。

## 🚀 功能特点

### 📝 简历优化
- 支持PDF、DOCX、TXT格式简历上传
- AI智能分析简历内容
- 生成个性化优化建议
- 提供优化后的简历版本
- 简历保存和管理

### 🎤 自我介绍
- 基于简历生成个性化自我介绍
- 支持不同版本长度：30秒电梯演讲版、3分钟标准版、5分钟深度版
- 支持不同语言风格：正式、活泼、专业、亲切
- 语音朗读功能
- 提词器功能
- PDF导出功能

### 📚 智能题库
- 基于简历生成个性化题库
- 支持不同题目数量：10题、30题、50题、100题
- 题型分布：
  - 高频必问题 (30%)
  - 简历深挖题 (25%)
  - 专业技能题 (25%)
  - 行为/情景题 (20%)
- 支持自定义话题
- 提供参考答案和面试官意图分析
- 题库导出功能

### 💬 模拟面试
- 基于简历生成面试问题
- 支持不同面试风格：技术面、HR面、综合面
- 支持不同面试模式：自由模式、限时模式
- 支持不同面试时长
- 面试过程录制和回放
- 面试报告生成

### 📊 面试策略
- 基于简历生成画像分析
- 提供优化方向建议
- 生成高质量的反问问题
- 支持按问题类型生成：公司发展类、团队文化类、岗位发展类、工作内容类
- 面试策略历史记录管理

## 🛠️ 技术栈

### 前端
- **框架**: Vue 3
- **构建工具**: Vite
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **PDF生成**: jsPDF + html2canvas

### 后端
- **框架**: Flask
- **ORM**: SQLAlchemy
- **数据库**: MySQL
- **AI服务**: DeepSeek API
- **语音识别**: Aliyun SDK
- **PDF处理**: pdfplumber

## 📦 快速开始

### 环境要求
- Node.js >= 20.19.0
- Python >= 3.8
- MySQL >= 5.7

### 安装依赖

#### 前端依赖
```bash
npm install
```

#### 后端依赖
```bash
cd backend
pip install -r requirements.txt
```

### 配置环境

项目使用 `.env` 文件进行配置管理。

1. **复制配置文件**
   ```bash
   cp .env.example .env
   ```

2. **修改配置信息**
   编辑 `.env` 文件，填入您的实际配置：
   - DeepSeek API Key
   - 数据库连接信息
   - 阿里云 Access Key (用于语音识别)
   - 邮件服务配置

### 初始化数据库
```bash
cd backend
python init_db.py
```

### 启动服务

#### 前端服务
```bash
npm run dev
```

访问地址: `http://localhost:5173`

#### 后端服务
```bash
cd backend
python run.py
```

访问地址: `http://127.0.0.1:5000`

## 📁 项目结构

```
offerBei/
├── src/                     # 前端代码
│   ├── assets/              # 静态资源
│   ├── components/          # 公共组件
│   ├── views/               # 页面组件
│   │   ├── HomeView.vue
│   │   ├── ResumeView.vue
│   │   ├── SelfIntroView.vue
│   │   ├── QuestionBankView.vue
│   │   ├── MockInterviewView.vue
│   │   └── StrategyView.vue
│   ├── router/              # 路由配置
│   ├── utils/               # 工具函数
│   ├── App.vue              # 根组件
│   └── main.js              # 入口文件
├── backend/                 # 后端代码
│   ├── app/                 # 应用代码
│   │   ├── routes/         # API路由
│   │   ├── services/       # 业务服务
│   │   ├── models.py       # 数据库模型
│   │   ├── utils/          # 工具函数
│   │   └── config.py       # 配置文件
│   ├── resumes/             # 简历文件存储
│   │   ├── original/       # 原始简历
│   │   └── optimized/      # 优化后的简历
│   ├── init_db.py          # 数据库初始化
│   └── run.py              # 应用入口
├── public/                  # 公共资源
├── index.html               # HTML模板
├── package.json             # 前端依赖配置
├── vite.config.js           # Vite配置
├── requirements.txt         # 后端依赖配置
└── README.md               # 项目说明文档
```

## 📖 使用说明

### 1. 简历优化
1. 点击"简历优化"导航
2. 上传您的简历文件
3. 等待AI分析完成
4. 查看优化建议和优化后的简历
5. 下载优化后的简历

### 2. 自我介绍
1. 点击"自我介绍"导航
2. 选择自我介绍版本和风格
3. 点击"生成自我介绍"
4. 查看生成的自我介绍
5. 可以使用语音朗读、提词器或导出PDF

### 3. 智能题库
1. 点击"智能题库"导航
2. 选择题目数量
3. 可以输入自定义话题
4. 点击"生成题库"
5. 查看生成的题库
6. 可以查看参考答案或导出题库

### 4. 模拟面试
1. 点击"模拟面试"导航
2. 配置面试风格、模式和时长
3. 点击"开始面试"
4. 回答面试问题
5. 完成面试后查看面试报告

### 5. 面试策略
1. 点击"面试策略"导航
2. 输入背景信息和优化方向
3. 点击"生成分析"或"生成问题"
4. 查看生成的面试策略或反问问题
5. 可以查看历史记录

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系我们：

- 项目地址: https://github.com/hal888/offerBei.git
- 邮箱: hal888@163.com

## 📊 项目状态

![Project Status](https://img.shields.io/badge/status-active-brightgreen.svg)

---

**Offer贝** - 让面试更简单，让成功更靠近！🚀