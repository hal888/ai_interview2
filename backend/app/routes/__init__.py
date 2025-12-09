# 导出所有路由蓝图
from .resume import bp as resume_bp
from .self_intro import bp as self_intro_bp
from .question_bank import bp as question_bank_bp
from .mock_interview import bp as mock_interview_bp
from .strategy import bp as strategy_bp

# 重命名蓝图，便于在__init__.py中导入
resume = resume_bp
self_intro = self_intro_bp
question_bank = question_bank_bp
mock_interview = mock_interview_bp
strategy = strategy_bp
