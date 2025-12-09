from flask import Blueprint, request, jsonify
from ..services.deepseek_service import generate_self_intro
from ..services.file_service import get_resume_content
from ..models import db, User, SelfIntro
import uuid

# 创建蓝图
bp = Blueprint('self_intro', __name__, url_prefix='/api/self-intro')

@bp.route('/generate', methods=['POST'])
def generate():
    """根据优化后的简历生成自我介绍API"""
    data = request.get_json()
    version = data.get('version', '30秒电梯演讲版')
    style = data.get('style', '正式')
    user_info = data.get('userInfo', '')
    user_id = data.get('userId') or str(uuid.uuid4())
    
    # 根据userId获取最新的resumeId
    resume_id = None
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
    
    # 打印请求参数
    print(f"[API LOG] /api/self-intro/generate - Request received: resumeId={resume_id}, version={version}, style={style}, userInfo={user_info[:50]}..., userId={user_id}")
    
    # 根据版本确定预计时长
    estimated_time = "0.5" if version == '30秒电梯演讲版' else "3" if version == '3分钟标准版' else "5"
    
    # 优先使用优化后的简历内容
    resume_content = ""
    if resume_id:
        resume_content = get_resume_content(resume_id, 'optimized')
    
    # 如果没有简历内容，使用userInfo
    if not resume_content:
        resume_content = user_info
    
    # 调用DeepSeek API生成自我介绍
    try:
        intro = generate_self_intro(resume_content, version, style)
        
        # 保存到数据库
        try:
            # 查询或创建用户
            user = User.query.filter_by(user_id=user_id).first()
            if not user:
                user = User(user_id=user_id)
                db.session.add(user)
                db.session.commit()  # 立即提交，获取user.id
            
            # 创建自我介绍记录
            self_intro = SelfIntro(
                user_id=user.id,
                resume_id=resume_id or "1",
                self_intro_type=f"{version}_{style}",
                content=intro
            )
            db.session.add(self_intro)
            db.session.commit()
        except Exception as e:
            print(f"保存自我介绍到数据库失败: {e}")
            db.session.rollback()
        
        return jsonify({
            "intro": intro,
            "version": version,
            "style": style,
            "estimatedTime": estimated_time,
            "userId": user_id  # 返回user_id，前端保存到localStorage
        }), 200
    except Exception as e:
        print(f"生成自我介绍失败: {e}")
        return jsonify({"error": "生成自我介绍失败，请重试"}), 500

@bp.route('/get', methods=['POST'])
def get_self_intro():
    """获取已生成的自我介绍数据"""
    data = request.get_json()
    user_id = data.get('userId')
    intro_type = data.get('introType')
    
    # 打印请求参数
    print(f"[API LOG] /api/self-intro/get - Request received: userId={user_id}, introType={intro_type}")
    
    if not user_id:
        return jsonify({"error": "Missing userId"}), 400
    
    try:
        # 查询用户
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # 查询自我介绍数据
        if intro_type:
            # 查询指定类型的自我介绍
            self_intro = SelfIntro.query.filter_by(self_intro_type=intro_type, user_id=user.id).first()
        else:
            # 查询最新的自我介绍
            self_intro = SelfIntro.query.filter_by(user_id=user.id).order_by(SelfIntro.updated_at.desc()).first()
        
        if not self_intro:
            return jsonify({"error": "Self introduction not found"}), 404
        
        # 提取版本和风格
        version_style = self_intro.self_intro_type.split('_', 1)
        version = version_style[0]
        style = version_style[1] if len(version_style) > 1 else '正式'
        
        # 根据版本确定预计时长
        estimated_time = "0.5" if version == '30秒电梯演讲版' else "3" if version == '3分钟标准版' else "5"
        
        # 构造返回结果
        result = {
            "intro": self_intro.content,
            "version": version,
            "style": style,
            "estimatedTime": estimated_time,
            "resumeId": self_intro.resume_id,
            "userId": user.user_id
        }
        
        return jsonify(result), 200
    except Exception as e:
        print(f"查询自我介绍失败: {e}")
        return jsonify({"error": "Failed to get self introduction"}), 500
