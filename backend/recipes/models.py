from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True
    )
    measurement_unit = models.CharField(
        max_length=200
    )


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True
    )
    color = models.CharField(
        max_length=7,
    )
    slug = models.SlugField(
        unique=True,
        db_index=True
    )


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True
    )
    image = models.FileField()
    text = models.TextField()
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        related_name='recipes'
    )
    ingridients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        related_name='recipes'
    )
    author = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.SET_DEFAULT,
        related_name='recipes',
        default=None
    )


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        db_index=True,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        db_index=True,
        on_delete=models.PROTECT
    )
    amount = models.IntegerField()


class Favorites(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        db_index=True,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='favorites'
    )


class Carts(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        db_index=True,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='cart'
    )
