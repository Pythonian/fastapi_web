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
        description="Title of the blog post. Must be between 10 and 255 characters.",
    )
    excerpt: str = Field(
        ...,
        min_length=20,
        max_length=300,
        description="Short excerpt of the blog post. Must be between 20 and 300 characters.",
    )
    content: str = Field(
        ...,
        description="Full content of the blog post.",
    )
    image_url: str = Field(
        ...,
        max_length=255,
        description="URL of the blog post image.",
    )
    is_deleted: Optional[bool] = Field(
        False,
        description="Flag to indicate if the blog post is deleted. Defaults to False.",
    )


class BlogCreate(BlogBase):
    """Schema for creating a new blog post."""

    pass


class BlogUpdate(BaseModel):
    """Schema for updating an existing blog post."""

    title: Optional[str] = Field(
        None,
        min_length=10,
        max_length=255,
        description="Title of the blog post. Must be between 10 and 255 characters.",
    )
    excerpt: Optional[str] = Field(
        None,
        min_length=20,
        max_length=300,
        description="Short excerpt of the blog post. Must be between 20 and 300 characters.",
    )
    content: Optional[str] = Field(
        None,
        description="Full content of the blog post.",
    )
    image_url: Optional[str] = Field(
        None,
        max_length=255,
        description="URL of the blog post image.",
    )
    is_deleted: Optional[bool] = Field(
        False,
        description="Flag to indicate if the blog post is deleted. Defaults to False.",
    )


class BlogResponse(BlogBase):
    """Schema for returning blog post data."""

    id: int = Field(
        ...,
        description="Unique identifier for the blog post.",
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the blog post was created.",
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the blog post was last updated.",
    )


class BlogListItemResponse(BaseModel):
    """Schema for representing a blog post item in the list response."""

    id: int = Field(
        ...,
        description="Unique identifier for the blog post.",
    )
    title: str = Field(
        ...,
        description="Title of the blog post.",
    )
    excerpt: str = Field(
        ...,
        description="Short excerpt of the blog post.",
    )
    image_url: str = Field(
        ...,
        description="URL of the blog post image.",
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the blog post was created.",
    )


class BlogListResponse(BaseModel):
    """Schema for representing a blog post listing in the API response."""

    count: int = Field(
        ...,
        description="Total number of blog posts.",
    )
    next: Optional[str] = Field(
        None,
        description="URL to the next page of results, if available.",
    )
    previous: Optional[str] = Field(
        None,
        description="URL to the previous page of results, if available.",
    )
    results: List[BlogListItemResponse] = Field(
        ...,
        description="List of blog post items.",
    )
