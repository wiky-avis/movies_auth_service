# Проектная работа 6 спринта

###  Сборка и запуск в контейнере
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
- сборка контейнеров
```bash
make up_local_compose
```
- создание .env файла
```bash
cp .env.test .env
```
- привозникновении ошибки "ModuleNotFoundError: No module named 'config'"
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

###  Тест API
[Swagger](http://127.0.0.1:5000/api/swagger)

Примерный флоу регистрации пользователя:
```
1. Проверка, существует ли такой пользователь:
GET /api/v1/users?email=sgsf@sgfg.ru

В случае, если не существует, вернет ошибку 404 (значит такого пользователя не найдено)
Если вернулся код 404 создаем временного пользователя.
Если такой пользователь существует и вернулся код 200 и флаг verified_mail=true(смотрит фронт), открываем окно ввода пароля(Аутентификация /api/v1/users/sign_in). 
Если код 200 и флаг verified_mail=false, просим пользователя подтвердить почту, ппересылаем ему код подтверждения /api/v1/users/308645/resend_code

2. Создание временного пользователя.
POST /api/v1/users/sign_up
body:
{
"email":"sgsf@sgfg.ru"
}

Ответ:
{
  "success": true,
  "data": {
    "id": 308866, 
    "email": "sds@sdfsdf.ru",
    "roles": [
      "ROLE_TEMPORARY_USER"
    ],
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
PUT /api/v1/users/308645/mail?code=7505

*Проверяем в редисе есть ли такой код 7505

- Если есть ответ  {
  "success":true,
  «result»: "Ok"
}
- Если такого нет {
  "success":false,
  «result»: null
}
5. Если ответ ручки /api/v1/users/308645/mail отрицательный. Отправить повторно код пользователю с id пользователя для подтверждения почты.
POST /api/v1/users/308645/resend_code
Body:
{
	"code": 7506
}

6. Если ответ ручки /api/v1/users/308645/mail положительный. Регистрируем полноценно пользователя, проставляем флаг verified_mail в True и обновляем роль ROLE_PORTAL_USER.

PATCH /api/v1/users/308645/sign_up

Ответ:
{
  "success": true,
  "data": {
    "id": 308866, 
    "email": "sds@sdfsdf.ru",
    "roles": [
      "ROLE_PORTAL_USER"
    ],
  }
}
```
