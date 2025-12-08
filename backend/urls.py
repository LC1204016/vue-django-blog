from django.urls import path
from . import views

urlpatterns = [
    # 认证相关
    path('auth/login/', views.login, name='login'),
    path('auth/register/', views.register, name='register'),
    path('captcha/', views.send_captcha, name='send-captcha'),
    
    # 文章相关
    path('pubposts/', views.create_article, name='create-article'),
    path('getposts/', views.get_posts, name='get-posts'),
    path('posts/<int:post_id>/', views.get_post, name='get-post'),
    path('getmyposts/', views.get_my_posts, name='get-my-posts'),
    path('edit/<int:post_id>/', views.edit_post, name='edit-post'),
    path('deletepost/<int:post_id>/', views.delete_post, name='delete-post'),
    path('searchposts/', views.search_post, name='search-post'),
    
    # 分类和标签相关
    path('categories/', views.get_categories, name='get-categories'),
    path('tags/<str:category>/', views.tags, name='tags'),
    
    # 评论相关
    path('comments/<int:post_id>/', views.get_comments, name='get-comments'),
    path('pubcomments/<int:post_id>/', views.pub_comment, name='pub-comment'),
    
    # 互动功能
    path('likes/<int:post_id>/', views.likes, name='likes'),
    path('dislikes/<int:post_id>/', views.dislikes, name='dislikes'),
    
    # 用户资料相关
    path('profile/', views.my_profile, name='my-profile'),
    path('profile/<int:user_id>/', views.get_user_profile, name='get-user-profile'),
]
