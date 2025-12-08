from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Article, Like, Dislike


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