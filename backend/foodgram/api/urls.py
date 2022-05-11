from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, TagViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = (
    path('users/', include('users.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('tags/', include('tags.urls')),
    # path('ingredients/', include('ingredients.urls')),
    path('recipes/', include('recipes.urls')),
    path('', include(router.urls)))
