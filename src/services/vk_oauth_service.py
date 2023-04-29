from src import settings
from src.common.services.oauth_service import BaseOAuthService


class VKOAuthService(BaseOAuthService):
    def __init__(self, config: settings.VKOAuthConfig):
        super().__init__(config)
        self._config = config
