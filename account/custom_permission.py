from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from .models import User

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        return request.method in SAFE_METHODS


class NameCharPermission(BasePermission):

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        # print(request.user.name)
        if request.user.name.startswith("j"):
            return True
        return False