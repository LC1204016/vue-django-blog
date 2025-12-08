#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
sys.path.append(r'D:\dev\blog')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from backend.models import Category

# 创建测试客户端
client = Client()

# 创建或获取测试用户
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()

# 登录获取token
response = client.post('/api/auth/login/', {
    'email': 'test@example.com',
    'password': 'testpass123'
})

print(f"登录响应状态码: {response.status_code}")
print(f"登录响应内容: {response.content.decode()}")

if response.status_code == 200:
    token = response.json()['access']
    print(f"获取到令牌: {token}")
    
    # 设置认证头
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    
    # 获取分类
    categories = Category.objects.all()
    print(f"可用分类: {[(c.id, c.category) for c in categories]}")
    
    if categories:
        # 尝试创建文章
        data = {
            'title': '测试文章',
            'content': '测试文章内容',
            'category': categories[0].category
        }
        
        response = client.post('/api/pubposts/', data)
        print(f"\n创建文章响应状态码: {response.status_code}")
        print(f"创建文章响应内容: {response.content.decode()}")
else:
    print("登录失败，无法继续测试")