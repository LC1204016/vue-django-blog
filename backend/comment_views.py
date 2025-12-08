from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Comment
from .serializers import CommentSerializer


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