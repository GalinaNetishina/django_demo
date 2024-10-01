from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=30)
    birth_date = models.DateField(
        null=True,
    )


class Course(models.Model):

    name = models.CharField(max_length=30)

    students = models.ManyToManyField(
        Student,
        blank=True,
    )
