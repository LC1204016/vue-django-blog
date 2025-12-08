from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    支持邮箱登录的认证后端
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # 支持邮箱登录
            user = User.objects.get(email=email)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            return None
        
        return None