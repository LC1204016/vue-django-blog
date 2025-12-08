"""
Django 后端测试框架
提供单元测试、集成测试和性能测试功能
"""
import json
import random
import string
from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import UserProfile, Article, Category, Comment, Like, Dislike, Captcha
from .serializers import UserRegistrationSerializer, ArticleSerializer


class BaseTestCase(APITestCase):
    """测试基类，提供通用的测试工具和方法"""
    
    def setUp(self):
        """测试前的初始化"""
        # 设置测试客户端
        self.client = Client()
        # 添加testserver到ALLOWED_HOSTS以避免DisallowedHost错误
        from django.conf import settings
        if 'testserver' not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.append('testserver')
        # 创建测试分类
        self.category1 = Category.objects.create(
            category="技术",
            description="技术相关文章"
        )
        self.category2 = Category.objects.create(
            category="生活",
            description="生活相关文章"
        )
        
        # 创建测试用户
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # 创建用户资料
        UserProfile.objects.create(user=self.user1, introduction="测试用户1")
        UserProfile.objects.create(user=self.user2, introduction="测试用户2")
        
        # 创建测试文章
        self.article1 = Article.objects.create(
            title="测试文章1",
            content="这是测试文章1的内容",
            author=self.user1,
            category=self.category1
        )
        self.article2 = Article.objects.create(
            title="测试文章2",
            content="这是测试文章2的内容",
            author=self.user2,
            category=self.category2
        )
    
    def generate_random_string(self, length=10):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def generate_random_email(self):
        """生成随机邮箱"""
        return f"{self.generate_random_string(8)}@example.com"
    
    def authenticate_user(self, user):
        """用户认证并获取token"""
        response = self.client.post('/api/auth/login/', {
            'email': user.email,
            'password': 'testpass123'
        })
        if response.status_code == 200:
            token = response.data['access']
            # 使用APITestClient的方法设置认证头
            self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'
            return token
        return None


