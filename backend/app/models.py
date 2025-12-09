from flask_sqlalchemy import SQLAlchemy
import datetime
import uuid

# 创建SQLAlchemy实例
db = SQLAlchemy()

# 用户表
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), unique=True, nullable=False)  # 前端localStorage中的user_id
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    # 关系
    resumes = db.relationship('Resume', backref='user', lazy=True)
    self_intros = db.relationship('SelfIntro', backref='user', lazy=True)
    question_banks = db.relationship('QuestionBank', backref='user', lazy=True)
    mock_interviews = db.relationship('MockInterview', backref='user', lazy=True)
    interview_strategies = db.relationship('InterviewStrategy', backref='user', lazy=True)

# 简历表
class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = db.Column(db.String(8), unique=True, nullable=False)  # 前端使用的resume_id
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    original_content = db.Column(db.Text, nullable=True)
    optimized_content = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)
    diagnosis = db.Column(db.JSON, nullable=True)  # 智能诊断
    keywords = db.Column(db.JSON, nullable=True)  # 关键词
    star_rewrite = db.Column(db.JSON, nullable=True)  # STAR法则重写
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

# 自我介绍表
class SelfIntro(db.Model):
    __tablename__ = 'self_intros'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.String(8), nullable=False)  # 关联的简历ID
    self_intro_type = db.Column(db.String(50), nullable=False)  # 自我介绍类型
    content = db.Column(db.Text, nullable=False)  # 自我介绍内容
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

# 智能题库表
class QuestionBank(db.Model):
    __tablename__ = 'question_banks'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.String(8), nullable=False)  # 关联的简历ID
    count = db.Column(db.Integer, nullable=False)  # 题库数量
    questions = db.Column(db.JSON, nullable=False)  # 生成的问题列表
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

# 模拟面试表
class MockInterview(db.Model):
    __tablename__ = 'mock_interviews'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.String(8), nullable=False)  # 关联的简历ID
    style = db.Column(db.String(50), nullable=False)  # 面试风格
    mode = db.Column(db.String(50), nullable=False)  # 面试模式
    duration = db.Column(db.Integer, nullable=False)  # 面试时长
    conversation_history = db.Column(db.JSON, nullable=True)  # 对话历史
    question_answers = db.Column(db.JSON, nullable=True)  # 问答记录
    report = db.Column(db.JSON, nullable=True)  # 面试报告
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

# 面试策略表
class InterviewStrategy(db.Model):
    __tablename__ = 'interview_strategies'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.String(8), nullable=False)  # 关联的简历ID
    type = db.Column(db.String(20), nullable=False)  # 策略类型：analysis或questions
    background_info = db.Column(db.Text, nullable=True)  # 背景信息
    directions = db.Column(db.JSON, nullable=True)  # 优化方向
    company_name = db.Column(db.String(100), nullable=True)  # 目标公司
    position = db.Column(db.String(100), nullable=True)  # 目标岗位
    question_types = db.Column(db.JSON, nullable=True)  # 问题类型
    result = db.Column(db.JSON, nullable=True)  # 生成结果
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


