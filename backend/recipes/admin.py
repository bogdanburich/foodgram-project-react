from django.contrib import admin

from .models import Tag

admin.site.site_header = 'Foodgram Admin'
admin.site.register(Tag)
