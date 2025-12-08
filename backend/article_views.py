from django.db.models import Q, Prefetch, Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .models import Article, Comment, Like, Dislike
from .serializers import ArticleSerializer


class ArticleList(APIView):
    @permission_classes([AllowAny])
    def get(self, request):
        """
        获取文章
        """
        # 获取分页参数
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 16))
        author_id = request.query_params.get('author_id')
        
        # 获取搜索、排序和分类参数
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        category = request.query_params.get('category')

        # 分页查询
        start = (page - 1) * page_size
        end = start + page_size

        # 基础查询
        article_queryset = Article.objects.all()
        
        # 如果指定了author_id，则获取指定用户的文章
        if author_id:
            article_queryset = article_queryset.filter(author_id=author_id)
            
        # 如果指定了分类，则筛选该分类的文章
        if category:
            article_queryset = article_queryset.filter(category_id=category)
            
        # 如果指定了搜索关键词，则进行搜索
        if search:
            query = Q()
            keywords = search.split()
            for word in keywords:
                query |= Q(title__icontains=word) | Q(content__icontains=word) | Q(author__username__icontains=word) | Q(tags__tag__icontains=word)
            article_queryset = article_queryset.filter(query)

        # 应用排序
        if ordering:
            article_queryset = article_queryset.order_by(ordering)

        total_count = article_queryset.count()
        
        # 优化查询
        articles = article_queryset.select_related(
            'author',
            'category',
            'author__backend_profile',
        ).prefetch_related(
            'tags',
            Prefetch('comments', queryset=Comment.objects.only('id'))
        ).annotate(
            comment_count=Count('comments', distinct=True),
        ).distinct()

        articles = articles[start:end]

        article_list = [{
            'id': article.id,
            'author': article.author.username,
            'title': article.title,
            'content': article.content[:150] + '...' if len(article.content) > 150 else article.content,
            'pub_time': article.pub_time.isoformat(),
            'category': article.category.category,
            'views': article.views,
            'like_count': article.like_count,
            'dislike_count': article.dislike_count,
            'comments_count': article.comment_count,
            'updated_time': article.updated_time.isoformat(),
            'profile_pic': article.author.backend_profile.profile_pic.url if article.author.backend_profile.profile_pic else None,
            'tags': [tag.tag for tag in article.tags.all()],
        } for article in articles]

        return Response({
            'results': article_list,
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size,
        })

    @permission_classes([IsAuthenticated])
    def post(self, request):
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


class ArticleDetail(APIView):
    @permission_classes([AllowAny])
    def get(self, request, pk):
        """
            获取文章
            """
        try:
            article = Article.objects.get(id=pk)
            article.views += 1
            article.save()
        except Article.DoesNotExist:
            return Response({'errors': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)

        liked = False
        disliked = False
        if request.user.is_authenticated:
            liked = Like.objects.filter(article_id=article.id, user_id=request.user.id).exists()
            disliked = Dislike.objects.filter(article_id=article.id, user_id=request.user.id).exists()

        article_dict = {
            'author_id': article.author.id,
            'title': article.title,
            'content': article.content,
            'pub_time': article.pub_time.isoformat(),
            'author': article.author.username,
            'category': article.category.category,
            'views': article.views,
            'like_count': article.like_count,
            'dislike_count': article.dislike_count,
            'liked': liked,
            'disliked': disliked,
            'updated_time': article.updated_time,
            'profile_pic': article.author.backend_profile.profile_pic.url if article.author.backend_profile.profile_pic else None,
            'tags': [tag.tag for tag in article.tags.all()],
        }
        return Response(article_dict)

    @permission_classes([IsAuthenticated])
    def put(self, request, pk):
        try:
            article = Article.objects.get(id=pk)
        except Article.DoesNotExist:
            return Response({'errors': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)

        # 检查编辑权限
        if article.author != request.user:
            return Response({'errors': '无权限编辑此文章'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        try:
            article = Article.objects.get(id=pk)
        except Article.DoesNotExist:
            return Response({
                'errors': '文章不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        article.delete()
        return Response({
            'success': True
        }, status=status.HTTP_200_OK)