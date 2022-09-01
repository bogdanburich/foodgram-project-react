from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, subscribe, subscriptions

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', subscriptions),
    path('users/<int:pk>/subscribe/', subscribe),
    path('', include(router.urls)),
]
