import string
import random

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q, Prefetch, Count
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt

from blog import settings
from .models import UserProfile, Category, Article, Comment, Like, Dislike, Captcha
from .serializers import UserRegistrationSerializer, LoginSerializer, ArticleSerializer, CommentSerializer, UserProfileSerializer


@api_view(['GET'])
def api_overview(request):
    """
    API概览
    """
    api_urls = {
        '概览': '/api/',
        '示例': '/api/example/',
    }
    return Response(api_urls)

@api_view(['GET'])
def example_api(request):
    """
    示例API端点
    """
    data = {
        'message': 'Hello from Django Backend!',
        'status': 'success',
        'data': {
            'project': 'Vue + Django Blog',
            'version': '1.0.0',
        }
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    用户登录视图
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        remember = serializer.validated_data['remember']
        # 记住我选项
        if remember:
            request.session.set_expiry(1209600)
        else:
            request.session.set_expiry(0)

        # 获取用户头像
        try:
            profile = UserProfile.objects.get(user=user)
            profile_pic = profile.profile_pic.url if profile.profile_pic else None
        except UserProfile.DoesNotExist:
            profile_pic = None
        
        # 这里可以生成token，暂时简化处理
        response_data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile_pic': profile_pic,
            },
            'token': 'simple-token-' + str(user.id),  # 简化的token，实际项目中应该用JWT
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
        print(f"收到注册请求: {request.data}")
        
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            print("序列化器验证通过")
            user = serializer.save()
            print(f"用户创建成功: {user.username}")
            
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
        
        print(f"序列化器验证失败: {serializer.errors}")
        # 验证失败，修正这里的错误
        return Response({
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        print(f"注册过程中发生错误: {str(e)}")
        return Response({
            'error': f'服务器内部错误: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def create_article(request):
    """
    发布文章
    """
    serializer = ArticleSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        article = serializer.save()

        response_data = {
            'article': {
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'category': article.category.category,
                'author': article.author.username,
                'pub_time': article.pub_time,
                'tags': [tag.tag for tag in article.tags.all()],
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    print(f"序列化器验证失败: {serializer.errors}")
    return Response({
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    category_list = [{"id":cat.id, 'name':cat.category} for cat in categories]
    return Response(category_list)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_post(request, post_id):
    """
    获取文章
    """
    try:
        post = Article.objects.get(id=post_id)
        post.views += 1
        post.save()
    except Article.DoesNotExist:
        return Response({'errors':'文章不存在'}, status=status.HTTP_404_NOT_FOUND)

    liked = False
    disliked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(article_id=post.id, user_id=request.user.id).exists()
        disliked = Dislike.objects.filter(article_id=post.id, user_id=request.user.id).exists()

    post_dict = {
        'author_id': post.author.id,
        'title': post.title,
        'content': post.content,
        'pub_time': post.pub_time.isoformat(),
        'author': post.author.username,
        'category': post.category.category,
        'views': post.views,
        'like_count': post.like_count,
        'dislike_count': post.dislike_count,
        'liked': liked,
        'disliked': disliked,
        'updated_time': post.updated_time,
        'profile_pic': post.author.backend_profile.profile_pic.url if post.author.backend_profile.profile_pic else None,
        'tags': [tag.tag for tag in post.tags.all()],
    }
    return Response(post_dict)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_posts(request):
    # 获取分页参数
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 16))
    author_id = request.query_params.get('author_id')

    # 分页查询
    start = (page - 1) * page_size
    end = start + page_size

    # 如果指定了author_id，则获取指定用户的文章
    if author_id:
        posts = Article.objects.filter(author_id=author_id)[start:end]
        total_count = Article.objects.filter(author_id=author_id).count()
    else:
        posts = Article.objects.all()[start:end]
        total_count = Article.objects.count()

    post_list = [{
        'id':post.id,
        'author': post.author.username,
        'title':post.title,
        'content': post.content[:150] + '...' if len(post.content) > 150 else  post.content,
        'pub_time': post.pub_time.isoformat(),
        'category': post.category.category,
        'views': post.views,
        'like_count': post.like_count,
        'dislike_count': post.dislike_count,
        'comments_count': post.comments.count(),
        'updated_time':post.updated_time,
        'profile_pic': post.author.backend_profile.profile_pic.url if post.author.backend_profile.profile_pic else None,
        'tags': [tag.tag for tag in post.tags.all()],
    } for post in posts]

    return Response({
        'results': post_list,
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'total_pages':(total_count + page_size - 1) // page_size,
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_comments(request, post_id):
    comments = Comment.objects.filter(article_id=post_id)
    comment_dict = [{
        'author_id':comment.author.id,
        'author': comment.author.username,
        'pub_time': comment.pub_time.isoformat(),
        'content': comment.content,
        'profile_pic':comment.author.backend_profile.profile_pic.url if comment.author.backend_profile.profile_pic else None,
    } for comment in comments]
    return Response(comment_dict)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pub_comment(request, post_id):
    serializer = CommentSerializer(data=request.data, context={'request': request, 'post_id': post_id})

    if serializer.is_valid():
        comment = serializer.save()

        response_data = {
            'comment': {
                'id': comment.id,
                'author': comment.author.username,
                'pub_time': comment.pub_time.isoformat(),
                'content': comment.content,
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response({
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def likes(request, post_id):
    try:
        post = Article.objects.get(id=post_id)
    except Article.DoesNotExist:
        return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        post.like_count += 1
        post.save()
        Like.objects.create(article_id=post.id, user_id=request.user.id)
        return Response({'likes':post.like_count}, status=status.HTTP_201_CREATED)
    else:
        post.like_count -= 1
        post.save()
        Like.objects.filter(article_id=post.id, user_id=request.user.id).delete()
        return Response({'likes':post.like_count}, status=status.HTTP_201_CREATED)

@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def dislikes(request, post_id):
    try:
        post = Article.objects.get(id=post_id)
    except Article.DoesNotExist:
        return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        post.dislike_count += 1
        post.save()
        Dislike.objects.create(article_id=post.id, user_id=request.user.id)
        return Response({'dislikes':post.dislike_count}, status=status.HTTP_201_CREATED)
    else:
        post.dislike_count -= 1
        post.save()
        Dislike.objects.filter(article_id=post.id, user_id=request.user.id).delete()
        return Response({'dislikes':post.dislike_count}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_posts(request):
    """
    获取自己的文章
    """
    # 获取分页参数
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 12))

    # 分页查询
    start = (page - 1) * page_size
    end = start + page_size

    posts = Article.objects.filter(author_id=request.user.id)[start:end]

    post_list = [{
        'id':post.id,
        'author': post.author.username,
        'title':post.title,
        'content': post.content[:150] + '...' if len(post.content) > 150 else  post.content,
        'pub_time': post.pub_time.isoformat(),
        'category': post.category.category,
        'views': post.views,
        'like_count': post.like_count,
        'dislike_count': post.dislike_count,
        'updated_time': post.updated_time,
        'tags': [tag.tag for tag in post.tags.all()],
    } for post in posts]

    # 返回分页信息
    total_count = Article.objects.filter(author_id=request.user.id).count()
    return Response({
        'results': post_list,
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'total_pages':(total_count + page_size - 1) // page_size,
    })

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def edit_post(request, post_id):
    try:
        post = Article.objects.get(id=post_id)
    except Article.DoesNotExist:
        return Response({'errors': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)

    # 检查编辑权限
    if post.author != request.user:
        return Response({'errors':'无权限编辑此文章'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        post_detail = {
            'id': post_id,
            'title': post.title,
            'content': post.content,
            'pub_time': post.pub_time.isoformat(),
            'category': post.category.category,
            'updated_time':post.updated_time,
            'tags': [tag.tag for tag in post.tags.all()],
            'tag_ids': [tag.id for tag in post.tags.all()],
        }
        return Response({'post':post_detail}, status=status.HTTP_200_OK)
    else:
        serializer = ArticleSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def my_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'GET':
        profile_detail = {
            'id': profile.id,
            'username': profile.user.username,
            'profile_pic': profile.profile_pic.url if profile.profile_pic else None,
            'introduction': profile.introduction,
            'birthday': profile.birthday,
            'created_at': profile.created_at,
        }
        return Response({'profile':profile_detail}, status=status.HTTP_200_OK)
    else:
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tags(request, category):
    try:
        tag_s = Category.objects.get(category=category).tags
    except Category.DoesNotExist:
        return Response({
            "errors":'分类不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    tags_list = [
        {
            'tag_id':tag.id,
            'tag':tag.tag,
        } for tag in tag_s
    ]
    return Response({'tags':tags_list}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def captcha(request):
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

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({
            "errors":"用户不存在"
        }, status=status.HTTP_404_NOT_FOUND)

    # 确保用户资料存在，不存在则创建
    user_detail = {
        'username': user.username,
        'profile_pic': user.backend_profile.profile_pic.url if user.backend_profile.profile_pic else None,
        'introduction': user.backend_profile.introduction if user.backend_profile.introduction else '',
        'birthday': user.backend_profile.birthday,
        'created_at': user.backend_profile.created_at,
    }
    return Response({'user':user_detail}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def search_post(request):
    main_keyword = request.query_params.get('keyword')
    category_id = request.query_params.get('category_id')
    order_by = request.query_params.get('order_by')

    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 16))

    start = (page - 1) * page_size
    end = start + page_size
    post_s = Article.objects

    if category_id:
        post_s = post_s.filter(category_id=category_id)

    if main_keyword:
        query = Q()
        keywords = main_keyword.split()
        for word in keywords:
            query |= Q(title__icontains=word) | Q(content__icontains=word) | Q(author__username__icontains=word) | Q(tags__tag__icontains=word)
        post_s = post_s.filter(query)


    # 使用select_related获取外键关联对象（一对一，一对多）
    # 使用prefetch_related获取多对多关联对象
    # 使用annotate预计算评论数量
    post_s = post_s.select_related(
        'author',  # 获取作者信息
        'category',  # 获取分类信息
        'author__backend_profile'  # 获取作者的个人资料
    ).prefetch_related(
        'tags',  # 预加载标签
        Prefetch('comments', queryset=Comment.objects.only('id'))  # 只加载评论ID用于计数
    ).annotate(
        comments_count=Count('comments', distinct=True)  # 预计算评论数
    ).distinct()  # 由于tags查询可能导致重复，使用distinct去重

    if order_by:
        post_s = post_s.order_by(order_by)

    total_count = post_s.count()
    # 先分页，再转换为列表
    paginated_posts = list(post_s[start:end])

    post_list = [
        {
        'id': post.id,
        'author': post.author.username,
        'title': post.title,
        'content': post.content[:150] + '...' if len(post.content) > 150 else post.content,
        'pub_time': post.pub_time.isoformat(),
        'category': post.category.category,
        'views': post.views,
        'like_count': post.like_count,
        'dislike_count': post.dislike_count,
        'comments_count': post.comments_count,
        'updated_time': post.updated_time.isoformat(),
        'profile_pic': post.author.backend_profile.profile_pic.url if post.author.backend_profile.profile_pic else None,
        'tags':[tag.tag for tag in post.tags.all()],
    } for post in paginated_posts]

    print(post_list)

    return Response({
        'results': post_list,
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'total_pages': (total_count + page_size - 1) // page_size,
    })