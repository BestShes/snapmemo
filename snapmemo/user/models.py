from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models


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
    username = models.EmailField(unique=True)
    password = models.CharField(blank=True, max_length=100)
    token = models.CharField(max_length=100)
    access_key = models.CharField(blank=True, max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

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
