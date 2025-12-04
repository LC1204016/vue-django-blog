import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 用户信息
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='backend_profile')
    introduction = models.TextField(max_length=30, blank=True)
    birthday = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username}的资料"

# 文章
class Article(models.Model):
    title = models.CharField(max_length=30) # 标题
    content = models.TextField() # 内容
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE) # 作者
    category = models.ForeignKey('Category', on_delete=models.CASCADE) # 分类
    pub_time = models.DateTimeField(auto_now_add=True) # 发布时间
    updated_time = models.DateTimeField(auto_now=True) # 更新时间
    views = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', related_name='articles')

    class Meta:
        ordering = ['-pub_time']

class Tag(models.Model):
    tag = models.CharField(max_length=10, unique=True)

# 点赞情况
class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'article'),)

# 不喜欢情况
class Dislike(models.Model):
    user = models.ForeignKey(User, related_name='dislikes', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='dislikes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'article'),)

# 评论
class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)

# 分类
class Category(models.Model):
    category = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.category

class Captcha(models.Model):
    captcha = models.CharField(max_length=6)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
