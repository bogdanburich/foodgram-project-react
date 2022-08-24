from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = router.urls
