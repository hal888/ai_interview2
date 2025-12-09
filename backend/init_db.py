#!/usr/bin/env python3
"""
数据库初始化脚本
创建数据库和表结构
"""

import os
import sys
import pymysql
from config import DB_CONFIG

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from app.models import db

def create_database():
    """创建数据库"""
    try:
        # 连接到MySQL服务器（不指定数据库）
        conn = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset=DB_CONFIG['charset']
        )
        cursor = conn.cursor()
        
        # 创建数据库（如果不存在）
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET {DB_CONFIG['charset']} COLLATE utf8mb4_unicode_ci;")
        print(f"数据库 {DB_CONFIG['database']} 创建成功或已存在")
        
        # 关闭连接
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"创建数据库失败: {e}")
        return False

def init_tables():
    """创建表结构"""
    try:
        with app.app_context():
            # 导入模型
            from app.models import InterviewStrategy, Resume, SelfIntro, QuestionBank, MockInterview, User
            
            # 删除所有表（如果存在）
            db.drop_all()
            
            # 重新创建所有表
            db.create_all()
            print("所有表创建成功")
            return True
    except Exception as e:
        print(f"创建表结构失败: {e}")
        return False

def main():
    """主函数"""
    print("开始初始化数据库...")
    
    # 1. 创建数据库
    if create_database():
        # 2. 创建表结构
        init_tables()
    
    print("数据库初始化完成")

if __name__ == "__main__":
    main()