class AuthenticationTestCase(BaseTestCase):
    """认证系统测试"""
    
    def test_user_registration_valid(self):
        """测试有效用户注册"""
        # 先创建验证码
        from backend.models import Captcha
        email = self.generate_random_email()
        captcha = Captcha.objects.create(email=email, captcha='123456')
        
        data = {
            'username': self.generate_random_string(8),
            'email': email,
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'captcha': '123456'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=data['username']).exists())
    
    def test_user_registration_invalid_email(self):
        """测试无效邮箱注册"""
        email = 'invalid-email'
        captcha = Captcha.objects.create(email=email, captcha='123456')
        
        data = {
            'username': self.generate_random_string(8),
            'email': email,
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'captcha': '123456'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_registration_password_mismatch(self):
        """测试密码不匹配"""
        email = self.generate_random_email()
        captcha = Captcha.objects.create(email=email, captcha='123456')
        
        data = {
            'username': self.generate_random_string(8),
            'email': email,
            'password': 'testpass123',
            'password_confirm': 'differentpass',
            'captcha': '123456'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login_valid(self):
        """测试有效用户登录"""
        response = self.client.post('/api/auth/login/', {
            'email': 'test1@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_user_login_invalid_password(self):
        """测试无效密码登录"""
        response = self.client.post('/api/auth/login/', {
            'email': 'test1@example.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login_nonexistent_user(self):
        """测试不存在用户登录"""
        response = self.client.post('/api/auth/login/', {
            'email': 'nonexistent@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_token_refresh(self):
        """测试令牌刷新"""
        # 先登录
        response = self.client.post('/api/auth/login/', {
            'email': 'test1@example.com',
            'password': 'testpass123'
        })
        refresh_token = response.data['refresh']
        
        # 刷新令牌
        response = self.client.post('/api/token/refresh/', {
            'refresh': refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class ArticleTestCase(BaseTestCase):
    """文章系统测试"""
    
    def test_get_articles_list(self):
        """测试获取文章列表"""
        response = self.client.get('/api/getposts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)  # 至少有2篇文章
    
    def test_get_article_detail(self):
        """测试获取文章详情"""
        response = self.client.get(f'/api/posts/{self.article1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.article1.title)
    
    def test_create_article_authenticated(self):
        """测试认证用户创建文章"""
        self.authenticate_user(self.user1)
        data = {
            'title': '新文章标题',
            'content': '新文章内容',
            'category': self.category1.category  # 使用分类名称而不是ID
        }
        response = self.client.post('/api/pubposts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Article.objects.filter(title='新文章标题').exists())
    
    def test_create_article_unauthenticated(self):
        """测试未认证用户创建文章"""
        data = {
            'title': '新文章',
            'content': '新文章内容',
            'category': self.category1.id
        }
        response = self.client.post('/api/pubposts/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_article_owner(self):
        """测试文章作者更新文章"""
        self.authenticate_user(self.user1)
        data = {
            'title': '更新的文章',
            'content': '更新的内容',
            'category': self.category1.category
        }
        response = self.client.put(f'/api/edit/{self.article1.id}/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article1.refresh_from_db()
        self.assertEqual(self.article1.title, '更新的文章')
    
    def test_update_article_non_owner(self):
        """测试非作者更新文章"""
        self.authenticate_user(self.user2)
        data = {
            'title': '更新的文章',
            'content': '更新的内容',
            'category': self.category1.id
        }
        response = self.client.put(f'/api/edit/{self.article1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_search_articles_by_keyword(self):
        """测试按关键词搜索文章"""
        response = self.client.get('/api/searchposts/', {'keyword': '测试'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_search_articles_by_category(self):
        """测试按分类搜索文章"""
        response = self.client.get('/api/searchposts/', {'category_id': self.category1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 搜索API返回的数据结构是 {'results': [...], ...}
        for article in response.data.get('results', []):
            self.assertEqual(article['category'], self.category1.category)


class CommentTestCase(BaseTestCase):
    """评论系统测试"""
    
    def test_get_comments(self):
        """测试获取文章评论"""
        response = self.client.get(f'/api/comments/{self.article1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_comment_authenticated(self):
        """测试认证用户创建评论"""
        self.authenticate_user(self.user1)
        data = {
            'content': '测试评论内容'
        }
        response = self.client.post(f'/api/pubcomments/{self.article1.id}/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(content='测试评论内容').exists())
    
    def test_create_comment_unauthenticated(self):
        """测试未认证用户创建评论"""
        data = {
            'content': '测试评论'
        }
        response = self.client.post(f'/api/pubcomments/{self.article1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class InteractionTestCase(BaseTestCase):
    """互动功能测试"""
    
    def test_like_article(self):
        """测试点赞文章"""
        self.authenticate_user(self.user1)
        response = self.client.post(f'/api/likes/{self.article1.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.user1, article=self.article1).exists())
    
    def test_unlike_article(self):
        """测试取消点赞"""
        self.authenticate_user(self.user1)
        # 先点赞
        self.client.post(f'/api/likes/{self.article1.id}/')
        # 再取消点赞
        response = self.client.delete(f'/api/likes/{self.article1.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # API返回201而不是204
        self.assertFalse(Like.objects.filter(user=self.user1, article=self.article1).exists())
    
    def test_dislike_article(self):
        """测试踩文章"""
        self.authenticate_user(self.user1)
        response = self.client.post(f'/api/dislikes/{self.article1.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Dislike.objects.filter(user=self.user1, article=self.article1).exists())
    
    def test_like_own_article(self):
        """测试点赞自己的文章"""
        self.authenticate_user(self.user1)
        response = self.client.post(f'/api/likes/{self.article1.id}/')
        # 应该允许点赞自己的文章
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserProfileTestCase(BaseTestCase):
    """用户资料测试"""
    
    def test_get_own_profile(self):
        """测试获取自己的资料"""
        self.authenticate_user(self.user1)
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile']['username'], 'testuser1')
    
    def test_get_other_profile(self):
        """测试获取他人资料"""
        response = self.client.get(f'/api/profile/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser2')
    
    def test_update_own_profile(self):
        """测试更新自己的资料"""
        self.authenticate_user(self.user1)
        data = {
            'introduction': '更新后的简介'
        }
        response = self.client.put('/api/profile/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile = UserProfile.objects.get(user=self.user1)
        self.assertEqual(profile.introduction, '更新后的简介')


class BoundaryTestCase(BaseTestCase):
    """边界条件测试"""
    
    def test_long_article_title(self):
        """测试超长文章标题"""
        self.authenticate_user(self.user1)
        long_title = 'a' * 100  # 超过30个字符的限制
        data = {
            'title': long_title,
            'content': '测试内容',
            'category': self.category1.id
        }
        response = self.client.post('/api/pubposts/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_empty_article_title(self):
        """测试空文章标题"""
        self.authenticate_user(self.user1)
        data = {
            'title': '',
            'content': '测试内容',
            'category': self.category1.id
        }
        response = self.client.post('/api/pubposts/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_short_password(self):
        """测试过短密码"""
        data = {
            'username': self.generate_random_string(8),
            'email': self.generate_random_email(),
            'password': '123',
            'password2': '123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_duplicate_username(self):
        """测试重复用户名"""
        data = {
            'username': 'testuser1',  # 已存在的用户名
            'email': self.generate_random_email(),
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_nonexistent_article(self):
        """测试不存在的文章"""
        response = self.client.get('/api/posts/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_nonexistent_category(self):
        """测试不存在的分类"""
        self.authenticate_user(self.user1)
        data = {
            'title': '测试文章',
            'content': '测试内容',
            'category': 99999  # 不存在的分类ID
        }
        response = self.client.post('/api/pubposts/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ErrorHandlingTestCase(BaseTestCase):
    """错误处理测试"""
    
    def test_database_connection_error(self):
        """测试数据库连接错误处理"""
        # 这里可以模拟数据库连接错误
        pass
    
    def test_invalid_json_request(self):
        """测试无效JSON请求"""
        response = self.client.post(
            '/api/auth/login/',
            data='invalid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_missing_required_fields(self):
        """测试缺少必需字段"""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser1'
            # 缺少password字段
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


if __name__ == '__main__':
    import unittest
    unittest.main()