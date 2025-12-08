from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Article, Like, Dislike
from rest_framework.views import APIView

class Likes(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, post_id):
        try:
            post = Article.objects.get(id=post_id)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)

        post.like_count += 1
        post.save()
        Like.objects.create(article_id=post.id, user_id=request.user.id)
        return Response({'likes': post.like_count}, status=status.HTTP_201_CREATED)

    @permission_classes([IsAuthenticated])
    def delete(self, request, post_id):
        try:
            post = Article.objects.get(id=post_id)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)

        post.like_count -= 1
        post.save()
        Like.objects.filter(article_id=post.id, user_id=request.user.id).delete()
        return Response({'likes': post.like_count}, status=status.HTTP_201_CREATED)

class Dislikes(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, post_id):
        try:
            post = Article.objects.get(id=post_id)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)
        post.dislike_count += 1
        post.save()
        Dislike.objects.create(article_id=post.id, user_id=request.user.id)
        return Response({'dislikes': post.dislike_count}, status=status.HTTP_201_CREATED)

    @permission_classes([IsAuthenticated])
    def delete(self, request, post_id):
        try:
            post = Article.objects.get(id=post_id)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)

        post.dislike_count -= 1
        post.save()
        Dislike.objects.filter(article_id=post.id, user_id=request.user.id).delete()
        return Response({'dislikes':post.dislike_count}, status=status.HTTP_201_CREATED)