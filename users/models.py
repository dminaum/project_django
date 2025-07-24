from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

