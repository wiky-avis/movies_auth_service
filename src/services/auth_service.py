from http import HTTPStatus

from sqlalchemy import inspect
from werkzeug.security import check_password_hash

from src.api.v1.auth.models.user import UserResponse
from src.common.response import BaseResponse
from src.repositories.auth_repository import AuthRepository


def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs
    }


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

    @staticmethod
    def check_password(password_hash, password):
        if not password:
            return False
        return check_password_hash(password_hash, password)
