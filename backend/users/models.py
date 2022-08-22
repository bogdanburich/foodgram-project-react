from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
        ('user', 'User'),
        ('admin', 'Admin')
    )


class User(AbstractUser):

    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_banned = models.BooleanField(default=False)
    role = models.CharField(choices=ROLES, max_length=1, default='user')

    REQUIRED_FIELDS = [
        'id',
        'username',
        'first_name',
        'last_name',
    ]
    USERNAME_FIELD = 'email'


class Follow(models.Model):

    author = models.ForeignKey(
        User,
        related_name='subscribers',
        on_delete=models.CASCADE
    )
    subscriber = models.ForeignKey(
        User,
        related_name='subscriptions',
        on_delete=models.CASCADE
    )
