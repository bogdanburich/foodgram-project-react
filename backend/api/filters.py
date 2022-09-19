from django_filters import rest_framework
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class IngredientFilter(SearchFilter):
    search_param = 'name'

    def get_search_fields(self, view, request):
        return ('^name',)
