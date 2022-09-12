from recipes.models import Ingredient, Recipe, RecipeIngredients, Tag
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def __create_ingredients(self, recipe, ingredients):
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
            self.__create_ingredients(recipe, ingredients)

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
