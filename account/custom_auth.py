from .models import User
from rest_framework import authentication
from rest_framework import exceptions



class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        # print(request.META.keys())
        if not username:
            return None

        try:
            user = User.objects.get(name=username)
            if user.is_admin:
                return (user, None)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return None