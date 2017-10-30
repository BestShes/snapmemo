from django.db import models
from snapmemo import settings


def memo_directory_path(instance, filename):
    return 'image/user_{0}/{1}'.format(instance.user_id, filename)


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)


class Memo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000, blank=True)
    image = models.ImageField(blank=True, upload_to=memo_directory_path)
