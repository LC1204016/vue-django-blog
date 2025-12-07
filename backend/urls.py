from django.urls import path
from rest_framework_simplejwt.views import(
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('', views.api_overview, name='api-overview'),
    path('example/', views.example_api, name='example-api'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('pubposts/', views.create_article, name='create-article'),
    path('categories/', views.get_categories, name='get-category'),
    path('posts/<int:post_id>/', views.get_post, name='get-post'),
    path('getposts/', views.get_posts, name='get-posts'),
    path('comments/<int:post_id>/', views.get_comments, name='get-comments'),
    path("pubcomments/<int:post_id>/", views.pub_comment, name='pub-comment'),
    path("likes/<int:post_id>/", views.likes, name='likes'),
    path("dislikes/<int:post_id>/", views.dislikes, name='dislikes'),
    path('getmyposts/', views.get_my_posts, name='get-my-posts'),
    path('edit/<int:post_id>/', views.edit_post, name='edit-post'),
    path('tags/<str:category>/', views.tags, name='tags'),
    path('profile/', views.my_profile, name='my-profile'),
    path("captcha/", views.captcha, name='captcha'),
    path("profile/<int:user_id>/", views.get_user_profile, name='get-user-profile'),
    path('searchposts/', views.search_post, name='search-post'),
]
