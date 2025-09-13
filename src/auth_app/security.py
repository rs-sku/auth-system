from functools import wraps

from rest_framework.exceptions import PermissionDenied

from auth_app.models import Status, User


def admin_protection(model: User):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request):
            user_obj = (
                model.objects.select_related("status")
                .filter(pk=request.session["user_id"])
                .first()
            )
            if user_obj.status.value != "admin":
                raise PermissionDenied()
            result = func(self, request)
            return result

        return wrapper

    return decorator


def right_protection(model: Status):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request):
            status_obj = (
                model.objects.prefetch_related("rights")
                .filter(status_by_user__id=request.session["user_id"])
                .first()
            )
            right_obj = status_obj.rights.all()
            rights = [right.value for right in right_obj]
            if request.method.lower() not in rights:
                raise PermissionDenied()
            return func(self, request)

        return wrapper

    return decorator
