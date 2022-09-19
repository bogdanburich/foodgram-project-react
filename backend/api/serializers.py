from django.contrib.auth import get_user_model
from recipes.models import Recipe, Ingredient, Tag, RecipeIngredients, Favorite, Cart
from users.serializers import CustomUserSerializer
from backend.settings import MEDIA_URL
from rest_framework import serializers

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


class RecipeSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def _get_request(self):
        return self.context.get('request')

    def get_image(self, obj):
        request = self.context.get('request')
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


class RecipeReadSerializer(RecipeSerializer):

    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'author', 'tags', 'name', 'image', 'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')


class RecipeWriteSerializer(RecipeSerializer):

    ingredients = AmountSerializer(many=True, write_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')

