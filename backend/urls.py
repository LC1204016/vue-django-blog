from django.urls import path
from . import views

urlpatterns = [
    # 认证相关
    path('auth/login/', views.login, name='login'),
    path('auth/register/', views.register, name='register'),
    path('captcha/', views.send_captcha, name='send-captcha'),
    path('password/reset/', views.password_reset, name='password_reset'),
    
    # 文章相关
    path('articles/', views.ArticleList.as_view(), name='articles'),
    path('articles/<int:pk>/', views.ArticleDetail.as_view(), name='article-detail'),

    # 分类和标签相关
    path('categories/', views.get_categories, name='get-categories'),
    path('tags/<str:category>/', views.tags, name='tags'),
    
    # 评论相关
    path('articles/<int:article_id>/comments/', views.Comments.as_view(), name='Comments'),

    # 互动功能
    path('likes/<int:post_id>/', views.Likes.as_view(), name='likes'),
    path('dislikes/<int:post_id>/', views.Dislikes.as_view(), name='dislikes'),
    
    # 用户资料相关
    path('users/profile/', views.UserProfilesView.as_view(), name='my-profile'),
    path('users/<int:user_id>/profile/', views.UserProfilesView.as_view(), name='other-profile'),
]
