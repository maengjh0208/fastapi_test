from typing import Optional

from pydantic.main import BaseModel


class UserRegister(BaseModel):
    email: str
    password: str
    nickname: Optional[str] = None


class Token(BaseModel):
    Authorization: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class UserToken(BaseModel):
    member_no: int
    email: str
