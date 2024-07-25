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
    try:
        return BlogService.create_blog(db, blog)
    except ValueError as e:
        logger.warning(str(e))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )


@blog.get(
    "",
    response_model=BlogListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_blog(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> BlogListResponse:
    try:
        return BlogService.list_blog(db, page, page_size)
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )


@blog.get(
    "/{id}",
    response_model=BlogResponse,
    status_code=status.HTTP_200_OK,
)
async def read_blog(
    id: int,
    db: Session = Depends(get_db),
) -> BlogResponse:
    try:
        return BlogService.read_blog(db, id)
    except ValueError as e:
        logger.warning(str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )


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
    try:
        return BlogService.update_blog(db, id, blog_update)
    except RequestValidationError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors(),
        )
    except ValueError as e:
        logger.warning(str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
            if "not found" in str(e).lower()
            else status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )
    except Exception as e:
        logger.error(f"Internal server error: {e}")
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
        BlogService.delete_blog(db, id)
    except ValueError as e:
        logger.warning(str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )
