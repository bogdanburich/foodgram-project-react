from django.contrib import admin
from django.urls import include, path

BASE_API_URL = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{BASE_API_URL}/', include('users.urls')),
    path(f'{BASE_API_URL}/', include('api.urls')),
]
