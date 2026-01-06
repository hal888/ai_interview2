import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import datetime
from functools import wraps
from flask import request, jsonify
from config import JWT_CONFIG

class JWTUtil:
    @staticmethod
    def generate_token(user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_CONFIG['access_token_expiry'])
        }
        return jwt.encode(payload, JWT_CONFIG['secret_key'], algorithm=JWT_CONFIG['algorithm'])
    
    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(
                token,
                JWT_CONFIG['secret_key'],
                algorithms=[JWT_CONFIG['algorithm']]
            )
            return payload['user_id']
        except ExpiredSignatureError:
            return None
        except InvalidTokenError:
            return None

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Missing authorization header'}), 401
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid authorization header format'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = JWTUtil.verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Attach user_id to request for downstream use
        request.user_id = user_id
        return f(*args, **kwargs)
    return decorated