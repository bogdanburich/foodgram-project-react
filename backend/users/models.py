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

    def get_shopping_list(self):
        cart = self.cart.all()
        carted_recipes = [item.recipe for item in cart]

        shopping_list = {}
        for recipe in carted_recipes:
            for recipe_ingredient in recipe.ingredients.all():
                name = recipe_ingredient.ingredient.name
                measurement_unit = (recipe_ingredient.ingredient.
                                    measurement_unit)
                if name in shopping_list:
                    shopping_list[f'{name}']['amount'] += (recipe_ingredient.
                                                           amount)
                else:
                    shopping_list[f'{name}'] = {
                        'amount': recipe_ingredient.amount,
                        'measurement_unit': measurement_unit
                    }
        return shopping_list


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
