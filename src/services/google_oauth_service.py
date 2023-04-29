from src import settings
from src.common.services.oauth_service import BaseOAuthService


class GoogleOAuthService(BaseOAuthService):
    def __init__(self, config: settings.GoogleOAuthConfig):
        super().__init__(config)
        self._config = config
