from typing import Optional

from pydantic import BaseSettings


class BaseOAuthConfig(BaseSettings):
    code: str
    url_token: str
    url_user_info: str
    client_id: str
    client_secret: str
    redirect_auth_uri: str
    redirect_uri: str
    grant_type: Optional[str]


class VKOAuthConfig(BaseOAuthConfig):
    code: str = ""
    url_token: str = "https://oauth.vk.com/access_token"
    url_user_info: str = (
        "https://api.vk.com/method/users.get?fields=uid,first_name,last_name,nickname,screen_name,sex,bdate,city,country,timezone,photo",
    )
    client_id: str = "..."
    client_secret: str = "..."
    redirect_uri: str = "http://localhost:5000/api/v1/oauth/callback/vk"


class GoogleOAuthConfig(BaseOAuthConfig):
    code: str = ""
    url_token: str = "https://accounts.google.com/o/oauth2/token"
    url_user_info: str = "https://www.googleapis.com/oauth2/v1/userinfo"
    client_id: str = "..."
    client_secret: str = "..."
    redirect_uri: str = "http://localhost:5000/api/v1/oauth/callback/google"
    grant_type: str = "authorization_code"


class YandexOAuthConfig(BaseOAuthConfig):
    code: str = ""
    url_token: str = "https://oauth.yandex.ru/token"
    url_user_info: str = "https://login.yandex.ru/info"
    client_id: str = "314d5b466adc4c99896baf2a2ce96673"
    client_secret: str = "caf4f54c2d7d4253b418700370407d1e"
    redirect_auth_uri: str = "https://oauth.yandex.ru/authorize"
    redirect_uri: str = "http://localhost:8080/api/v1/oauth/callback/yandex"
    grant_type: str = "authorization_code"
