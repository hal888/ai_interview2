from app import app

# 打印所有注册的路由
print("注册的路由：")
for rule in app.url_map.iter_rules():
    print(f"{rule}")
