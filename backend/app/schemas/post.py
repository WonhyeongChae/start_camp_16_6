from datetime import datetime
from typing import Literal

from pydantic import Field

from app.schemas.common import CamelModel


PostCategory = Literal["여행", "맛집", "축제", "생활", "자유"]


class PostBase(CamelModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    category: PostCategory
    nickname: str = Field(default="익명", min_length=1, max_length=50)


class PostCreate(PostBase):
    password: str = Field(min_length=1, max_length=100)


class PostUpdate(PostBase):
    password: str = Field(min_length=1, max_length=100)


class PostDeleteRequest(CamelModel):
    password: str = Field(min_length=1, max_length=100)


class PostRead(CamelModel):
    id: int
    title: str
    content: str
    category: str
    nickname: str
    view_count: int
    recommendation_count: int
    created_at: datetime
    updated_at: datetime


class PostListItem(PostRead):
    pass


class PostListData(CamelModel):
    items: list[PostListItem]
    page: int
    size: int
    total: int
    total_pages: int


class PostDetailData(CamelModel):
    post: PostRead
