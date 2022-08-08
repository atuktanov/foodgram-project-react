# Продуктовый помощник


![foodgram workflow](https://github.com/atuktanov/foodgram-project-react/workflows/foodgram_workflow/badge.svg)
  
Сайт (социальная сеть) для публикации кулинарных рецептов, с возможностью подписываться на публикации других авторов, добавлять рецепты в избранное и
список покупок. Список покупок дает возможность скачать список продуктов, необходимых для приготовления добавленных блюд.

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Над проектом работали](#над-проектом-работали)

## Технологии
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Nginx](https://nginx.org/)
- [Gunicorn](https://gunicorn.org/)
- [Docker](https://www.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Yandex.Cloud](https://cloud.yandex.ru/)

## Использование
На вашем сервере должен быть установлен docker и docker-compose
  
Скопируйте из папки infra в рабочую папку проекта файлы docker-compose.yml и nginx.conf, также скопируйте и переименуйте файл .env.template в .env (этот файл содержит шаблон заполнения .env) 
Отредакетируйте nginx.conf и .env в соответствии с параметрами своего сервера

Пример заполнения .env файла
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=j#@2yv698sb@#x=pq4b!^=4ap1!$b7xgpgv3fbpc5@9017!5jx
```

Запустите контейнеры
```
sudo docker-compose up -d
```
Примените миграции
```
sudo docker-compose exec backend python manage.py migrate
```
Cоздайте суперпользователя
```
sudo docker-compose exec backend python manage.py createsuperuser
```
Cоберите статику
```
sudo docker-compose exec backend python manage.py collectstatic
```
Загрузите в БД данные по ингредиентам
``` 
sudo docker-compose exec backend python manage.py load_data
```
Создайте через админ зону необходимые теги.

После этого проект будет доступен для пользователей

## Над проектом работали

- [Алексей Туктанов](https://t.me/atuktanov) - Backend
- [Яндекс.Практикум](https://github.com/yandex-praktikum/foodgram-project-react) - Frontend
