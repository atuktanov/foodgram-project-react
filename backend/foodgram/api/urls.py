from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = (
    path('users/', include('users.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)))
