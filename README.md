# Проектная работа 6 спринта

###  Сборка и запуск в контейнере
- создание .env файла (.env.example)

- prod
```bash
make up
```
- local
```bash
make up_local_compose
```

### Миграции
- автоматическое создание миграции после изменения модели
```bash
flask db migrate --message "message"
```
- применить миграцию
```bash
flask db upgrade
```
- откат миграции
```bash
flask db downgrade
```
- содать пустую миграцию
```bash
flask db revision --message "message"
```

### Тестирование (локально)
- установка зависимостей
```bash
pip3 install poetry
poetry install --no-root && poetry shell
```
- создание .env файла (.env.example)
```bash
cp .env.example .env
```

- сборка контейнеров
```bash
make up_local_compose
```
- создание .env файла (для локального запуска api и тестов)
```bash
cp .env.test .env
```
- при возникновении ошибки "ModuleNotFoundError: No module named 'config'"
```bash
export PYTHONPATH=src
```
- запуск апи
```bash
python manage.py api
```
- запуск тестов
```bash
pytest
```
- создать суперпользователя
```bash
python manage.py create-superuser your_email your_password
```

###  Тест API
[Swagger](http://127.0.0.1:5000/api/swagger)

Примерный флоу регистрации пользователя:
```
1. Проверка, существует ли такой пользователь:
GET /api/v1/users?email=sgsf@sgfg.ru

Ответ:
{
    "success": true,
    "result": {
      "id": "string",
      "email": "string",
      "roles": [
        "ROLE_PORTAL_USER"
      ],
      "verified_mail": false,
      "registered_on": "string"
    }
}

В случае, если не существует, вернет ошибку 404 (значит такого пользователя не найдено)
Если вернулся код 404 создаем временного пользователя.
Если такой пользователь существует и вернулся код 200 и флаг verified_mail=true(смотрит фронт), 
открываем окно ввода пароля(Аутентификация /api/v1/users/login). 
Если код 200 и флаг verified_mail=false, просим пользователя подтвердить почту, 
пересылаем ему код подтверждения /api/v1/users/308645/send_code.

2. Создание временного пользователя.
POST /api/v1/users/sign_up
body:
{
    "email":"sgsf@sgfg.ru"
    "password": "password"
}

Ответ:
{
    "success": true,
    "result": {
        "id": 308866,
        "email": "sds@sdfsdf.ru",
        "roles": ["ROLE_PORTAL_USER"],
        "verified_mail": false,
        "registered_on": "string"
    }
}

3. Отправить код пользователю с id пользователя для подтверждения почты.
POST /api/v1/users/308645/send_code
Body:
{
	"code": 7505
}

* код сохраняем в редисе с ограниченным сроком жизни (10 мин например)

4. Подтверждение почты кодом из письма.
POST /api/v1/users/308645/mail

{
	"code": 7505
}

*Проверяем в редисе есть ли такой код 7505

- Если есть, проставляем флаг verified_mail в True
Ответ:

{
    "success":true,
    "result": "Ok"
}
- Если такого нет, ответ:
{
    "success":false,
    "result": null
}
- Если ответ ручки /api/v1/users/308645/mail отрицательный. Отправить повторно код пользователю 
с id пользователя для подтверждения почты.
POST /api/v1/users/308645/send_code
Body:
{
	"code": 7506
}
```
