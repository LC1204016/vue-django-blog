"""
主视图文件 - 导入所有模块化视图
"""

# 导入所有模块化视图
from .auth_views import login, register, send_captcha, password_reset
from .article_views import ArticleDetail, ArticleList
from .comment_views import Comments
from .interaction_views import Likes, Dislikes
from .profile_views import UserProfilesView
from .category_views import get_categories, tags

# 导出所有视图函数
__all__ = [
    # 认证视图
    'login',
    'register',
    'send_captcha',
    'password_reset',
    
    # 文章视图
    'ArticleList',
    'ArticleDetail',

    # 评论视图
    'Comments',

    # 互动视图
    'Likes',
    'Dislikes',
    
    # 用户资料视图
    'UserProfilesView',
    
    # 分类和标签视图
    'get_categories',
    'tags',
]