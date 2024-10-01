import json

from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import Book
from datetime import datetime


def books_view(request):
    template = "books/books_list.html"
    data = Book.objects.all()
    return render(request, template, context={"books": data})


def books_on_date(request, dt):
    template = "books/pagi.html"

    content = Book.objects.filter(pub_date=dt)
    date = datetime.strftime(dt, "%d %b %Y")
    try:
        next = Book.objects.filter(pub_date__gt=dt).first().pub_date
        next = datetime.strftime(next, "%Y-%m-%d")
    except:
        next = None
    try:
        prev = Book.objects.filter(pub_date__lt=dt).last().pub_date
        prev = datetime.strftime(prev, "%Y-%m-%d")
    except:
        prev = None

    return render(
        request,
        template,
        context={"books": content, "date": date, "prev": prev, "next": next},
    )
