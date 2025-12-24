from flask import Blueprint, request, jsonify
from ..models import db, User
from ..utils.jwt_utils import JWTUtil

# 创建蓝图
bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    """用户登录API"""
    data = request.get_json()
    user_id = data.get('userId')
    
    if not user_id:
        return jsonify({"error": "userId is required"}), 400
    
    # 现有模式：get or create
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        user = User(user_id=user_id)
        db.session.add(user)
        db.session.commit()
    
    # 生成JWT token
    token = JWTUtil.generate_token(user.id)
    return jsonify({"token": token, "userId": user_id}), 200

@bp.route('/refresh', methods=['POST'])
def refresh_token():
    """刷新JWT token API"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Invalid authorization header"}), 401
    
    token = auth_header.split(' ')[1]
    user_id = JWTUtil.verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    # 生成新token
    new_token = JWTUtil.generate_token(user_id)
    return jsonify({"token": new_token}), 200