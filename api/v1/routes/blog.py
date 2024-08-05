"""API routes and handlers for blog-related operations."""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.db.database import get_db
from api.v1.schemas.blog import (
    BlogCreate,
    BlogListResponse,
    BlogResponse,
    BlogUpdate,
)
from api.v1.services.blog import BlogService

blog = APIRouter(prefix="/blogs", tags=["Blog"])

logger = logging.getLogger("api")


@blog.post(
    "",
    response_model=BlogResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_blog(
    blog: BlogCreate,
    db: Session = Depends(get_db),
) -> BlogResponse:
    """Create a new blog post.

    Args:
        blog (BlogCreate): The blog post data to create.
        db (Session): The database session dependency.

    Returns:
        BlogResponse: The created blog post response.

    Raises:
        HTTPException: If a blog post with the same title already
                       exists or a database error occurs.
    """
    try:
        return BlogService.create_blog(db, blog)
    except ValueError as e:
        logger.warning("Value error occurred: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except SQLAlchemyError as e:
        logger.exception("Database error occurred", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        ) from e
    except Exception as e:
        logger.exception("Internal server error", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from e


@blog.get(
    "",
    response_model=BlogListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_blog(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=25),
    db: Session = Depends(get_db),
) -> BlogListResponse:
    """Retrieve a list of blog posts with pagination.

    Args:
        page (int): The page number for pagination.
        page_size (int): The number of items per page.
        db (Session): The database session dependency.

    Returns:
        BlogListResponse: The list of blog posts with pagination info.

    Raises:
        HTTPException: If a database error occurs.
    """
    try:
        return BlogService.list_blog(db, page, page_size)
    except SQLAlchemyError as e:
        logger.exception("Database error occurred", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        ) from e
    except Exception as e:
        logger.exception("Internal server error", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from e


@blog.get(
    "/{id}",
    response_model=BlogResponse,
    status_code=status.HTTP_200_OK,
)
async def read_blog(
    id: int,
    db: Session = Depends(get_db),
) -> BlogResponse:
    """Retrieve a blog post by ID.

    Args:
        id (int): The ID of the blog post to retrieve.
        db (Session): The database session dependency.

    Returns:
        BlogResponse: The blog post response.

    Raises:
        HTTPException: If the blog post is not found
                       or a database error occurs.
    """
    try:
        return BlogService.read_blog(db, id)
    except ValueError as e:
        logger.warning("Value error occurred: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except SQLAlchemyError as e:
        logger.exception("Database error occurred", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        ) from e
    except Exception as e:
        logger.exception("Internal server error", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from e


@blog.patch(
    "/{id}",
    response_model=BlogResponse,
    status_code=status.HTTP_200_OK,
)
async def update_blog(
    id: int,
    blog_update: BlogUpdate,
    db: Session = Depends(get_db),
) -> BlogResponse:
    """Update an existing blog post by ID.

    Args:
        id (int): The ID of the blog post to update.
        blog_update (BlogUpdate): The updated blog post data.
        db (Session): The database session dependency.

    Returns:
        BlogResponse: The updated blog post response.

    Raises:
        HTTPException: If the blog post is not found, a conflict occurs,
                       or a database error occurs.
    """
    try:
        return BlogService.update_blog(db, id, blog_update)
    except RequestValidationError as e:
        logger.warning("Validation error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors(),
        ) from e
    except ValueError as e:
        logger.warning("Value error occurred: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
            if "not found" in str(e).lower()
            else status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except SQLAlchemyError as e:
        logger.exception("Database error occurred", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        ) from e
    except Exception as e:
        logger.exception("Internal server error", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from e


@blog.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_blog(
    id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a blog post by ID (soft delete).

    Args:
        id (int): The ID of the blog post to delete.
        db (Session): The database session dependency.

    Raises:
        HTTPException: If the blog post is not found
                       or a database error occurs.
    """
    try:
        BlogService.delete_blog(db, id)
    except ValueError as e:
        logger.warning("Value error occurred: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except SQLAlchemyError as e:
        logger.exception("Database error occurred", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        ) from e
    except Exception as e:
        logger.exception("Internal server error", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from e
