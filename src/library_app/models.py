from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=128)


class Author(models.Model):
    name = models.CharField(max_length=128)
    books = models.ManyToManyField("Book", related_name="authors")
