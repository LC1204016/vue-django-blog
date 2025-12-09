from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Article, Like, Dislike
from rest_framework.views import APIView

class Likes(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, article_id):
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)

        article.like_count += 1
        article.save()
        Like.objects.create(article_id=article_id, user_id=request.user.id)
        return Response({'likes': article.like_count}, status=status.HTTP_201_CREATED)

    @permission_classes([IsAuthenticated])
    def delete(self, request, article_id):
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)

        article.like_count -= 1
        article.save()
        Like.objects.filter(article_id=article_id, user_id=request.user.id).delete()
        return Response({'likes': article.like_count}, status=status.HTTP_201_CREATED)

class Dislikes(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, article_id):
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)
        article.dislike_count += 1
        article.save()
        Dislike.objects.create(article_id=article_id, user_id=request.user.id)
        return Response({'dislikes': article.dislike_count}, status=status.HTTP_201_CREATED)

    @permission_classes([IsAuthenticated])
    def delete(self, request, article_id):
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)

        article.dislike_count -= 1
        article.save()
        Dislike.objects.filter(article_id=article_id, user_id=request.user.id).delete()
        return Response({'dislikes':article.dislike_count}, status=status.HTTP_201_CREATED)