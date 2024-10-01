# coding=utf-8

from django.db import models
from django.contrib.postgres.indexes import BrinIndex


class Book(models.Model):
    name = models.CharField("Название", max_length=64)
    author = models.CharField("Автор", max_length=64)
    pub_date = models.DateField("Дата публикации")

    def __str__(self):
        return f"{self.name}  {self.author}"

    class Meta:
        indexes = (BrinIndex(fields=["pub_date"]),)
        ordering = ["pub_date"]
