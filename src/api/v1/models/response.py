from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    email: str
