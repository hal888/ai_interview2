import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 从.env文件读取邮件配置
def read_env():
    env = {}
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env[key] = value.strip()
    return env

# 测试邮件发送功能
def test_email_send():
    print("开始测试邮件发送功能...")
    
    # 读取配置
    env = read_env()
    
    # 提取邮件配置
    mail_server = env.get('MAIL_SERVER', 'smtp.163.com')
    mail_port = int(env.get('MAIL_PORT', '587'))
    mail_username = env.get('MAIL_USERNAME', '')
    mail_password = env.get('MAIL_PASSWORD', '')
    mail_use_tls = env.get('MAIL_USE_TLS', 'True').lower() == 'true'
    mail_default_sender = env.get('MAIL_DEFAULT_SENDER', '')
    
    # 测试邮件内容
    test_email = 'test_recipient@example.com'  # 替换为你的测试邮箱
    subject = 'AI面试助手 - 测试邮件'
    content = '这是一封测试邮件，用于验证邮件发送功能是否正常工作。'
    
    print(f"邮件服务器: {mail_server}")
    print(f"端口: {mail_port}")
    print(f"用户名: {mail_username}")
    print(f"使用TLS: {mail_use_tls}")
    print(f"发件人: {mail_default_sender}")
    print(f"测试收件人: {test_email}")
    
    try:
        # 创建SMTP连接
        if mail_use_tls:
            server = smtplib.SMTP(mail_server, mail_port)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(mail_server, mail_port)
        
        # 登录SMTP服务器
        server.login(mail_username, mail_password)
        print("成功登录SMTP服务器")
        
        # 创建邮件
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = Header(mail_default_sender, 'utf-8')
        msg['To'] = Header(test_email, 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 发送邮件
        server.sendmail(mail_default_sender, test_email, msg.as_string())
        print("邮件发送成功！")
        
        # 关闭连接
        server.quit()
        return True
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_email_send()
    if success:
        print("测试成功！邮件发送功能正常。")
        sys.exit(0)
    else:
        print("测试失败！邮件发送功能存在问题。")
        sys.exit(1)