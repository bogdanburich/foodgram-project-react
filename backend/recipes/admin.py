from django.contrib import admin

from .models import Ingredient, Tag

admin.site.site_header = 'Foodgram Admin'

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name', 'measurement_unit')
    empty_value_display = '-empty-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')
    empty_value_display = '-empty-'

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
