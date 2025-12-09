from flask import Blueprint, request, jsonify
import random
import uuid
import json
from ..services.deepseek_service import client
from ..services.file_service import get_resume_content
from ..models import db, User, MockInterview

# 创建蓝图
bp = Blueprint('mock_interview', __name__, url_prefix='/api/mock-interview')

# 保存面试会话的字典（生产环境中应使用数据库）
interview_sessions = {}

@bp.route('/start', methods=['POST'])
def start():
    """开始模拟面试API"""
    data = request.get_json()
    style = data.get('style', '温柔HR')
    mode = data.get('mode', '文字模式')
    duration = data.get('duration', 15)
    user_id = data.get('userId', 'default_user')
    
    # 打印请求参数
    print(f"[API LOG] /api/mock-interview/start - Request received: style={style}, mode={mode}, duration={duration}, userId={user_id}")
    
    # 根据userId获取最新的resumeId
    resume_id = '1'  # 默认值
    try:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            # 获取用户最新的简历
            from app.models import Resume
            latest_resume = Resume.query.filter_by(user_id=user.id).order_by(Resume.updated_at.desc()).first()
            if latest_resume:
                resume_id = latest_resume.resume_id
                print(f"[API LOG] 使用用户最新的简历ID: {resume_id}")
    except Exception as e:
        print(f"获取用户最新简历失败: {e}")
    
    # 获取简历内容
    resume_content = get_resume_content(resume_id, 'optimized')
    
    # 生成interviewId
    interview_id = f"interview_{uuid.uuid4().hex[:8]}"
    
    # 构建prompt生成第一个问题（使用字符串连接避免格式说明符问题）
    prompt = "你是一位" + style + "风格的面试官，正在为候选人进行面试。请基于以下简历内容，生成第一个面试问题，要求：\n\n1. 问题类型：高频必问题（如自我介绍、求职动机等）\n2. 问题要与候选人的简历背景相关\n3. 语言风格符合" + style + "特点\n4. 仅输出JSON格式，包含id、content、type字段\n5. 不要包含任何额外的文字或解释\n\n简历内容：\n" + resume_content
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位" + style + "风格的专业面试官"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=512
        )
        
        import json
        import re
        
        # 解析API返回结果
        api_result = response.choices[0].message.content
        
        # 清理可能的额外内容，只保留JSON部分
        start_idx = api_result.find('{')
        end_idx = api_result.rfind('}') + 1
        if start_idx == -1 or end_idx <= start_idx:
            # 如果解析失败，使用默认问题
            first_question = {"id": 1, "content": "请介绍一下你自己", "type": "高频必问题"}
        else:
            json_content = api_result[start_idx:end_idx]
            first_question = json.loads(json_content)
        
        # 保存会话信息
        interview_sessions[interview_id] = {
            "style": style,
            "mode": mode,
            "duration": duration,
            "resume_id": resume_id,
            "resume_content": resume_content,
            "current_question_id": 1,
            "total_questions": 10,
            "conversation_history": [],
            "question_answers": []
        }
        
        return jsonify({
            "interviewId": interview_id,
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
        
    except Exception as e:
        print(f"生成第一个问题失败: {e}")
        # 使用默认问题作为备选
        first_question = {"id": 1, "content": "请介绍一下你自己", "type": "高频必问题"}
        
        return jsonify({
            "interviewId": interview_id,
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

@bp.route('/answer', methods=['POST'])
def answer():
    """回答问题API"""
    data = request.get_json()
    interview_id = data.get('interviewId')
    question_id = data.get('questionId')
    answer = data.get('answer')
    
    # 打印请求参数
    print(f"[API LOG] /api/mock-interview/answer - Request received: interviewId={interview_id}, questionId={question_id}, answer={answer[:50]}...")
    
    # 检查会话是否存在
    if interview_id not in interview_sessions:
        return jsonify({"error": "面试会话不存在"}), 404
    
    session = interview_sessions[interview_id]
    
    # 保存当前问题和回答
    session["question_answers"].append({
        "question_id": question_id,
        "question": session["conversation_history"][-1] if session["conversation_history"] else "请介绍一下你自己",
        "answer": answer
    })
    
    # 构建prompt生成反馈和下一个问题（使用字符串连接避免格式说明符问题）
    current_question = session["conversation_history"][-1] if session["conversation_history"] else "请介绍一下你自己"
    prompt = "你是一位" + session['style'] + "风格的面试官，正在为候选人进行面试。请基于以下信息：\n\n1. 简历内容：" + session['resume_content'] + "\n2. 对话历史：" + str(session['conversation_history']) + "\n3. 当前问题：" + current_question + "\n4. 候选人回答：" + answer + "\n\n请完成以下任务：\n\n1. 生成对当前回答的反馈，要求：\n   - 评价回答的质量、逻辑、深度\n   - 指出优点和不足\n   - 语言风格符合" + session['style'] + "\n\n2. 生成下一个面试问题，要求：\n   - 问题类型多样（简历深挖题、专业技能题、行为/情景题等）\n   - 与候选人的简历和对话历史相关\n   - 难度适中，符合面试流程\n\n输出格式要求：\n{\"feedback\": \"对当前回答的反馈\", \"nextQuestion\": {\"id\": 数字id, \"content\": \"下一个问题内容\", \"type\": \"问题类型\"}}\n\n只输出JSON格式，不要包含任何额外的文字或解释。"
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位" + session['style'] + "风格的专业面试官"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        import json
        import re
        
        # 解析API返回结果
        api_result = response.choices[0].message.content
        
        # 清理可能的额外内容，只保留JSON部分
        start_idx = api_result.find('{')
        end_idx = api_result.rfind('}') + 1
        if start_idx == -1 or end_idx <= start_idx:
            # 如果解析失败，使用默认反馈和问题
            result = {
                "feedback": "您的回答结构清晰，重点突出，但可以更具体地描述项目成果。",
                "nextQuestion": {
                    "id": session["current_question_id"] + 1,
                    "content": "您为什么想来我们公司工作？",
                    "type": "高频必问题"
                }
            }
        else:
            json_content = api_result[start_idx:end_idx]
            result = json.loads(json_content)
            result["nextQuestion"]["id"] = session["current_question_id"] + 1
        
        # 更新会话信息
        session["current_question_id"] += 1
        session["conversation_history"].append(result["nextQuestion"]["content"])
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"生成反馈和下一个问题失败: {e}")
        # 使用默认反馈和问题作为备选
        result = {
            "feedback": "您的回答结构清晰，重点突出，但可以更具体地描述项目成果。",
            "nextQuestion": {
                "id": session["current_question_id"] + 1,
                "content": "您为什么想来我们公司工作？",
                "type": "高频必问题"
            }
        }
        
        # 更新会话信息
        session["current_question_id"] += 1
        session["conversation_history"].append(result["nextQuestion"]["content"])
        
        return jsonify(result), 200

@bp.route('/end', methods=['POST'])
def end():
    """结束模拟面试API"""
    data = request.get_json()
    interview_id = data.get('interviewId')
    user_id = data.get('userId', 'default_user')
    
    # 打印请求参数
    print(f"[API LOG] /api/mock-interview/end - Request received: interviewId={interview_id}, userId={user_id}")
    
    # 检查会话是否存在
    if interview_id not in interview_sessions:
        return jsonify({"error": "面试会话不存在"}), 404
    
    session = interview_sessions[interview_id]
    
    # 构建prompt生成面试报告（使用字符串连接避免格式说明符问题）
    prompt = "你是一位专业的面试评估专家，正在为候选人生成面试报告。请基于以下信息：\n\n1. 简历内容：" + session['resume_content'] + "\n2. 面试风格：" + session['style'] + "\n3. 面试时长：" + str(session['duration']) + "分钟\n4. 问答记录：" + str(session['question_answers']) + "\n5. 对话历史：" + str(session['conversation_history']) + "\n\n请生成一份详细的面试报告，要求：\n\n1. 包含以下评分项（0-100分）：\n   - professionalScore：专业能力评分\n   - logicScore：逻辑表达评分\n   - confidenceScore：自信程度评分\n   - matchScore：岗位匹配度评分\n\n2. 逐题诊断，每个问题包含：\n   - question：问题内容\n   - answer：候选人回答\n   - feedback：对该回答的评价\n   - suggestion：改进建议\n\n3. 优化建议，包含至少4条针对性建议\n\n输出格式要求：\n{\"professionalScore\": 数字, \"logicScore\": 数字, \"confidenceScore\": 数字, \"matchScore\": 数字, \"questionAnalysis\": [{\"question\": \"问题内容\", \"answer\": \"候选人回答\", \"feedback\": \"评价\", \"suggestion\": \"改进建议\"}], \"optimizationSuggestions\": [\"建议1\", \"建议2\"]}\n\n只输出JSON格式，不要包含任何额外的文字或解释。"
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位专业的面试评估专家"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        
        # 解析API返回结果
        api_result = response.choices[0].message.content
        
        # 清理可能的额外内容，只保留JSON部分
        start_idx = api_result.find('{')
        end_idx = api_result.rfind('}') + 1
        if start_idx == -1 or end_idx <= start_idx:
            # 如果解析失败，使用默认报告
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
        else:
            json_content = api_result[start_idx:end_idx]
            report = json.loads(json_content)
        
        # 保存到数据库
        try:
            # 获取或创建用户
            user = User.query.filter_by(user_id=user_id).first()
            if not user:
                user = User(user_id=user_id)
                db.session.add(user)
                db.session.commit()
            
            # 创建MockInterview记录
            mock_interview = MockInterview(
                user_id=user.id,
                resume_id=session['resume_id'],
                style=session['style'],
                mode=session['mode'],
                duration=session['duration'],
                conversation_history=json.dumps(session['conversation_history']),
                question_answers=json.dumps(session['question_answers']),
                report=json.dumps(report)
            )
            db.session.add(mock_interview)
            db.session.commit()
        except Exception as db_error:
            print(f"保存模拟面试到数据库失败: {db_error}")
        
        # 删除会话信息
        del interview_sessions[interview_id]
        
        return jsonify(report), 200
        
    except Exception as e:
        print(f"生成面试报告失败: {e}")
        # 使用默认报告作为备选
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
        
        # 删除会话信息
        del interview_sessions[interview_id]
        
        return jsonify(report), 200

@bp.route('/history', methods=['GET'])
def get_history():
    """获取用户的模拟面试历史记录API"""
    user_id = request.args.get('userId', 'default_user')
    
    # 打印请求参数
    print(f"[API LOG] /api/mock-interview/history - Request received: userId={user_id}")
    
    if not user_id:
        return jsonify({"error": "Missing userId"}), 400
    
    try:
        # 获取用户
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # 获取用户的所有模拟面试记录
        mock_interviews = MockInterview.query.filter_by(user_id=user.id).order_by(MockInterview.created_at.desc()).all()
        
        # 转换为前端需要的格式
        history = []
        for interview in mock_interviews:
            history.append({
                "id": interview.id,
                "style": interview.style,
                "mode": interview.mode,
                "duration": interview.duration,
                "resume_id": interview.resume_id,
                "created_at": interview.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "report": json.loads(interview.report) if interview.report else {}
            })
        
        return jsonify(history), 200
    except Exception as e:
        print(f"获取模拟面试历史失败: {e}")
        return jsonify({"error": "Failed to get mock interview history"}), 500