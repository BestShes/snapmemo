from django.db import models
from snapmemo import settings


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)


class Memo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=250, blank=True)
    image = models.ImageField(blank=True)
