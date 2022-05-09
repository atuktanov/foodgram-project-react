from django.contrib import admin

from .models import Ingredient, Measure


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    pass
