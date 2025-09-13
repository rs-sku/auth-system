from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission

from auth_app.models import User


class AuthPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        if request.session.get("user_id") is None:
            return False
        return True


class AuthObjectPermission(AuthPermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if obj.id != request.session["user_id"]:
            raise PermissionDenied()
        return True


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        user_id = request.session.get("user_id")
        if user_id is None:
            return False
        user_obj = User.objects.get(pk=user_id)
        if user_obj.status.value != "admin":
            return False
        return True
