from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
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
        db_index=True,
        unique=True
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex='^#(?:[0-9a-fA-F]{3}){1,2}$',
                message='Provided color code is invalid.'
            )
        ]
    )
    slug = models.SlugField(
        unique=True,
        db_index=True
    )
    recipe = models.ManyToManyField(
        'Recipe',
        db_index=True,
        related_name='tags',
        blank=True
    )

    def __str__(self):
        return self.name


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
    tag = models.ManyToManyField(
        Tag,
        db_index=True,
        related_name='recipes'
    )
    ingridient = models.ManyToManyField(
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


class Favorite(models.Model):
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


class Cart(models.Model):
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
