from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if exc.__class__.__name__ == "PermissionDenied":
            response.data = {
                "detail": "You do not have permission to perform this action"
            }
            response.status_code = status.HTTP_403_FORBIDDEN
        elif exc.__class__.__name__ == "NotAuthenticated":
            response.data = {"detail": "Authentication credentials were not provided"}
            response.status_code = status.HTTP_401_UNAUTHORIZED

    return response
