from django.contrib import admin
from django.urls import path, register_converter

from books import converters
from books.views import books_view, books_on_date

register_converter(converters.DateConverter, "date")

urlpatterns = [
    path("books/", books_view, name="books"),
    path("books/<date:dt>/", books_on_date),
    path("admin/", admin.site.urls),
]
