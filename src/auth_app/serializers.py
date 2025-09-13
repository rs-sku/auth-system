from django.contrib.auth import authenticate
from rest_framework import serializers

from auth_app.models import Right, Status, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "email",
            "password",
            "repeat_password",
            "status",
        ]
        read_only_fields = ["id", "is_active"]

    def create(self, validated_data: dict) -> User:
        if validated_data["password"] != validated_data["repeat_password"]:
            msg = "Password does not match"
            raise serializers.ValidationError(msg, code="authorization")
        validated_data.pop("repeat_password")
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user or not user.is_active:
                msg = "Unable to log in with provided credentials"
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = "Must include username and password"
            raise serializers.ValidationError(msg, code="authorization")

        data["user"] = user
        return data


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "value", "rights"]
        read_only_fields = ["id"]


class RightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Right
        fields = ["id", "value", "statuses"]
        read_only_fields = ["id"]
