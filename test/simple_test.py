#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
sys.path.append(r'D:\dev\blog')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from backend.models import Category, Article
from rest_framework import status

class SimpleArticleTest(TestCase):
    def setUp(self):
        # 添加testserver到ALLOWED_HOSTS
        from django.conf import settings
        settings.ALLOWED_HOSTS.append('testserver')
        
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # 创建测试分类
        self.category = Category.objects.create(
            category='技术',
            description='技术相关文章'
        )
        
        self.client = Client()
    
    def test_basic_flow(self):
        # 1. 测试登录
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        print(f"登录状态码: {response.status_code}")
        if response.status_code == 200:
            token = response.json()['access']
            print(f"获取令牌成功")
            
            # 2. 设置认证头
            self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'
            
            # 3. 测试创建文章
            data = {
                'title': '测试文章',
                'content': '测试文章内容',
                'category': '技术'  # 使用分类名称
            }
            response = self.client.post('/api/pubposts/', data, content_type='application/json')
            print(f"创建文章状态码: {response.status_code}")
            print(f"响应内容: {response.content.decode()}")
            
            if response.status_code == 201:
                print("文章创建成功！")
            else:
                print("文章创建失败")
        else:
            print(f"登录失败: {response.content.decode()}")

# 运行测试
if __name__ == '__main__':
    import unittest
    unittest.main()