import string
import random
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from blog import settings
from .models import UserProfile, Captcha
from .serializers import UserRegistrationSerializer, LoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    用户登录视图
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']

        # 获取用户头像
        try:
            profile = UserProfile.objects.get(user=user)
            profile_pic = profile.profile_pic.url if profile.profile_pic else None
        except UserProfile.DoesNotExist:
            profile_pic = None

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)


        response_data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile_pic': profile_pic,
            },
            'access':access_token, # JWT访问令牌
            'refresh':refresh_token, # JWT刷新令牌
            'message': '成功登录'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

    return Response({
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    用户注册视图
    """
    try:
        # print(f"收到注册请求: {request.data}")
        
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            # print("序列化器验证通过")
            user = serializer.save()
            # print(f"用户创建成功: {user.username}")
            
            # 返回用户信息
            response_data = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'message': '注册成功'
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        # print(f"序列化器验证失败: {serializer.errors}")
        # 验证失败，修正这里的错误
        return Response({
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        # print(f"注册过程中发生错误: {str(e)}")
        return Response({
            'error': f'服务器内部错误: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_captcha(request):
    email = request.data.get('email')
    if not email:
        return Response({
            'errors':'邮箱不能为空'
        }, status.HTTP_400_BAD_REQUEST)

    captcha = "".join(random.choices(string.digits, k=6))
    Captcha.objects.update_or_create(email=email, defaults={'captcha':captcha})

    try:
        subject = '验证码'
        message = f'您的验证码是：{captcha}，10分钟内有效。'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        print(f"生成的验证码: {captcha}")
        send_mail(subject, message, from_email, recipient_list)

        return Response({
            "message":'验证码发送成功'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'errors':f"发送失败{str(e)}"
        }, status=status.HTTP_400_BAD_REQUEST)