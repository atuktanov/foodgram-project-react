from django.urls import include, path

urlpatterns = (
    path('users/', include('users.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('tags/', include('tags.urls')),
    path('ingredients/', include('ingredients.urls')),
    path('recipes/', include('recipes.urls')))
