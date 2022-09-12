from django.contrib.auth import get_user_model
from recipes.models import Recipe, Ingredient, Tag
from backend.settings import MEDIA_URL
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .fields import Base64ImageField

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class RecipeReadSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'author', 'tags', 'name', 'image', 'text', 'cooking_time')

    def get_image(self, obj):
        request = self.context.get('request')
        return f'{request.get_host()}{MEDIA_URL}{obj.image}'


class RecipeWriteSerializer(serializers.ModelSerializer):

    ingredients = AmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')

    def validate_ingredients(self, value):
        for ingredient in value:
            id = ingredient['id']
            if not Ingredient.objects.filter(id=id).exists():
                raise ValidationError(f'Tag with id {id} doesn\'t exist')
        return value
