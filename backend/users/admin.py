from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'recipes_count')
    search_fields = ('email', 'username', 'role')
    list_filter = ('email', 'username', 'role')
    empty_value_display = '-empty-'


admin.site.register(Follow)
