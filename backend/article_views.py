from django.db.models import Q, Prefetch, Count
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt

from .models import Article, Comment, Like, Dislike
from .serializers import ArticleSerializer


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
    article_queryset = Article.objects.all()
    if author_id:
        article_queryset = article_queryset.filter(author_id=author_id)

    total_count = article_queryset.count()
    posts = article_queryset.select_related(
        'author',
        'category',
        'author__backend_profile',
    ).prefetch_related(
        'tags',
        Prefetch('comments', queryset=Comment.objects.only('id'))
    ).annotate(
        comment_count=Count('comments', distinct=True),
    ).distinct()

    posts = posts[start:end]

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
        'comments_count': post.comment_count,
        'updated_time':post.updated_time.isoformat(),
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
        'title':post.title,
        'pub_time': post.pub_time.isoformat(),
        'views': post.views,
        'like_count': post.like_count,
        'dislike_count': post.dislike_count,
        'updated_time': post.updated_time,
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    try:
        post = Article.objects.get(id=post_id)
    except Article.DoesNotExist:
        return Response({
            'errors':'文章不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    post.delete()
    return Response({
        'success':True
    }, status=status.HTTP_200_OK)


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

    return Response({
        'results': post_list,
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'total_pages': (total_count + page_size - 1) // page_size,
    })