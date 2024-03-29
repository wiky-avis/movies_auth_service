# Сервис Auth API
Сервис авторизации с системой ролей. Авторозация реализована с помощью jwt-токенов, которые прокидываются в куки 
юзера. Токены шифруются с помощью приватного ключа и расшифровываются с помощью публичного ключа.

### Авторы
Лид команды: [Аксентий Виктория](https://github.com/wiky-avis)
Разработчик: [Подрядов Олег](https://github.com/opodryadov)

### Создана интеграция Auth-сервиса и AsyncAPI-сервиса:
[Интеграция с AsyncAPI](https://github.com/opodryadov/Async_API_sprint_1/pull/49)

### Доработан сервис Auth:
Осуществлена возможность передачи таймзоны (поле tz) от фронта в ручки регистрации/аутентификации пользователя, а также добавлена srv-ручка, которая по user_id возвращает всю модель без пароля.

[Доработка сервиса](https://github.com/wiky-avis/Auth_sprint_1/pull/90)

Пример запроса:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/srv/users?user_id=73c9c344-5230-478d-95bf-b100f8569440' \
  -H 'accept: application/json'
```

Ответ ручки:
```
{
  "success": true,
  "error": null,
  "result": {
    "id": "73c9c344-5230-478d-95bf-b100f8569440",
    "email": "123@123.ru",
    "roles": [
      "ROLE_PORTAL_USER"
    ],
    "verified_mail": true,
    "registered_on": "2023-06-20 07:13:22",
    "tz": "-8"
  }
}
```



## Используемые технологии
- API написано на Python и Flask.
- В качестве хранилища используется Postgres и Redis.
- Добавлена возможность регистрации с помощью социальных сетей (OAuth2).
- Добавлена распределённая трассировка, подключен Jaeger.

## Взаимодействие с другими сервисами
Что нужно, чтобы это работало у вас:
1. Получить секретный публичный ключ.
2. Реализовать в вашем сервисе логику, которая будет:
- Проверять наличие cookie "access_token_cookie" в запросе;
- Извлекать из него JWT токен;
- Получать из payload user_id и его роли;
- Выполнять логику метода своего сервиса в контексте полученного пользователя.
3. Получить токен доступа к srv ручкам.

Формат JWT:
```
{
  "user_id": "5eff1f88-8f2b-40c5-a4d0-85893cb7071b",
  "email": "test@test.ru",
  "verified_mail": true,
  "roles":["ROLE_PORTAL_USER"]
}
```

## Запуск проекта:
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
- Опционально: создать суперпользователя(для создания пользователя в бд должна быть роль 'ROLE_PORTAL_ADMIN')
```sql
insert into roles
(id, name, description)
VALUES('cfc83768-9be4-4066-be89-695d35ea9136', 'ROLE_PORTAL_ADMIN', '');
```
```bash
python manage.py create-superuser your_email your_password
```

###  Тест API
[Swagger](http://127.0.0.1:5000/api/swagger)

## Описание функционала
Преполагается взаимодействие фронта с апи нашего сервиса.

### Регистрации пользователя:
1. Проверка, существует ли такой пользователь:
**GET /api/v1/users?email=sgsf@sgfg.ru**

Ответ:
```
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
```

- В случае, если не существует, вернет ошибку 404 (значит такого пользователя не найдено).
- Если вернулся код 404 создаем временного пользователя.
- Если такой пользователь существует и вернулся код 200 и флаг verified_mail=true(смотрит фронт), 
открываем окно ввода пароля(Аутентификация /api/v1/users/login). 
- Если код 200 и флаг verified_mail=false, просим пользователя подтвердить почту, 
пересылаем ему код подтверждения /api/v1/users/308645/send_code.

2. Создание временного пользователя.
**POST /api/v1/users/sign_up**

body:
```
{
    "email":"sgsf@sgfg.ru"
    "password": "password"
}
```

Ответ:
```
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
```

3. Отправить код пользователю с id пользователя для подтверждения почты.
**POST /api/v1/users/308645/send_code**

Body:
```
{
	"code": 7505
}
```

* код сохраняем в редисе с ограниченным сроком жизни

4. Подтверждение почты кодом из письма.
**POST /api/v1/users/308645/mail**

body:
```
{
	"code": 7505
}
```

*Проверяем в редисе есть ли такой код 7505

- Если есть, проставляем флаг verified_mail в True

Ответ:
```
{
    "success":true,
    "result": "Ok"
}
```

- Если такого нет, ответ:

Ответ:
```
{
    "success":false,
    "result": null
}
```

- Если ответ ручки /api/v1/users/308645/mail отрицательный. Отправить повторно код пользователю 
с id пользователя для подтверждения почты.
**POST /api/v1/users/308645/send_code**

Body:
```
{
	"code": 7506
}
```

### Регистрация с помощью социальных сетей (OAuth2)
1. **GET /api/v1/users/authorize/<string:provider_name>**
2. **GET /api/v1/users/callback/<string:provider_name>**
На этом этапе получаем данные о пользователе от провайдера, создаем временного пользователя. Далее пользователю 
необходимо подвердить свою почту(Пункты 3 и 4 из предыдущего примера флоу регистрации пользователя).

### Управление ролями
- Получение списка ролей: **GET /api/v1/roles**
- Назначить роль пользователю: **POST /api/v1/roles**
- Удаление роли у пользователя: **DELETE /api/v1/roles**
- Получение ролей пользователя по user_id: **GET /api/v1/roles/check_permissions/?user_id=<str:user_id>**

Доступ к этим ручкам имеют юзеры с ролью администратор.

### Управление авторизацией
- Авторизация пользователя: **POST /api/v1/users/login**
- Создание пользователя: **POST /api/v1/users/sign_up**
- Выход пользователя (помещает переданные токены в блоклист): **DELETE /api/v1/users/logout**
- Обновление access-токена: **POST /api/v1/users/refresh_token**
- Авторизация и регистациа с помощью социальных сетей (OAuth2):
  **GET /api/v1/users/authorize/<string:provider_name>**
  **GET /api/v1/users/callback/<string:provider_name>**

### Управление пользователями
- Изменение email/логин пользователя: **PATCH /api/v1/users**
- История авторизаций пользователя: **GET /api/v1/users/login_history**
- Удаление аккаунта пользователя: **DELETE /api/v1/users**
- Изменение пароля пользователя **PATCH /api/v1/users/change_password**
- Подтверждение почты **POST /api/v1/users/<str:user_id>/mail**
- Отправка кода подтверждения на почту **POST /api/v1/users/<str:user_id>/send_code**

## Сервисные ручки
### Управление ролями
- Получение списка ролей: **GET /api/srv/roles**
- Назначение роли пользователю: **POST /api/srv/roles**
- Удаление роли у пользователя: **DELETE /api/srv/roles**
- Получение ролей пользователя по user_id: **GET /api/v1/roles/check_permissions/?user_id=<str:user_id>**
- Добавление новой роли в бд: **POST /api/srv/roles/create_role**
- Удаление роли из бд: **DELETE /api/srv/roles/<string:role_id>/delete_role**
### Пользователи:
- Получение информации о пользователе: **GET api/srv/users?user_id=<str:user_id>**

*Необходим токен доступа
