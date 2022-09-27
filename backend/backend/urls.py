from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

BASE_API_URL = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{BASE_API_URL}/', include('users.urls')),
    path(f'{BASE_API_URL}/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
