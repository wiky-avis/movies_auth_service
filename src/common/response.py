from typing import Any

from pydantic import BaseModel, fields


class BaseResponse(BaseModel):
    success: bool = True
    error: str | list | dict | None = None
    result: Any = None


class Pagination(BaseModel):
    page: int = fields.Field(default=1, ge=1)
    pages: int = fields.Field(default=1, ge=1)
    total_count: int = fields.Field(default=1, ge=1, le=50)
    prev_page: int = None
    next_page: int = None
    has_next: int = None
    has_prev: int = None
