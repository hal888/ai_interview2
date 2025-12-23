# 配置文件
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取项目根目录的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# DeepSeek API配置
DEEPSEEK_CONFIG = {
    "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
    "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
    "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
}

# 数据库配置
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "ai_interview_db"),
    "charset": os.getenv("DB_CHARSET", "utf8mb4"),
    "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
    "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10"))
}

# SQLAlchemy配置
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset={DB_CONFIG['charset']}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = DB_CONFIG['pool_size']
SQLALCHEMY_MAX_OVERFLOW = DB_CONFIG['max_overflow']

# 简历保存路径配置
RESUME_CONFIG = {
    "base_path": os.getenv("RESUME_BASE_PATH", os.path.join(BASE_DIR, "resumes")),
    "original_path": os.getenv("RESUME_ORIGINAL_PATH", "original"),
    "optimized_path": os.getenv("RESUME_OPTIMIZED_PATH", "optimized")
}