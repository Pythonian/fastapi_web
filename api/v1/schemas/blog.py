"""Blog Schema."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BlogBase(BaseModel):
    """Base schema for blog post data."""

    title: str = Field(
        ...,
        min_length=10,
        max_length=255,
        description="Title of the blog post",
    )
    excerpt: str = Field(
        ...,
        min_length=20,
        max_length=300,
        description="Short excerpt of the blog post",
    )
    content: str = Field(
        ...,
        description="Content of the blog post",
    )
    image_url: str = Field(
        ...,
        max_length=255,
        description="URL of the blog post image",
    )
    is_deleted: Optional[bool] = False


class BlogCreate(BlogBase):
    """Schema for creating a new blog post."""

    pass


class BlogUpdate(BaseModel):
    """Schema for updating an existing blog post."""

    title: Optional[str] = Field(
        None,
        min_length=10,
        max_length=255,
        description="Title of the blog post",
    )
    excerpt: Optional[str] = Field(
        None,
        min_length=20,
        max_length=300,
        description="Short excerpt of the blog post",
    )
    content: Optional[str]
    image_url: Optional[str]
    is_deleted: Optional[bool] = False


class BlogResponse(BlogBase):
    """Schema for returning blog post data."""

    id: int
    created_at: datetime
    updated_at: datetime


class BlogListItemResponse(BaseModel):
    """Schema for representing a blog post item in the list response."""

    id: int
    title: str
    excerpt: str
    image_url: str
    created_at: datetime


class BlogListResponse(BaseModel):
    """Schema for representing a blog post listing in the API response."""

    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[BlogListItemResponse]
