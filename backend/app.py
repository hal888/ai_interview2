from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import os
from openai import OpenAI
from docx import Document
from PyPDF2 import PdfReader

# 导入配置文件
from config import DEEPSEEK_CONFIG

app = Flask(__name__)
CORS(app)  # 解决跨域问题

# 配置DeepSeek API客户端
client = OpenAI(
    api_key=DEEPSEEK_CONFIG["api_key"],
    base_url=DEEPSEEK_CONFIG["base_url"]
)

# 文件读取和解析函数
def read_file_content(file_path, file_ext):
    """读取文件内容，支持PDF和DOCX格式"""
    content = ""
    
    try:
        if file_ext == 'pdf':
            # 使用PyMuPDF替代PyPDF2，优化PDF文本提取
            import fitz  # PyMuPDF的导入名是fitz
            doc = fitz.open(file_path)
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                # 提取文本，使用空格分隔避免格式错乱
                page_text = page.get_text("text") or ""
                # 清理文本，移除多余的空行和空格
                page_text = '\n'.join([line.strip() for line in page_text.split('\n') if line.strip()])
                content += page_text + "\n\n"
            doc.close()
        elif file_ext == 'docx':
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
        else:
            # 处理纯文本文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        content = ""
    print(f"读取到的文件内容：{content}")
    return content

