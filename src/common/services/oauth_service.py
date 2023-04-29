from urllib.parse import urlencode, urljoin

import requests
from flask import redirect

from src import settings
from src.common.collections import get_in


class BaseOAuthService:
    def __init__(self, config: settings.BaseOAuthConfig):
        super().__init__()
        self._config = config

    @staticmethod
    def build_url(base_url: str = None, **kwargs):
        params = urlencode(kwargs)
        return urljoin(base_url, f"?{params}")

    def authorize(self):
        params = dict(
            client_id=self._config.client_id,
            display="popup",
            response_type="code",
            state="yandex",
        )
        url = self.build_url(base_url=self._config.redirect_auth_uri, **params)
        return redirect(url, code=302)

    def get_token(self, auth_code):
        data = urlencode(
            dict(
                grant_type=self._config.grant_type or "",
                client_id=self._config.client_id,
                client_secret=self._config.client_secret,
                code=auth_code,
            )
        )
        token = requests.post(
            url=self._config.url_token,
            data=data,
        ).json()
        return token

    def get_user_info(self, access_token):
        user_info = requests.get(
            url=self._config.url_user_info,
            params=urlencode(
                dict(Authorization="OAuth", oauth_token=access_token)
            ),
        )
        return user_info.json()

    def callback(self, auth_code, user_agent, state: str):
        token = self.get_token(auth_code)
        access_token = get_in(token, "access_token")
        print("----access_token", access_token)
        user_data = self.get_user_info(access_token)
        print("---user_data", user_data)
        # {'id': '*****1641', 'login': '*****-*****', 'client_id': '***d5b466adc4*****baf2a2ce96****',
        #  'display_name': '*****-*****', 'real_name': 'Виктория Акс', 'first_name': 'Виктория', 'last_name': 'Акс',
        #  'sex': 'female', 'default_email': '***-******@yandex.ru', 'emails': ['****-******@yandex.ru'],
        #  'psuid': '1.AAnWCg.**************.6jzcyJwf*******hkKrs3BA'}
        email = get_in(user_data, "email") or get_in(user_data, "default_email") or get_in(user_data, "emails")[0]

        result = self.oauth_authorize(
            email=email,
            login=get_in(user_data, "login"),
            social_id=str(get_in(user_data, "id")),
            social_name=state.upper(),
            user_agent=user_agent,
        )
        print("----result", result)
        # ({'success': True, 'error': None, 'result': 'Ok'}, < HTTPStatus.OK: 200 >)
        return result

    def oauth_authorize(
        self, email, login, social_id, social_name, user_agent
    ):
        raise NotImplementedError
