from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool = True
    error: str | list | dict | None = None
    result: Any = None


class Pagination(BaseModel):
    page: int = None
    pages: int = None
    total_count: int = None
    prev_page: int = None
    next_page: int = None
    has_next: int = None
    has_prev: int = None
