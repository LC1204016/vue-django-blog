from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Category


@api_view(['GET'])
def get_categories(request):
    category_list = cache.get('category_list')

    if category_list is None:
        categories = Category.objects.all()
        category_list = [{"id": cat.id, 'name': cat.category} for cat in categories]
        cache.set('category_list', category_list)

    return Response(category_list, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def tags(request, category):
    cache_key = f'category_tags:{category}'

    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(cached_data, status=status.HTTP_200_OK)

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
    response_data = {'tags':tags_list}

    cache.set(cache_key, response_data, 60*30)

    return Response(response_data, status=status.HTTP_200_OK)