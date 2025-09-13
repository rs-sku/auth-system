from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from auth_app.models import Right, Status, User
from auth_app.permissions import AdminPermission, AuthObjectPermission
from auth_app.serializers import (
    LoginSerializer,
    RightSerializer,
    StatusSerializer,
    UserSerializer,
)
from auth_app.usecases import logout


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AuthObjectPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logout(request.session)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class LoginView(APIView):
    def post(self, request) -> Response:
        serializer = LoginSerializer()
        data = serializer.validate(request.data)
        user = data.get("user")
        request.session["user_id"] = user.id
        return Response("You are logged in", status=status.HTTP_201_CREATED)


class LogOutView(APIView):
    def post(self, request) -> Response:
        if not logout(request.session):
            msg = "User did not log in"
        else:
            msg = "You are logged out"
        return Response(msg, status=status.HTTP_202_ACCEPTED)


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [AdminPermission]


class RightViewSet(ModelViewSet):
    queryset = Right.objects.all()
    serializer_class = RightSerializer
    permission_classes = [AdminPermission]
