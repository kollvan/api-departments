# api-departments
---
api-departments - api интерфейс для модификации, удаления и добавления записей.

Пример испльзования api в postmen.<br>
![example](https://github.com/kollvan/api-departments/blob/master/assets/example.png?raw=true)

## Содержание
---
- [Технологии](#-технологии)
- [Использование](#-использование)
- [Настройка окружения](#-настройка-окружения)


## Технологии
---
- [python](https://docs.python.org/3/)
- [postgresql](https://www.postgresql.org/docs/)
- [django](https://docs.djangoproject.com/en/5.2/)
- [drf](https://www.django-rest-framework.org/)
- [docker](https://www.docker.com/)


## Использование
---
Для работы приложения необходимо настроить окружение (подробнее см. [[#Настройка окружения]]).
Отдельный запуск приложения.
```shell
python manage.py runserver
```

Запуск в docker.
Приложение запускается на порту 8000.
```shell
docker compose up
```

## Настройка окружения
---
Для запуске приложения необходим файл `.env` содержащий переменные среды.
Создание файла:
```shell
touch .env
```

### Список используемых переменных

| Переменная        | Описание                                                                                                                                                                                                                                        | Обязательная     | Пример      |
|-------------------| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |-------------|
| DJANGO_SECRET_KEY | Секретный ключ, используемый для криптографический операций [django secret_key](https://docs.djangoproject.com/en/6.0/ref/settings/#std-setting-SECRET_KEY) Генерируется с помощью функции `django.core.management.utils.get_random_secret_key` | Да               | -           |
| DJANGO_DEBUG      | Режим запуска приложения [django debug](https://docs.djangoproject.com/en/6.0/ref/settings/#debug) Если переменная не задана, то приложение запускается в режиме debug.                                                                         | Нет              | True/False  |
| DB_HOST           | Хост на котором расположен СУБД postgresql. При запуске через docker compose должна принимать значение psdb.                                                                                                                                    | Да               | psdb        |
| DB_PORT           | Порт для доступа к субд postgresql                                                                                                                                                                                                              | Да               | 5432        |
| DB_NAME           | Имя создаваемой базы данных в postgresql.                                                                                                                                                                                                       | Да               | departments |
| DB_USER           | Имя пользователя базы данных в postgresql.                                                                                                                                                                                                      | Да               | admin       |
| DB_PASSWORD       | Пароль пользователя базы данных в postgresql.                                                                                                                                                                                                   | Да               | -           |
