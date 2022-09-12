from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Tag
from rest_framework import serializers

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeReadSerializer(serializers.ModelSerializer):

    class Meta:
        pass


class RecipeWriteSerializer(serializers.ModelSerializer):

    class Meta:
        pass
