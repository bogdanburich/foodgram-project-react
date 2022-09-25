from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_banned', 'role', 'recipes_count')
    search_fields = ('email', 'username', 'role')
    list_filter = ('email', 'username', 'is_banned', 'role')
    empty_value_display = '-empty-'

admin.site.register(User, UserAdmin)
admin.site.register(Follow)