# 简化的Markdown解析函数
def parse_markdown_result(content):
    """解析函数，处理JSON格式响应，不回退到Markdown解析"""
    # 默认结果结构
    result = {
        "score": 0,
        "diagnosis": [],
        "keywords": [],
        "starRewrite": [],
        "optimizedResume": ""
    }
    # content内容写入文件
    with open('response.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("=== 开始JSON解析 ===")
    print(f"原始响应长度：{len(content)}字符")
    print(f"响应前内容：{content}")
    
    try:
        import json
        import re
        
        # 1. 清理可能的额外内容，只保留JSON部分
        # 查找JSON的起始和结束位置
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        
        if start_idx == -1:
            print("❌ 未找到JSON起始标记 '{'")
            return result
        
        if end_idx <= start_idx:
            print(f"❌ JSON结束位置无效：start={start_idx}, end={end_idx}")
            return result
        
        # 提取JSON内容
        json_content = content[start_idx:end_idx]
        print(f"✓ 提取JSON内容：{len(json_content)}字符")
        print(f"✓ JSON前50字符：{json_content[:50]}...")
        
        # 2. 清理JSON中的可能问题
        # 移除可能的Markdown代码块标记
        json_content = json_content.replace('```json', '').replace('```', '')
        
        # 移除多余的换行符和空格
        json_content = ' '.join(json_content.split())
        
        # 确保所有字符串使用双引号
        json_content = json_content.replace("'", '"')
        
        # 3. 修复常见JSON格式问题
        # 修复尾随逗号（在}或]之前的逗号）
        json_content = re.sub(r',\s*([}\]])', r' \1', json_content)
        
        # 移除JSON中的注释（如果有）
        json_content = re.sub(r'//.*?(?=\\n|$)', '', json_content)
        json_content = re.sub(r'/\*.*?\*/', '', json_content, flags=re.DOTALL)
        
        # 移除可能的控制字符，但保留Unicode字符
        json_content = re.sub(r'[\x00-\x1f\x7f]', '', json_content)  # 只移除控制字符
        
        print(f"✓ 清理后JSON：{json_content[:100]}...")
        
        # 3. 解析JSON
        json_result = json.loads(json_content)
        print("✓ JSON解析成功！")
        
        # 4. 验证并提取所需字段
        if not isinstance(json_result, dict):
            print("❌ JSON结果不是对象类型")
            return result
        
        print(f"✓ 提取到字段：{list(json_result.keys())}")
        
        # 提取评分
        if 'score' in json_result and isinstance(json_result['score'], (int, float)):
            result['score'] = int(json_result['score'])
            print(f"✓ 提取评分：{result['score']}")
        
        # 提取诊断意见
        if 'diagnosis' in json_result and isinstance(json_result['diagnosis'], list):
            valid_types = ['警告', '错误', '建议']
            for item in json_result['diagnosis']:
                if isinstance(item, dict) and \
                   all(k in item for k in ['type', 'title', 'description']) and \
                   item['type'] in valid_types:
                    result['diagnosis'].append({
                        "type": item['type'],
                        "title": item['title'],
                        "description": item['description']
                    })
            print(f"✓ 提取诊断意见：{len(result['diagnosis'])}条")
        
        # 提取关键词
        if 'keywords' in json_result and isinstance(json_result['keywords'], list):
            result['keywords'] = [k.strip() for k in json_result['keywords'] if isinstance(k, str) and k.strip()]
            print(f"✓ 提取关键词：{len(result['keywords'])}个")
        
        # 提取STAR法则重写
        if 'starRewrite' in json_result and isinstance(json_result['starRewrite'], list):
            for item in json_result['starRewrite']:
                if isinstance(item, dict):
                    result['starRewrite'].append({
                        "situation": item.get('situation', '').strip(),
                        "task": item.get('task', '').strip(),
                        "action": item.get('action', '').strip(),
                        "result": item.get('result', '').strip()
                    })
            print(f"✓ 提取STAR重写：{len(result['starRewrite'])}条")
        
        # 提取优化后简历
        if 'optimizedResume' in json_result and isinstance(json_result['optimizedResume'], str):
            result['optimizedResume'] = json_result['optimizedResume'].strip()
            print(f"✓ 提取优化后简历：{len(result['optimizedResume'])}字符")
        
        print("=== JSON解析完成 ===")
        return result
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误：{e}")
        print(f"❌ 错误位置：行{e.lineno}，列{e.colno}")
        print(f"❌ 错误片段：{json_content[max(0, e.pos-20):e.pos+20]}")
    except Exception as e:
        print(f"❌ JSON处理异常：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("=== JSON解析失败 ===")
    return result

# 模拟数据
mock_resume_data = {
    "score": 75,
    "diagnosis": [
        {
            "type": "警告",
            "title": "缺乏量化结果",
            "description": "您的工作经历中缺乏具体的数据支撑，建议使用STAR法则进行重写"
        },
        {
            "type": "错误",
            "title": "格式不一致",
            "description": "简历中存在字体大小和间距不一致的问题，建议统一格式"
        },
        {
            "type": "建议",
            "title": "关键词不足",
            "description": "简历中缺少与目标岗位相关的关键词，建议适当添加"
        }
    ],
    "keywords": ["JavaScript", "Vue", "React", "Node.js", "RESTful API", "数据库设计", "性能优化", "团队协作"]
}

mock_questions = [
    {
        "id": 1,
        "content": "请介绍一下你自己",
        "type": "高频必问题",
        "answer": "这是一个高频必问题的参考答案，建议结合自身经历进行回答。在回答时，应突出自己的核心优势和与岗位的匹配度，保持简洁明了，重点突出。",
        "analysis": "面试官通过这类问题了解你的基本情况、沟通能力和自我认知，判断你是否符合公司的招聘需求和企业文化。"
    },
    {
        "id": 2,
        "content": "您为什么想来我们公司工作？",
        "type": "高频必问题",
        "answer": "我非常欣赏贵公司在行业中的领先地位和创新精神，特别是贵公司最近推出的XX产品给我留下了深刻的印象。我认为我的技能和经验非常适合这个岗位，同时我也非常认同贵公司的企业文化和价值观。",
        "analysis": "面试官通过这个问题了解你对公司的了解程度和求职动机，判断你是否真心想加入公司。"
    },
    {
        "id": 3,
        "content": "您认为自己最大的优点是什么？",
        "type": "高频必问题",
        "answer": "我认为自己最大的优点是具有较强的学习能力和团队协作精神。我能够快速适应新的技术和环境，同时也能够与团队成员保持良好的沟通和协作，共同完成项目目标。",
        "analysis": "面试官通过这个问题了解你的自我认知和核心优势，判断你是否适合这个岗位。"
    },
    {
        "id": 4,
        "content": "请详细描述你在项目中负责的工作内容和遇到的挑战",
        "type": "简历深挖题",
        "answer": "在回答简历深挖题时，建议使用STAR法则：情境(Situation)、任务(Task)、行动(Action)、结果(Result)。详细描述项目背景、你的职责、采取的行动以及取得的成果，重点突出你的贡献和解决问题的能力。",
        "analysis": "面试官通过这类问题验证你简历的真实性，了解你的实际工作能力和项目经验，判断你是否具备胜任目标岗位的能力。"
    },
    {
        "id": 5,
        "content": "请解释一下Vue框架的核心原理",
        "type": "专业技能题",
        "answer": "对于专业技能题，建议从核心概念、工作原理、使用场景、优缺点等方面进行回答。如果是技术问题，可以结合实际项目经验，说明如何在项目中应用该技术，以及遇到的问题和解决方案。",
        "analysis": "面试官通过这类问题考察你的专业知识掌握程度，判断你是否具备岗位所需的技术能力和解决问题的能力。"
    },
    {
        "id": 6,
        "content": "请描述一个你在工作中解决的复杂问题",
        "type": "行为/情景题",
        "answer": "行为/情景题考察的是你的实际工作能力和行为模式，建议使用STAR法则进行回答。选择一个具体的案例，详细描述事件的背景、你的任务、采取的行动以及最终的结果，重点突出你的能力和特质。",
        "analysis": "面试官通过这类问题了解你的行为模式、价值观和处理问题的方式，判断你是否与岗位和团队文化匹配。"
    }
]

# API端点

@app.route('/api/resume/analyze', methods=['POST'])
def analyze_resume():
    """简历分析API"""
    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # 获取文件信息
    filename = file.filename
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    # 保存文件到临时目录
    temp_dir = '/tmp/resume_uploads'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    file_path = os.path.join(temp_dir, filename)
    file.save(file_path)
    
    # 读取文件内容
    file_content = read_file_content(file_path, file_ext)
    content_length = len(file_content)
    # 文件内容写入文件
    with open('resume.txt', 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    if not file_content:
        # 清理临时文件
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({"error": "无法读取文件内容"}), 400
    
    # 调用DeepSeek API进行简历分析
    prompt = f"""
    请对以下简历内容进行全面分析和优化，并严格按照以下要求输出JSON格式结果：
    
    ## 输出要求：
    1. **仅输出JSON字符串**，不要包含任何额外的文字、解释或说明
    2. JSON格式必须严格有效，使用双引号，转义所有特殊字符（如换行符\n）
    3. 确保所有字段类型正确
    4. 不要包含任何Markdown格式或其他格式标记
    
    ## 必须包含的字段：
    - `score`: 整数，0-100分的综合评分
    - `diagnosis`: 数组，每条诊断包含`type`(警告/错误/建议)、`title`、`description`
    - `keywords`: 数组，至少10个与技术岗位相关的关键词
    - `starRewrite`: 数组，每条STAR包含`situation`、`task`、`action`、`result`
    - `optimizedResume`: 字符串，完整的优化后简历内容
    
    ## 示例输出格式：
    ```json
    {{"score":85,"diagnosis":[{{"type":"警告","title":"缺乏量化结果","description":"工作经历中缺乏具体的数据支撑"}}],"keywords":["JavaScript","Vue"],"starRewrite":[{{"situation":"在电商项目中","task":"负责前端开发","action":"使用Vue框架开发","result":"提升了页面性能"}}],"optimizedResume":"# 优化后简历\n\n## 个人信息\n张三 | 前端开发工程师"}}
    ```
    
    简历内容：
    {file_content}
    """
    
    response = client.chat.completions.create(
        model=DEEPSEEK_CONFIG["model"],
        messages=[
            {"role": "system", "content": "你是一位专业的简历分析专家，擅长评估技术岗位的简历"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4096
    )
    
    # 解析API返回结果
    api_result = response.choices[0].message.content
    print(api_result)
    
    # 使用简化的解析函数生成结构化结果
    parsed_result = parse_markdown_result(api_result)
    print(parsed_result)
    
    # 生成最终的分析结果
    analysis_result = {
        "score": parsed_result["score"],
        "diagnosis": parsed_result["diagnosis"],
        "keywords": parsed_result["keywords"],
        "starRewrite": parsed_result["starRewrite"],
        "optimizedResume": parsed_result["optimizedResume"],
        "fileInfo": {
            "filename": filename,
            "fileType": file_ext,
            "contentLength": content_length
        },
        "apiResponse": api_result  # 保留原始API响应，方便调试
    }
    
    # 保存原始简历内容
    import uuid
    resume_id = str(uuid.uuid4())
    original_resume_path = os.path.join('resumes', 'original', f'{resume_id}.txt')
    with open(original_resume_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    # 保存优化后的简历内容
    optimized_resume_path = os.path.join('resumes', 'optimized', f'{resume_id}.txt')
    if parsed_result['optimizedResume']:
        with open(optimized_resume_path, 'w', encoding='utf-8') as f:
            f.write(parsed_result['optimizedResume'])
    
    # 清理临时文件
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # 返回结果时包含resume_id
    analysis_result['resumeId'] = resume_id
    
    return jsonify(analysis_result), 200

@app.route('/api/self-intro/generate', methods=['POST'])
def generate_self_intro():
    """生成自我介绍API - 优先使用优化后的简历"""
    data = request.get_json()
    resume_id = data.get('resumeId')
    version = data.get('version', '30秒电梯演讲版')
    style = data.get('style', '正式')
    user_info = data.get('userInfo', '')
    
    # 根据版本确定预计时长
    estimated_time = "0.5" if version == '30秒电梯演讲版' else "3" if version == '3分钟标准版' else "5"
    
    # 优先使用优化后的简历内容
    resume_content = ""
    if resume_id:
        optimized_resume_path = os.path.join('resumes', 'optimized', f'{resume_id}.txt')
        try:
            with open(optimized_resume_path, 'r', encoding='utf-8') as f:
                resume_content = f.read()
        except FileNotFoundError:
            # 简历文件不存在，回退到使用userInfo
            resume_content = user_info
    else:
        # 没有resumeId，使用userInfo
        resume_content = user_info
    
    # 调用DeepSeek API生成自我介绍
    if resume_content:
        prompt = f"""
        请根据以下信息，生成一个{style}风格的{version}自我介绍。
        
        ## 信息内容：
        {resume_content}
        
        ## 输出要求：
        1. 仅输出自我介绍文本，不要包含任何额外内容
        2. 自我介绍必须基于提供的信息，不要编造信息
        3. 语言流畅，符合{style}风格
        4. 时长控制在{version}对应的时间范围内
        5. 突出个人优势和核心竞争力
        6. 开头要有礼貌的问候语
        """
    else:
        # 如果没有任何信息，生成通用自我介绍
        prompt = f"""
        请生成一个{style}风格的{version}通用自我介绍。
        
        ## 输出要求：
        1. 仅输出自我介绍文本，不要包含任何额外内容
        2. 语言流畅，符合{style}风格
        3. 时长控制在{version}对应的时间范围内
        4. 突出个人优势和核心竞争力
        5. 开头要有礼貌的问候语
        6. 适用于大多数职业场景
        """
    
    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_CONFIG["model"],
            messages=[
                {"role": "system", "content": "你是一位专业的自我介绍生成专家，擅长生成自然、流畅、有吸引力的自我介绍"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        intro = response.choices[0].message.content.strip()
        
        return jsonify({
            "intro": intro,
            "version": version,
            "style": style,
            "estimatedTime": estimated_time
        }), 200
    except Exception as e:
        print(f"生成自我介绍失败: {e}")
        return jsonify({"error": "生成自我介绍失败，请重试"}), 500

@app.route('/api/question-bank/generate', methods=['POST'])
def generate_questions():
    """生成题库API"""
    data = request.get_json()
    count = data.get('count', 50)
    topic = data.get('topic', '')
    
    # 随机选择问题
    selected_questions = random.sample(mock_questions, min(count, len(mock_questions)))
    
    return jsonify({
        "questions": selected_questions,
        "total": len(selected_questions),
        "topic": topic
    }), 200

@app.route('/api/mock-interview/start', methods=['POST'])
def start_mock_interview():
    """开始模拟面试API"""
    data = request.get_json()
    style = data.get('style', '温柔HR')
    mode = data.get('mode', '文字模式')
    duration = data.get('duration', 15)
    
    # 生成第一个问题
    first_question = mock_questions[0]
    
    return jsonify({
        "interviewId": "mock_123",
        "style": style,
        "mode": mode,
        "duration": duration,
        "currentQuestion": {
            "id": first_question['id'],
            "content": first_question['content'],
            "type": first_question['type']
        },
        "tips": ["保持微笑，展现自信", "回答问题时保持逻辑清晰", "注意控制语速，避免过快或过慢"]
    }), 200

@app.route('/api/mock-interview/answer', methods=['POST'])
def answer_question():
    """回答问题API"""
    data = request.get_json()
    interview_id = data.get('interviewId')
    question_id = data.get('questionId')
    answer = data.get('answer')
    
    # 模拟生成下一个问题
    next_question = random.choice(mock_questions[1:])
    
    return jsonify({
        "nextQuestion": {
            "id": next_question['id'],
            "content": next_question['content'],
            "type": next_question['type']
        },
        "feedback": "您的回答结构清晰，重点突出，但可以更具体地描述项目成果。"
    }), 200

@app.route('/api/mock-interview/end', methods=['POST'])
def end_mock_interview():
    """结束模拟面试API"""
    data = request.get_json()
    interview_id = data.get('interviewId')
    
    # 生成面试报告
    report = {
        "professionalScore": 85,
        "logicScore": 78,
        "confidenceScore": 82,
        "matchScore": 80,
        "questionAnalysis": [
            {
                "question": "请介绍一下你自己",
                "answer": "我是一名前端开发工程师，有5年工作经验...",
                "feedback": "回答结构清晰，重点突出，但可以更具体地描述项目成果",
                "suggestion": "建议使用STAR法则，增加数据支撑"
            }
        ],
        "optimizationSuggestions": [
            "加强专业术语的使用，提升专业性",
            "注意语速控制，保持清晰流畅",
            "增加具体案例，增强说服力",
            "加强与面试官的眼神交流（视频面试）"
        ]
    }
    
    return jsonify(report), 200

@app.route('/api/strategy/analysis', methods=['POST'])
def generate_strategy_analysis():
    """生成策略分析API"""
    data = request.get_json()
    background_info = data.get('backgroundInfo', '')
    directions = data.get('directions', [])
    
    # 生成分析结果
    sections = []
    if '空窗期分析' in directions or not directions:
        sections.append({
            "title": "空窗期分析和应对策略",
            "content": "根据您提供的信息，您有6个月的职业空窗期。这段时间您主要在学习新技术，这是一个积极的信号。",
            "tips": [
                "在面试中主动提及空窗期，展示您在这段时间的成长和收获",
                "重点强调您学习的新技术与目标岗位的相关性",
                "准备具体的学习成果展示，如项目作品、证书等",
                "保持积极的态度，避免负面情绪表达"
            ]
        })
    
    if '防御性话术' in directions or not directions:
        sections.append({
            "title": "防御性话术建议",
            "content": "针对可能被问到的敏感问题，建议您准备以下话术：",
            "tips": [
                '关于薪资期望："我希望薪资能反映我的技能和经验水平，同时也考虑公司的薪酬体系"',
                '关于离职原因："我希望寻找更有挑战性的工作机会，贵公司的岗位非常符合我的职业发展方向"',
                '关于缺点："我有时候会过于追求完美，导致项目进度稍有延迟，但我正在学习更好地平衡质量和效率"',
                '关于职业规划："我希望在未来3-5年内成长为一名高级前端开发工程师，负责复杂项目的架构设计"'
            ]
        })
    
    return jsonify({"sections": sections}), 200

@app.route('/api/strategy/questions', methods=['POST'])
def generate_questions_for_company():
    """生成公司问题API"""
    data = request.get_json()
    company_name = data.get('companyName', '')
    position = data.get('position', '')
    question_types = data.get('questionTypes', [])
    
    # 生成问题
    generated_questions = [
        {
            "content": "请问贵公司这个岗位的核心职责是什么？",
            "type": "工作内容类",
            "explanation": "了解岗位的具体工作内容，判断是否与自己的技能和兴趣匹配"
        },
        {
            "content": "贵公司的团队文化是什么样的？",
            "type": "团队文化类",
            "explanation": "了解公司的工作氛围和价值观，判断自己是否能适应"
        },
        {
            "content": "这个岗位在公司的发展路径是怎样的？",
            "type": "岗位发展类",
            "explanation": "了解职业发展空间，判断公司是否能提供自己所需的成长机会"
        },
        {
            "content": "贵公司未来3-5年的发展规划是什么？",
            "type": "公司发展类",
            "explanation": "了解公司的战略方向，判断公司的发展前景"
        }
    ]
    
    return jsonify({"questions": generated_questions}), 200

if __name__ == '__main__':
    app.run(debug=False, port=5000)
