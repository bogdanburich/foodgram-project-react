from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        unique=True
    )
    measurement_unit = models.CharField(
        max_length=200
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


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

    class Meta:
        ordering = ['name']


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
    ingredients = models.ManyToManyField(
        'RecipeIngredients',
        related_name='recipes'
    )
    author = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.SET_DEFAULT,
        related_name='recipes',
        default=None
    )
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    @property
    def favorited_count(self):
        return self.favorited.aggregate(models.Count('id'))['id__count']

    class Meta:
        ordering = ['-date_added']


class RecipeIngredients(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='amount_in_recipes'
    )
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Recipe Ingredients'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='favorited'
    )
    user = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Cart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='carted'
    )
    user = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    def __str__(self):
        return f'{self.user} - {self.recipe}'
