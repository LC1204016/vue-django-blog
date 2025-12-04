from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class SimpleTokenAuthentication(BaseAuthentication):
    """
    简单的token认证类
    """
    def authenticate(self, request):
        # 从请求头获取token
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
            
        try:
            # 解析Bearer token
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None
                
            # 简单的token验证（实际项目中应该更安全）
            if token.startswith('simple-token-'):
                user_id = token.split('-')[-1]
                try:
                    user = User.objects.get(id=int(user_id))
                    return (user, token)
                except User.DoesNotExist:
                    raise AuthenticationFailed('无效的token')
            else:
                return None
                
        except (ValueError, IndexError):
            raise AuthenticationFailed('无效的token格式')
    
    def authenticate_header(self, request):
        return 'Bearer'