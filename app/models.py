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


class UserInfo(BaseModel):
    email: str
    nickname: Optional[str] = None


class BookmarkFolderInfo(BaseModel):
    folder_name: str


class BookmarkFolders(BookmarkFolderInfo):
    folder_no: int


class BookmarkProduct(BaseModel):
    product_no: int
    folder_no: int


class ProductInfo(BaseModel):
    product_no: int
    product_name: str
    thumbnail: str
    price: int

