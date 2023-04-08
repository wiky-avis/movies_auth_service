from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    """Базовый класс для ответа от сервиса."""

    success: bool = True
    error: str | list | dict | None = None
    data: Any = None
