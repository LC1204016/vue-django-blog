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
from backend.models import Category, Article, Comment
from rest_framework import status

class CommentTest(TestCase):
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
        
        # 创建测试文章
        self.article = Article.objects.create(
            title='测试文章标题',
            content='测试文章内容',
            author=self.user,
            category=self.category
        )
        
        self.client = Client()
    
    def test_comment_creation(self):
        # 1. 登录
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        print(f"登录状态码: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json()['access']
            self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'
            
            # 2. 创建评论
            data = {
                'content': '测试评论内容'
            }
            response = self.client.post(f'/api/pubcomments/{self.article.id}/', data, content_type='application/json')
            print(f"创建评论状态码: {response.status_code}")
            print(f"响应内容: {response.content.decode()}")
            
            if response.status_code == 201:
                print("评论创建成功！")
            else:
                print("评论创建失败")

# 运行测试
if __name__ == '__main__':
    import unittest
    unittest.main()