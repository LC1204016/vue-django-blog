from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from .models import UserProfile
from .serializers import UserProfileSerializer


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