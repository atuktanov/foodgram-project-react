from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import Cart, Favorite, IngredientAmount, Recipe


class IngredientAmountInLine(admin.TabularInline):
    model = IngredientAmount
    raw_id_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'number_favorites')
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientAmountInLine,)
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}}

    def number_favorites(self, obj):
        return obj.favorites.count()
    number_favorites.short_description = 'Добавлений в избранное'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass
