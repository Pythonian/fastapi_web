import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import not_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.db.database import get_db
from api.v1.models.blog import Blog
from api.v1.schemas.blog import (
    BlogCreateResponseSchema,
    BlogCreateSchema,
    BlogListItemResponseSchema,
    BlogListResponseSchema,
)

blog = APIRouter(prefix="/blogs", tags=["Blog"])

logger = logging.getLogger("api")


@blog.post(
    "",
    response_model=BlogCreateResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_blog(
    blog: BlogCreateSchema,
    db: Session = Depends(get_db),
) -> BlogCreateResponseSchema:
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

        return BlogCreateResponseSchema.model_validate(new_blog.__dict__)

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


@blog.get(
    "",
    response_model=BlogListResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def list_blog(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> BlogListResponseSchema:
    try:
        offset = (page - 1) * page_size
        query = (
            db.query(Blog)
            .filter(not_(Blog.is_deleted))
            .order_by(Blog.created_at.desc())
        )
        total_count = query.count()
        blogs = query.offset(offset).limit(page_size).all()

        next_page = None
        if offset + page_size < total_count:
            next_page = f"/api/v1/blogs?page={page + 1}&page_size={page_size}"

        prev_page = None
        if page > 1:
            prev_page = f"/api/v1/blogs?page={page - 1}&page_size={page_size}"

        results = [
            BlogListItemResponseSchema(
                id=blog.id,
                title=blog.title,
                excerpt=blog.excerpt,
                image_url=blog.image_url,
                created_at=blog.created_at,
            )
            for blog in blogs
        ]

        return BlogListResponseSchema(
            count=total_count,
            next=next_page,
            previous=prev_page,
            results=results,
        )

    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
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
