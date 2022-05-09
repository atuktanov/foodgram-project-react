from django.db import models


class Measure(models.Model):
    name = models.CharField(
        'Название', max_length=200, unique=True, blank=False, null=False)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['name'],
                name='unique_measure'),)
        ordering = ('-id',)
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название', max_length=200, unique=False, blank=False, null=False)
    measurement_unit = models.ForeignKey(
        Measure, on_delete=models.CASCADE, related_name='ingredients',
        verbose_name='Единица измерения', db_index=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'),)
        ordering = ('-id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'
