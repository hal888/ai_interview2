import requests
import json

# 测试登录API
print("测试登录API...")
login_url = "http://localhost:5000/api/auth/login"
login_data = {"userId": "test_user_123"}
headers = {"Content-Type": "application/json"}

try:
    login_response = requests.post(login_url, headers=headers, data=json.dumps(login_data), timeout=10)
    print(f"登录响应状态码: {login_response.status_code}")
    print(f"登录响应内容: {login_response.text}")
    
    if login_response.status_code == 200:
        # 获取token
        login_result = login_response.json()
        token = login_result.get("token")
        print(f"获取到的token: {token}")
        
        # 测试刷新token API
        print("\n测试刷新token API...")
        refresh_url = "http://localhost:5000/api/auth/refresh"
        refresh_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        refresh_response = requests.post(refresh_url, headers=refresh_headers, timeout=10)
        print(f"刷新token响应状态码: {refresh_response.status_code}")
        print(f"刷新token响应内容: {refresh_response.text}")
        
except Exception as e:
    print(f"测试过程中发生错误: {str(e)}")