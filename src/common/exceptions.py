import flask


class ResponseError(Exception):
    """Бросает ошибку при некорректных кодах ответа"""

    def __init__(
        self, message: str, request: flask.Request, response: flask.Response
    ):
        super().__init__(message)
        self.request = request
        self.response = response


class BadRequestError(ResponseError):
    """Бросает ошибку для 4хх кодов ответа"""


class ServiceError(ResponseError):
    """Бросает ошибку для 5хх кодов ответа"""
