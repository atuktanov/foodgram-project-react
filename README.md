![foodgram workflow](https://github.com/atuktanov/foodgram-project-react/workflows/foodgram_workflow/badge.svg)
# Продуктовый помощник
### Описание:
Сайт (социальная сеть) для публикации кулинарных рецептов, с возможностью подписываться на публикации других авторов, добавлять рецепты в избранное и
список покупок. Список покупок дает возможность скачать список продуктов, необходимых для приготовления добавленных блюд.

### Стек технологий: 
Python, Django, Django REST Framework, PostgreSQL, Nginx, Gunicorn, Docker, GitHub Actions, Яндекс.Облако

### Запуск проекта на собственном сервере:
На сервере должен быть установлен docker и docker-compose

Скопировать из папки infra в рабочую папку проекта файлы docker-compose.yml и nginx.conf, также скопировать и переименовать файл .env.template в .env (этот файл содержит шаблон заполнения .env) 
Отредакетировать nginx.conf и .env в соответствии с параметрами своего сервера

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

Запустить контейнеры
```
sudo docker-compose up -d
```
Применить миграции
```
sudo docker-compose exec backend python manage.py migrate
```
Cоздать суперпользователя
```
sudo docker-compose exec backend python manage.py createsuperuser
```
Cобрать статику
```
sudo docker-compose exec backend python manage.py collectstatic
```
Загрузить в БД данные по ингредиентам
``` 
sudo docker-compose exec backend python manage.py load_data
```
Создать через админ зону необходимые теги.

После этого проект будет доступен для пользователей

### Авторы:
[atuktanov](https://github.com/atuktanov) - Backend  
[Яндекс.Практикум](https://github.com/yandex-praktikum/foodgram-project-react) - Frontend
