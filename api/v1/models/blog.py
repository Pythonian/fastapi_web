"""The Blog Post Model."""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from api.v1.models.base import Base


class Blog(Base):
    """Blog Post model to store details of blog posts."""

    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, unique=True)
    excerpt = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
