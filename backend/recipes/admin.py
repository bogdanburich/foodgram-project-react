from django.contrib import admin

from .models import Ingredient, Tag

admin.site.site_header = 'Foodgram Admin'
admin.site.register(Tag)
admin.site.register(Ingredient)
