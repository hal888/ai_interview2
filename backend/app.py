# 导入app包中定义的应用实例
from app import app

if __name__ == '__main__':
    app.run(debug=False, port=5000)
