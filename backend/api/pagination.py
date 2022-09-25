from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class RecipeLimitPagination(LimitOffsetPagination):
    limit_query_param = 'recipes_limit'
    offset_query_param = None
