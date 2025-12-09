from django.utils import timezone
import datetime
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile, Article, Category, Comment, Captcha

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember = serializers.BooleanField(default=False, required=False)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # 使用自定义认证后端，支持邮箱登录
            user = authenticate(email=email, password=password)
            
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("用户已被禁用")
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError('邮箱或密码错误')
        else:
            raise serializers.ValidationError('邮箱或密码不能为空')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, max_length=20)
    password_confirm = serializers.CharField(write_only=True)
    captcha = serializers.CharField(max_length=6,min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'captcha']

    def validate(self, data):
        # 验证邮箱唯一
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("邮箱已经被注册")

        captcha_obj = Captcha.objects.filter(email=data['email']).first()
        if not captcha_obj or data['captcha'] != captcha_obj.captcha:
            raise serializers.ValidationError('验证码错误')

        # 检查验证码是否过期（10分钟）
        if captcha_obj.created_at < timezone.now() - datetime.timedelta(minutes=10):
            raise serializers.ValidationError('验证码已过期')

        # 验证用户名唯一性
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('用户已经存在')

        # 验证密码正确
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('密码不匹配')

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)

        # 使用create_user而不是create，这样密码会自动哈希
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        UserProfile.objects.create(user=user)

        return user

class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=5, max_length=30)
    content = serializers.CharField(min_length=5)
    category = serializers.CharField()
    tags = serializers.StringRelatedField(many=True, read_only=True)
    tag_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Article
        fields = ['title', 'content', 'category','tags', 'tag_ids']

    def validate_category(self, value):
        if not Category.objects.filter(category=value).exists():
            raise serializers.ValidationError(f"分类 '{value}' 不存在")
        return value

    def validate(self, data):
        title = data.get('title')
        # 获取当前实例（如果是更新操作）
        instance = getattr(self, 'instance', None)

        # 检查标题唯一性（排除当前文章
        queryset = Article.objects.filter(title=title)
        if instance and instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

        if queryset.exists():
            raise serializers.ValidationError('文章已存在')

        return data

    def create(self, validated_data):
        # 提取tag_ids，然后从validated_data中移除
        tag_ids = validated_data.pop('tag_ids', [])
        category_name = validated_data.pop('category')

        category_id = Category.objects.get(category=category_name)

        article = Article.objects.create(
            author=self.context['request'].user,
            category=category_id,
            **validated_data
        )

        # 设置tags关联关系
        if tag_ids:
            article.tags.set(tag_ids)

        return article

    def update(self, instance, validated_data):
        # 提取tag_ids，然后从validated_data中移除
        tag_ids = validated_data.pop('tag_ids', None)

        if 'category' in validated_data:
            category_name = validated_data.pop('category')
            category_id = Category.objects.get(category=category_name)
            validated_data['category'] = category_id

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if tag_ids is not None:
            instance.tags.set(tag_ids)
        return instance

class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(min_length=5, max_length=300)

    class Meta:
        model = Comment
        fields = ['content']

    def create(self, validated_data):
        article_id = self.context.get('article_id')
        comment_obj = Comment.objects.create(
            author=self.context['request'].user,
            content=validated_data['content'],
            article_id=article_id
        )

        return comment_obj

class UserProfileSerializer(serializers.ModelSerializer):
    introduction = serializers.CharField(max_length=30, required=False, allow_blank=True)
    birthday = serializers.DateField(required=False, allow_null=True)
    profile_pic = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ['introduction', 'birthday', 'profile_pic']

    def update(self, instance, validated_data):
        # 更新UserProfile字段
        instance.introduction = validated_data.get('introduction', instance.introduction)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        
        # 处理头像上传
        if 'profile_pic' in validated_data:
            if validated_data['profile_pic'] is None:
                # 如果明确设置为None，保持当前头像
                pass
            else:
                # 更新头像
                instance.profile_pic = validated_data['profile_pic']
        
        instance.save()
        return instance

    def to_representation(self, instance):
        """修改返回数据格式，确保头像URL正确"""
        data = super().to_representation(instance)
        if instance.profile_pic:
            # 确保头像URL是完整的URL路径
            if not instance.profile_pic.url.startswith('http'):
                data['profile_pic'] = f"http://localhost:8000{instance.profile_pic.url}"
        return data

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6, max_length=20)
    password_confirm = serializers.CharField(write_only=True)
    captcha = serializers.CharField(max_length=6, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'captcha']

    def validate(self, data):
        if not User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("用户不存在")

        captcha_obj = Captcha.objects.filter(email=data['email']).first()
        if not captcha_obj or data['captcha'] != captcha_obj.captcha:
            raise serializers.ValidationError('验证码错误')

        # 检查验证码是否过期（10分钟）
        if captcha_obj.created_at < timezone.now() - datetime.timedelta(minutes=10):
            raise serializers.ValidationError('验证码已过期')

        # 验证密码正确
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('密码不匹配')

        return data

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return user