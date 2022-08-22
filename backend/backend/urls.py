from django.contrib import admin
from django.urls import include, path

BASE_API_URL = 'api'

urlpatterns = [
    path(r'^admin/', admin.site.urls),
    path(rf'{BASE_API_URL}/', include('users.urls'))
]
