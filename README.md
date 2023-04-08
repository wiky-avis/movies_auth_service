# Проектная работа 6 спринта

## Сборка и запуск в контейнере

```bash
make test_build
```

###  Тест API
[Swagger](http://127.0.0.1:5000/api/swagger)

Примерный флоу регистрации пользователя:
```
1. Проверка, существует ли такой пользователь:
GET /api/v1/users/checking_mail?email=sgsf@sgfg.ru

В случае, если не существует, вернет ошибку 404 (значит такого пользователя не найдено)

2. Создание временного пользователя.
POST /api/v1/users/sign_up
body:
{
"email":"sgsf@sgfg.ru",
"password": "pass",
"roles":["ROLE_TEMPORARY_USER"]
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
    "access_token": "fsdcshocjsapa"
  }
}

3. Отправить код пользователю с id пользователя для подтверждения почты.
POST /api/v1/users/308645/send_code
Body:
{
	"code": 7505
}

* код сохраняем в редисе с ограниченным сроком жизни

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
    "access_token": "fsdcshogffhcjsapa",
    "refresh_token": "ggddahAKhdh5rthrt"
  }
}
```
