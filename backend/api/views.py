from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from common.pagination import CustomPageNumberPagination
from recipes.models import Cart, Ingredient, Recipe, RecipeIngredients, Tag, Favorite
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, RecipeShortSerializer, TagSerializer)
from .filters import IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def _create_ingredients(self, recipe, ingredients):
        for ingredient in ingredients:
            ingredient_obj = Ingredient.objects.get(id=ingredient['id'])
            amount = ingredient['amount']
            RecipeIngredients.objects.create(
                recipe=recipe, ingredient=ingredient_obj, amount=amount
            )

    def create(self, request, *args, **kwargs):
        serializer = RecipeWriteSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            ingredients = serializer.validated_data.pop('ingredients')
            tags = serializer.validated_data.pop('tags')
            author = self.request.user

            recipe = Recipe.objects.create(
                author=author, **serializer.validated_data
            )
            recipe.tags.set(tags)
            ingredients = self._create_ingredients(recipe, ingredients)

            serializer = RecipeReadSerializer(
                instance=recipe,
                context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['POST', 'DELETE'], name='favorite', url_path='favorite', url_name='favorite')
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = Favorite.objects.filter(user=user, recipe=recipe)

        if request.method == 'POST':
            if not favorite.exists():
                Favorite.objects.create(user=user, recipe=recipe)
                serializer = RecipeShortSerializer(
                    instance=recipe,
                    context={'request': request}
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            raise ValidationError(f'Recipe {recipe} is already in favorite.')

        if favorite.exists():
            favorite.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        raise ValidationError(f'Recipe {recipe} is not in favorite.')

    @action(detail=True,
            methods=['POST', 'DELETE'],
            name='shopping-cart',
            url_path='shopping_cart',
            url_name='shopping_cart')
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        cart = Cart.objects.filter(user=user, recipe=recipe)

        if request.method == 'POST':
            if not cart.exists():
                Cart.objects.create(user=user, recipe=recipe)
                serializer = RecipeShortSerializer(
                    instance=recipe,
                    context={'request': request}
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            raise ValidationError(f'Recipe {recipe} is already in cart.')

        if cart.exists():
            cart.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        raise ValidationError(f'Recipe {recipe} is not in in cart.')
