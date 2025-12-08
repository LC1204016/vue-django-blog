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
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.tag
    
    @property
    def categories(self):
        """获取该标签所属的所有分类"""
        try:
            return [ct.category for ct in self.category_tags.all()]
        except:
            return []

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
    description = models.TextField(blank=True, help_text="分类描述")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category
    
    @property
    def tags(self):
        """获取该分类下的所有标签"""
        return [ct.tag for ct in self.category_tags.all()]
    
    def add_tag(self, tag_name):
        """为分类添加标签"""
        tag, created = Tag.objects.get_or_create(tag=tag_name)
        CategoryTag.objects.get_or_create(category=self, tag=tag)
        return tag
    
    def remove_tag(self, tag_name):
        """从分类中移除标签"""
        try:
            tag = Tag.objects.get(tag=tag_name)
            category_tag = CategoryTag.objects.get(category=self, tag=tag)
            category_tag.delete()
            return True
        except (Tag.DoesNotExist, CategoryTag.DoesNotExist):
            return False

# 分类-标签关联模型
class CategoryTag(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='category_tags')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('category', 'tag')
        verbose_name = '分类标签'
        verbose_name_plural = '分类标签'

    def __str__(self):
        return f"{self.category.category} - {self.tag.tag}"

class Captcha(models.Model):
    captcha = models.CharField(max_length=6)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now=True)
