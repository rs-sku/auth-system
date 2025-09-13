from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.models import Status, User
from auth_app.permissions import AuthPermission
from auth_app.security import admin_protection, right_protection
from library_app.models import Author, Book


class BooksView(APIView):
    permission_classes = [AuthPermission]

    @right_protection(Status)
    def get(self, request) -> Response:
        books_obj = Book.objects.prefetch_related("authors").all()
        resp = {}
        for book in books_obj:
            authors = set()
            for author in book.authors.all():
                authors.add(author.name)
            resp[book.name] = authors
        return Response(resp)


class AuthorsView(APIView):
    permission_classes = [AuthPermission]

    @admin_protection(User)
    def get(self, request) -> Response:
        author_obj = Author.objects.prefetch_related("books").all()
        resp = {}
        for author in author_obj:
            books = set()
            for book in author.books.all():
                books.add(book.name)
            resp[author.name] = books
        return Response(resp)
