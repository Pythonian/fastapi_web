"""The Blog Post Model."""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from api.v1.models.base import Base


class Blog(Base):
    """Blog Post model to store details of blog posts."""

    __tablename__ = "blogs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        doc="Unique identifier for the blog post.",
    )
    title = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        doc="Title of the blog post. Must be unique.",
    )
    excerpt = Column(
        String(300),
        nullable=False,
        doc="Summary of the blog post.",
    )
    content = Column(
        Text,
        nullable=False,
        doc="Full content of the blog post.",
    )
    image_url = Column(
        String(255),
        nullable=False,
        doc="URL of the image associated with the blog post.",
    )
    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Flag to indicate if the blog post is deleted.",
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        doc="Timestamp when the blog post was created.",
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Timestamp when the blog post was last updated.",
    )
