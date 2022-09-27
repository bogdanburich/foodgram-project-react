from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from backend.settings import MEDIA_URL
from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredients, Tag)
from users.models import Follow

from .pagination import RecipeLimitPagination

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AmountWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')
        extra_kwargs = {
            'id': {
                'read_only': False
            }
        }


class RecipeSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def _get_request(self):
        return self.context.get('request')

    def get_image(self, obj):
        request = self._get_request()
        return f'{request.get_host()}{MEDIA_URL}{obj.image}'

    def get_is_favorited(self, obj):
        user = self._get_request().user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self._get_request().user
        if user.is_authenticated:
            return Cart.objects.filter(user=user, recipe=obj).exists()
        return False


class RecipeShortSerializer(RecipeSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Follow.objects.filter(subscriber=request.user, author=obj).exists()
        return False


class SubscriptionUserSerialzier(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = Recipe.objects.filter(author=obj)
        paginator = RecipeLimitPagination()
        page = paginator.paginate_queryset(recipes, request)
        serializer = RecipeShortSerializer(page, many=True, read_only=True, context={'request': request})
        return serializer.data


class RecipeReadSerializer(RecipeSerializer):

    tags = TagSerializer(many=True, read_only=True)
    ingredients = AmountReadSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'author', 'tags', 'name', 'image', 'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')


class RecipeWriteSerializer(RecipeSerializer):

    ingredients = AmountWriteSerializer(many=True, write_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')

    def _add_ingredients_and_tags(self, instance, validated_data):
        ingredients, tags = (
            validated_data.pop('ingredients'), validated_data.pop('tags')
        )
        for ingredient in ingredients:
            count_of_ingredient, _ = RecipeIngredients.objects.get_or_create(
                ingredient=get_object_or_404(Ingredient, pk=ingredient['id']),
                amount=ingredient['amount'],
            )
            instance.ingredients.add(count_of_ingredient)
        instance.tags.set(tags)
        return instance

    def create(self, validated_data):
        saved = {}
        saved['ingredients'] = validated_data.pop('ingredients')
        saved['tags'] = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        return self._add_ingredients_and_tags(recipe, saved)

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        instance = self._add_ingredients_and_tags(instance, validated_data)
        return super().update(instance, validated_data)
