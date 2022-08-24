from recipes.models import Ingredient, Tag
from rest_framework import viewsets

from .serializers import IngredientsSerializer, TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
