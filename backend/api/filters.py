from django_filters import rest_framework
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class IngredientFilter(SearchFilter):
    search_param = 'name'

    def get_search_fields(self, view, request):
        return ('^name',)


class RecipeFilter(rest_framework.FilterSet):
    tags = rest_framework.CharFilter(field_name='tags__slug')
    author = rest_framework.CharFilter(field_name='author__id')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
