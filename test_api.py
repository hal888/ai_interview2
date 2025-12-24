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
        
        # 测试简历分析API
        print("\n测试简历分析API...")
        analyze_url = "http://localhost:5000/api/resume/analyze"
        analyze_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "multipart/form-data"
        }
        
        files = {
            "file": open("test_resume.pdf", "rb")
        }
        
        analyze_response = requests.post(analyze_url, headers={"Authorization": f"Bearer {token}"}, files=files, timeout=120)
        print(f"简历分析响应状态码: {analyze_response.status_code}")
        print(f"简历分析响应内容: {analyze_response.text}")
        
except Exception as e:
    print(f"测试过程中发生错误: {str(e)}")