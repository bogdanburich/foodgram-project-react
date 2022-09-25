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
    role = models.CharField(choices=ROLES, default='user', max_length=10)

    REQUIRED_FIELDS = [
        'id',
        'username',
        'first_name',
        'last_name',
    ]
    USERNAME_FIELD = 'email'

    @property
    def recipes_count(self):
        return self.recipes.aggregate(models.Count('id'))['id__count']

    def __str__(self):
        return f'{self.username}'


class Follow(models.Model):

    author = models.ForeignKey(
        User,
        related_name='subscriber',
        on_delete=models.CASCADE
    )
    subscriber = models.ForeignKey(
        User,
        related_name='subscription',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.author} - {self.subscriber}'
