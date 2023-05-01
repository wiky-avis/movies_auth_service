from typing import Any, Dict, Optional


class MockYandexApi:
    def add_mock_user_data_200(self, monkeypatch, auth_code=None):
        def mock(_, auth_code):
            res = {
                "access_token": "y0_AgAAAAAFjWGZAAnWCgAAAADiE",
                "expires_in": 31374752,
                "refresh_token": "1:vDpakA2L_1zj2oxm:UgDiZC",
                "token_type": "bearer",
            }
            return res

        monkeypatch.setattr(
            "src.services.oauth_service.OAuthService.get_user_data", mock
        )

    def add_mock_user_info_200(
        self, monkeypatch, data: Optional[Dict[str, Any]] = None
    ):
        def mock(_, data):
            res = {
                "id": "931514524",
                "login": "test",
                "client_id": "6baf2a2ce96673",
                "display_name": "test",
                "real_name": "Ирка Иванова",
                "first_name": "Ирка",
                "last_name": "Иванова",
                "sex": "female",
                "default_email": "test@yandex.ru",
                "emails": ["test@yandex.ru"],
                "psuid": "1.AAnWCg.Qj80upy.6jzs3BA",
            }
            return res

        monkeypatch.setattr(
            "src.services.oauth_service.OAuthService.get_user_info", mock
        )


class MockGoogleApi:
    def add_mock_user_data_200(self, monkeypatch, auth_code=None):
        def mock(_, auth_code):
            res = {
                "access_token": "ya29.a0AWY7Ckl2-KL8qV-r6a",
                "expires_in": 3599,
                "refresh_token": "1//0ct1875GAwSNwF-L9Ir3-zBpuRi",
                "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid",
                "token_type": "Bearer",
                "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImM5YWZkYTM2OD",
            }
            return res

        monkeypatch.setattr(
            "src.services.oauth_service.OAuthService.get_user_data", mock
        )

    def add_mock_user_info_200(
        self, monkeypatch, data: Optional[Dict[str, Any]] = None
    ):
        def mock(_, data):
            res = {
                "id": "104838852",
                "email": "test@gmail.com",
                "verified_email": True,
                "name": "Ирка Иванова",
                "given_name": "Ирка",
                "family_name": "Иванова",
                "picture": "https://lh3.googleusercontent.com/a/AGNmyxbD5K3sjy2JQ=s96-c",
                "locale": "ru",
            }
            return res

        monkeypatch.setattr(
            "src.services.oauth_service.OAuthService.get_user_info", mock
        )
