from django.db import models
from django.urls import reverse


# Create your models here.


class Author(models.Model):
    fullname = models.CharField()
    born_date = models.CharField()
    born_location = models.CharField()
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    tag = models.CharField()


class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


