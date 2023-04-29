from http import HTTPStatus

from src import settings
from src.common.response import BaseResponse
from src.common.services.oauth_service import BaseOAuthService
from src.repositories.auth_repository import AuthRepository


class YandexOAuthService(BaseOAuthService):
    def __init__(
        self,
        config: settings.YandexOAuthConfig,
        auth_repository: AuthRepository,
    ):
        super().__init__(config)
        self._config = config
        self._auth_repository = auth_repository

    def oauth_authorize(
        self, email, login, social_id, social_name, user_agent
    ):
        return (
            BaseResponse(
                success=True,
                result="Ok",
            ).dict(),
            HTTPStatus.OK,
        )
