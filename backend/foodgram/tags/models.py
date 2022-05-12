from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField(
        'Цвет', validators=[RegexValidator(
            regex=r'^#[\dABCDEF]{6}$', message=('цвет задается НЕХ кодом'))],
        max_length=7)
    slug = models.SlugField(
        'Slug', unique=True, max_length=200)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
