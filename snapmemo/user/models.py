from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

from memo.models import Category
from snapmemo import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=UserManager.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        u = self.create_user(email=username,
                             password=password,
                             )
        u.is_superuser = True
        u.save(using=self._db)
        return u


class Member(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('normal', 'Normal'),
        ('facebook', 'Facebook'),
    )
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(blank=True, max_length=100)
    user_type = models.CharField(choices=USER_TYPE, default='normal', max_length=10)
    access_key = models.CharField(blank=True, max_length=260)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, through='MemberCategory')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class MemberCategory(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey(Category)
    created_date = models.DateTimeField(auto_now_add=True)
