import os
import django
from django.core.mail import send_mail
from django.conf import settings

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

def test_email():
    try:
        subject = '测试邮件'
        message = '这是一封测试邮件，如果你收到说明配置成功！'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['your-email@qq.com']  # 替换为你的邮箱
        
        print(f"发送邮件到: {recipient_list[0]}")
        print(f"使用配置: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        print(f"发件人: {from_email}")
        
        result = send_mail(subject, message, from_email, recipient_list)
        print(f"邮件发送结果: {result}")
        
        if result:
            print("✅ 邮件发送成功！")
        else:
            print("❌ 邮件发送失败")
            
    except Exception as e:
        print(f"❌ 邮件发送出错: {e}")

if __name__ == '__main__':
    test_email()