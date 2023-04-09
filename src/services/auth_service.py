from http import HTTPStatus

from src.api.v1.models.response import UserResponse
from src.common.response import BaseResponse
from src.repositories.auth_repository import AuthRepository


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def checking_mail(self, email):
        user = self.repository.find_by_email(email)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist"}
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )
        result = UserResponse(id=str(user.id), email=user.email).dict()
        return BaseResponse(success=True, result=result).dict(), HTTPStatus.OK
