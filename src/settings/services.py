import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


class BaseOAuthConfig(BaseSettings):
    code: str
    url_token: str
    url_user_info: str
    client_id: str
    client_secret: str
    redirect_auth_uri: str
    redirect_path: str
    grant_type: Optional[str]


class GoogleOAuthConfig(BaseOAuthConfig):
    code: str = ""
    url_token: str = "https://accounts.google.com/o/oauth2/token"
    url_user_info: str = "https://www.googleapis.com/oauth2/v1/userinfo"
    client_id: str = os.getenv("GOOGLE_CLIENT_ID", default="test")
    client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", default="test")
    redirect_path: str = "/api/v1/users/callback/google"
    grant_type: str = "authorization_code"
    scope: str = "email profile"
    redirect_auth_uri = "https://accounts.google.com/o/oauth2/auth"


class YandexOAuthConfig(BaseOAuthConfig):
    code: str = ""
    url_token: str = "https://oauth.yandex.ru/token"
    url_user_info: str = "https://login.yandex.ru/info"
    client_id: str = os.getenv("YANDEX_CLIENT_ID", default="test")
    client_secret: str = os.getenv("YANDEX_CLIENT_SECRET", default="test")
    redirect_auth_uri: str = "https://oauth.yandex.ru/authorize"
    redirect_path: str = "/api/v1/users/callback/yandex"
    grant_type: str = "authorization_code"


def get_service_config(service_name: str):
    return {
        "google": GoogleOAuthConfig(),
        "yandex": YandexOAuthConfig(),
    }.get(service_name)
