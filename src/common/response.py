from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool = True
    error: str | list | dict | None = None
    result: Any = None
