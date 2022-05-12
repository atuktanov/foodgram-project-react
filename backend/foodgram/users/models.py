from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.expressions import F
from django.db.models.query_utils import Q


class User(AbstractUser):
    email = models.EmailField('Email адрес', max_length=254, unique=True)
    username = models.CharField(
        'Юзернейм', max_length=150,
        validators=(RegexValidator(
            regex=r'^[\w.@+-]+$',
            message=('Поле может содержать только буквы латинского алфавита, '
                     'цифры и символы _.@+-')),), unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)

    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribers',
        verbose_name='Автор')
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='authors',
        verbose_name='Подписчик')

    def clean(self):
        if self.subscriber == self.author:
            raise ValidationError('Нельзя подписываться на себя')

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'subscriber'),
                name='unique_subscription'),
            models.CheckConstraint(
                check=~Q(subscriber=F('author')),
                name='dont_subscribe_yourself'))
        ordering = ('-id',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.subscriber} подписан на {self.author}'
