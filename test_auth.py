import requests
import time
import json

# 测试配置
BASE_URL = 'http://localhost:5000/api'
TEST_EMAIL = f'test_{int(time.time())}@example.com'
TEST_PASSWORD = 'Test@12345'
NEW_PASSWORD = 'NewTest@12345'

def test_register():
    """测试注册功能"""
    print("测试注册功能...")
    
    # 1. 发送验证码
    print(f"1. 向邮箱 {TEST_EMAIL} 发送验证码")
    response = requests.post(f'{BASE_URL}/auth/send-verification-code', json={'email': TEST_EMAIL})
    print(f"   发送验证码响应: {response.status_code} - {response.json()}")
    
    # 2. 注册用户（这里需要手动输入验证码，所以跳过实际注册）
    print("2. 注册用户: 请手动在前端页面进行注册测试")
    
    return True

def test_login():
    """测试登录功能"""
    print("\n测试登录功能...")
    
    # 登录请求
    login_data = {
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD
    }
    
    print(f"1. 使用邮箱 {TEST_EMAIL} 和密码 {TEST_PASSWORD} 登录")
    response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
    print(f"   登录响应: {response.status_code} - {response.json()}")
    
    if response.status_code == 200:
        token = response.json().get('token')
        print(f"   获取到的令牌: {token}")
        return token
    else:
        print("   登录失败")
        return None

def test_refresh_token(token):
    """测试刷新令牌功能"""
    if not token:
        print("\n跳过刷新令牌测试: 没有有效的令牌")
        return None
    
    print("\n测试刷新令牌功能...")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.post(f'{BASE_URL}/auth/refresh', headers=headers)
    print(f"   刷新令牌响应: {response.status_code} - {response.json()}")
    
    if response.status_code == 200:
        new_token = response.json().get('token')
        print(f"   获取到的新令牌: {new_token}")
        return new_token
    else:
        print("   刷新令牌失败")
        return None

def test_request_reset_password():
    """测试请求重置密码功能"""
    print("\n测试请求重置密码功能...")
    
    response = requests.post(f'{BASE_URL}/auth/request-reset-password', json={'email': TEST_EMAIL})
    print(f"   请求重置密码响应: {response.status_code} - {response.json()}")
    
    return response.status_code == 200

def main():
    """主测试函数"""
    print("开始测试用户认证系统...")
    print("=" * 50)
    
    # 测试注册功能
    test_register()
    
    # 测试登录功能
    token = test_login()
    
    # 测试刷新令牌功能
    test_refresh_token(token)
    
    # 测试请求重置密码功能
    test_request_reset_password()
    
    print("\n" + "=" * 50)
    print("测试完成！请手动测试以下功能：")
    print("1. 注册流程（包括验证码发送和验证）")
    print("2. 登录流程（包括记住我功能）")
    print("3. 密码重置流程（包括重置链接发送和密码更新）")
    print("4. 前端页面的表单验证和错误提示")
    print("5. 密码强度提示功能")
    print("6. 验证码倒计时功能")
    
    print(f"\n测试邮箱: {TEST_EMAIL}")
    print(f"测试密码: {TEST_PASSWORD}")
    print(f"新密码: {NEW_PASSWORD}")

if __name__ == "__main__":
    main()