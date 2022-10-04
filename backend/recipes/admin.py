from django.contrib import admin

from .models import Cart, Favorite, Ingredient, Recipe, RecipeIngredients, Tag

admin.site.site_header = 'Foodgram Admin'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fields = ('name', 'measurement_unit')
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name', 'measurement_unit')
    empty_value_display = '-empty-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name', 'color', 'slug')
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')
    empty_value_display = '-empty-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ('name', 'image', 'text', 'cooking_time', 'author',
              'favorited_count')
    readonly_fields = ('favorited_count',)
    list_display = ('name', 'author', 'favorited_count')
    search_fields = ('name',)
    list_filter = ('author', 'tags')
    empty_value_display = '-empty-'


admin.site.register(RecipeIngredients)
admin.site.register(Favorite)
admin.site.register(Cart)
