import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import not_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.db.database import get_db
from api.v1.models.blog import Blog
from api.v1.schemas.blog import (
    BlogCreateSchema,
    BlogListItemResponseSchema,
    BlogListResponseSchema,
    BlogResponseSchema,
    BlogUpdateSchema,
)

blog = APIRouter(prefix="/blogs", tags=["Blog"])

logger = logging.getLogger("api")


@blog.post(
    "",
    response_model=BlogResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_blog(
    blog: BlogCreateSchema,
    db: Session = Depends(get_db),
) -> BlogResponseSchema:
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

        return BlogResponseSchema(
            id=new_blog.id,
            title=new_blog.title,
            excerpt=new_blog.excerpt,
            content=new_blog.content,
            image_url=new_blog.image_url,
            created_at=new_blog.created_at,
            updated_at=new_blog.updated_at,
        )

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


@blog.get(
    "/{id}",
    response_model=BlogResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def read_blog(
    id: int,
    db: Session = Depends(get_db),
) -> BlogResponseSchema:
    try:
        blog = (
            db.query(Blog)
            .filter(
                Blog.id == id,
                not_(Blog.is_deleted),
            )
            .first()
        )
        if not blog:
            logger.warning(f"Blog post with ID '{id}' not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog post not found.",
            )

        logger.info(f"Blog post with ID '{id}' retrieved successfully.")
        return BlogResponseSchema.model_validate(blog.__dict__)

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
            detail="Unexpected error occurred.",
        )


@blog.patch(
    "/{id}",
    response_model=BlogResponseSchema,
    status_code=status.HTTP_200_OK,
)
def update_blog(
    id: int,
    blog_update: BlogUpdateSchema,
    db: Session = Depends(get_db),
) -> BlogResponseSchema:
    try:
        # Fetch the blog post to be updated
        blog = (
            db.query(Blog)
            .filter(
                Blog.id == id,
                not_(Blog.is_deleted),
            )
            .first()
        )
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog post not found.",
            )

        # Get the updated data
        update_data = blog_update.model_dump(exclude_unset=True)

        # Check for title uniqueness
        if "title" in update_data and update_data["title"] != blog.title:
            existing_blog = (
                db.query(Blog)
                .filter(
                    Blog.title == update_data["title"],
                    not_(Blog.is_deleted),
                )
                .first()
            )
            if existing_blog:
                logger.warning(
                    f"Blog post with title '{update_data['title']}' already exists."
                )
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A blog post with this title already exists.",
                )

        # Update fields if they are provided
        for field, value in update_data.items():
            setattr(blog, field, value)

        db.commit()
        db.refresh(blog)
        logger.info(f"Blog post '{blog.title}' updated successfully.")

        return BlogResponseSchema(
            id=blog.id,
            title=blog.title,
            excerpt=blog.excerpt,
            content=blog.content,
            image_url=blog.image_url,
            created_at=blog.created_at,
            updated_at=blog.updated_at,
        )

    except HTTPException as http_err:
        # Log the HTTP exception
        logger.warning(f"HTTP error occurred: {http_err.detail}")
        raise http_err

    except SQLAlchemyError as sql_err:
        # Log SQLAlchemy errors
        logger.error(f"Database error occurred: {sql_err}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )

    except Exception as e:
        # Log other unexpected errors
        logger.error(f"Unexpected error occurred: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )


@blog.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_blog(
    id: int,
    db: Session = Depends(get_db),
) -> None:
    try:
        blog_to_delete = (
            db.query(Blog)
            .filter(
                Blog.id == id,
                not_(Blog.is_deleted),
            )
            .first()
        )
        if not blog_to_delete:
            logger.warning(f"Blog post with ID '{id}' not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog post with given id not found.",
            )

        blog_to_delete.is_deleted = True
        db.commit()
        logger.info(f"Blog post '{blog_to_delete.title}' deleted successfully.")

    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )

    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )
