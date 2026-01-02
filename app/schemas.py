from pydantic import BaseModel, EmailStr, PlainSerializer

from datetime import datetime
from typing import Optional, List
from pydantic.types import conint
from enum import Enum



class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'


class PostBase(BaseModel):
    title: Optional[str] = None
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class User(BaseModel):
    id: int
    email: EmailStr
    name: str
    profile_pic : str | None
    created_at: datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role : Optional[Role] = Role.USER


class UserLogin(UserCreate):
    email:str
    password: str


class UserUpdate(UserCreate):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    profile_pic : str | None = None
    role: Role = Role.USER
    created_at: datetime

    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: Optional[UserOut] = None

    class Config:
        from_attributes = True


class PostOut(BaseModel):

    Post: Post
    votes: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str | None] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # type:ignore


class LoginUserOut(BaseModel):
    id : int
    name : str
    email: EmailStr
    role : Role
    access_token: str
    token_type: str