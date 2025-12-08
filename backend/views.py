"""
主视图文件 - 导入所有模块化视图
"""

# 导入所有模块化视图
from .auth_views import login, register, send_captcha
from .article_views import create_article, get_post, get_posts, get_my_posts, edit_post, delete_post, search_post
from .comment_views import get_comments, pub_comment
from .interaction_views import likes, dislikes
from .profile_views import my_profile, get_user_profile
from .category_views import get_categories, tags

# 导出所有视图函数
__all__ = [

    # 认证视图
    'login',
    'register',
    'send_captcha',
    
    # 文章视图
    'create_article',
    'get_post',
    'get_posts',
    'get_my_posts',
    'edit_post',
    'delete_post',
    'search_post',
    
    # 评论视图
    'get_comments',
    'pub_comment',
    
    # 互动视图
    'likes',
    'dislikes',
    
    # 用户资料视图
    'my_profile',
    'get_user_profile',
    
    # 分类和标签视图
    'get_categories',
    'tags',
]