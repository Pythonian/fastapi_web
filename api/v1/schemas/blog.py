"""Blog Schema."""

from pydantic import BaseModel, Field
from datetime import datetime


class BlogResponseSchema(BaseModel):
    """Schema for representing a blog post in the API response."""

    id: int
    title: str
    excerpt: str
    content: str
    image_url: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BlogCreateSchema(BaseModel):
    """Schema for creating a new blog post.

    This represents the data structure required when a client
    submits a request to create a new blog post.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Title of the blog post",
    )
    excerpt: str = Field(
        ...,
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
