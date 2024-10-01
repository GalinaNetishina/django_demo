from django.db import models
from django.contrib.postgres.indexes import BrinIndex


class Tag(models.Model):

    name = models.CharField(max_length=50, verbose_name="тег", unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    text = models.TextField(verbose_name="Текст")
    published_at = models.DateTimeField(verbose_name="Дата публикации")
    image = models.ImageField(
        null=True,
        blank=True,
        verbose_name="Изображение",
    )
    tags = models.ManyToManyField(Tag, through="Scope")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-published_at"]
        indexes = (BrinIndex(fields=["published_at"]),)

    def __str__(self):
        return f"{self.title}"


class Scope(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="scopes"
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="scopes")
    is_main = models.BooleanField()

    class Meta:
        ordering = ["-is_main", "tag"]
