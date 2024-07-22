from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from api.v1.models.blog import Blog
from api.v1.schemas.blog import BlogCreateSchema, BlogResponseSchema
from api.db.database import get_db
import logging

blog = APIRouter(prefix="/blogs", tags=["blog"])

logger = logging.getLogger("api")


@blog.post(
    "",
    response_model=BlogResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_blog(blog: BlogCreateSchema, db: Session = Depends(get_db)):
    try:
        existing_blog = db.query(Blog).filter(Blog.title == blog.title).first()
        if existing_blog:
            logger.warning(f"Blog post with title '{blog.title}' already exists.")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A blog post with this title already exists.",
            )

        new_blog = Blog(
            title=blog.title,
            excerpt=blog.excerpt,
            content=blog.content,
            image_url=blog.image_url,
        )
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        logger.info(f"Blog post '{new_blog.title}' created successfully.")
        return new_blog

    except HTTPException as http_err:
        logger.warning(f"HTTP error occurred: {http_err.detail}")
        raise http_err

    except SQLAlchemyError as sql_err:
        logger.error(f"Database error occurred: {sql_err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )

    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )
