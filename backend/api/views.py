from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS

from common.pagination import CustomPageNumberPagination
from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredients, Tag)

from .filters import IngredientFilter
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeShortSerializer, RecipeWriteSerializer,
                          TagSerializer)


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
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if self.request.query_params.get('is_favorited'):
            queryset = queryset.filter(favorited__user=user)

        if self.request.query_params.get('is_in_shopping_cart'):
            queryset = queryset.filter(carted__user=user)

        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = RecipeReadSerializer(
            instance=serializer.instance,
            context={'request': self.request}
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = RecipeReadSerializer(
            instance=serializer.instance,
            context={'request': self.request}
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
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
