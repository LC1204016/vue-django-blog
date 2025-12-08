from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .models import UserProfile, Article
from .serializers import UserProfileSerializer

class UserProfilesView(APIView):
    def get(self, request, user_id=None):
        if user_id is None:
            if not request.user.is_authenticated:
                return Response({
                    'errors':'未登录'
                }, status=status.HTTP_401_UNAUTHORIZED)
            user = request.user
            is_owner = True
        else:
            try:
                user = User.objects.get(id=user_id)
                is_owner = request.user.is_authenticated and request.user.id == int(user_id)
            except User.DoesNotExist:
                return Response({
                    'errors':'用户不存在'
                },status=status.HTTP_404_NOT_FOUND)

        user_detail = {
            'id': user.id,
            'username': user.username,
            'profile_pic':user.backend_profile.profile_pic.url if user.backend_profile.profile_pic else None,
            'introduction':user.backend_profile.introduction if user.backend_profile.introduction else '',
            'birthday': user.backend_profile.birthday,
            'created_at': user.backend_profile.created_at,
            'is_owner': is_owner,
        }

        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 12))
        start = (page - 1) * page_size
        end = start + page_size

        articles = Article.objects.filter(author_id=user.id)[start:end]
        article_list = [{
            'id': article.id,
            'title': article.title,
            'pub_time': article.pub_time.isoformat(),
            'views': article.views,
            'like_count': article.like_count,
            'dislike_count': article.dislike_count,
        } for article in articles]

        total_count = Article.objects.filter(author_id=user.id).count()

        return Response({
            'profile': user_detail,
            'results': article_list,
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size,
        }, status = status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def put(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({
                'errors':'用户不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile ,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

