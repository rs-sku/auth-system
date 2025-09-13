from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=128, null=False)
    email = models.CharField(max_length=128, null=False)
    password = models.CharField(max_length=128, null=False)
    is_active = models.BooleanField(default=True)
    status = models.ForeignKey(
        "Status",
        on_delete=models.CASCADE,
        default=1,
        related_name="users",
        related_query_name="status_by_user",
    )


class Right(models.Model):
    value = models.CharField(
        choices=[
            ("get", "Get method"),
            ("post", "Post method"),
            ("put", "Put method"),
            ("patch", "Patch method"),
            ("delete", "Delete method"),
            ("head", "Head method"),
            ("options", "Options method"),
        ],
        unique=True,
    )


class Status(models.Model):
    value = models.CharField(
        choices=[("default", "Base status"), ("admin", "Admin status")],
        default="Default",
        unique=True,
    )
    rights = models.ManyToManyField("Right", related_name="statuses")
