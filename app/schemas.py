from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostResponseWithVotes(BaseModel):
    Post: PostResponse
    votes: conint(ge=0)

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class VoteCreate(BaseModel):
    post_id: int
    direction: conint(le=1, ge=0)


class VoteResponse(BaseModel):
    post_id: int

    class Config:
        orm_mode = True
