from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from .models import Comment
from .serializers import CommentSerializer


class Comments(APIView):
    @permission_classes([AllowAny])
    def get(self, request, article_id):
        comments = Comment.objects.filter(article_id=article_id)
        comment_dict = [{
            'author_id': comment.author.id,
            'author': comment.author.username,
            'pub_time': comment.pub_time.isoformat(),
            'content': comment.content,
            'profile_pic': comment.author.backend_profile.profile_pic.url if comment.author.backend_profile.profile_pic else None,
        } for comment in comments]
        return Response(comment_dict)

    @permission_classes([IsAuthenticated])
    def post(self, request, article_id):
        serializer = CommentSerializer(data=request.data, context={'request': request, 'article_id': article_id})

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