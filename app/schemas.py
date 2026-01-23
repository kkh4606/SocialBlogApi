from pydantic import BaseModel, EmailStr, Field
from pydantic.config import ConfigDict

from datetime import datetime
from typing import Optional, List
from pydantic.types import conint
from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    USER = "user"


class PostBase(BaseModel):
    content: str = Field(min_length=1)
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class User(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(User):
    password: str
    role: Optional[Role] = Role.USER


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(UserCreate):
    pass


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    name: str
    profile_pic: str | None = None
    role: Role = Role.USER
    created_at: datetime


class CommentCreate(BaseModel):
    content: str
    parent_id: int | None = None


class EditComment(BaseModel):
    content: str


class Comment(BaseModel):
    id: int
    post_id: int
    owner_id: int
    content: str


class CommentOut(Comment):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
    post_id: int
    parent_id: Optional[int] = None
    created_at: datetime
    comments_arr: List["CommentOut"] = []
    owner: Optional[UserResponse] = None


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    comments: List[CommentOut] = []
    owner: Optional[UserResponse] = None

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    Post: Post
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str | None] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # type: ignore


class LoginUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role
    access_token: str
    token_type: str
