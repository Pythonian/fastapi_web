from sqlalchemy import not_
from sqlalchemy.orm import Session

from api.v1.models.blog import Blog
from api.v1.schemas.blog import (
    BlogCreate,
    BlogListItemResponse,
    BlogListResponse,
    BlogResponse,
    BlogUpdate,
)


class BlogService:
    """Service class for blog operations."""

    @staticmethod
    def create_blog(
        db: Session,
        blog: BlogCreate,
    ) -> BlogResponse:
        """
        Create a new blog post.

        Args:
            db (Session): The database session.
            blog (BlogCreate): The blog post data to create.

        Returns:
            BlogResponse: The created blog post response.

        Raises:
            ValueError: If a blog post with the same title already exists.
        """
        existing_blog = db.query(Blog).filter(Blog.title == blog.title).first()
        if existing_blog:
            raise ValueError("A blog post with this title already exists.")

        new_blog = Blog(
            title=blog.title,
            excerpt=blog.excerpt,
            content=blog.content,
            image_url=blog.image_url,
        )
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)

        return BlogResponse(
            id=new_blog.id,
            title=new_blog.title,
            excerpt=new_blog.excerpt,
            content=new_blog.content,
            image_url=new_blog.image_url,
            created_at=new_blog.created_at,
            updated_at=new_blog.updated_at,
        )

    @staticmethod
    def list_blog(
        db: Session,
        page: int,
        page_size: int,
    ) -> BlogListResponse:
        """
        Retrieve a list of blog posts with pagination.

        Args:
            db (Session): The database session.
            page (int): The page number for pagination.
            page_size (int): The number of items per page.

        Returns:
            BlogListResponse: The list of blog posts with pagination info.
        """
        offset = (page - 1) * page_size
        query = (
            db.query(Blog)
            .filter(not_(Blog.is_deleted))
            .order_by(Blog.created_at.desc())
        )
        total_count = query.count()
        blogs = query.offset(offset).limit(page_size).all()

        next_page = (
            f"/api/v1/blogs?page={page + 1}&page_size={page_size}"
            if offset + page_size < total_count
            else None
        )
        prev_page = (
            f"/api/v1/blogs?page={page - 1}&page_size={page_size}" if page > 1 else None
        )

        results = [
            BlogListItemResponse(
                id=blog.id,
                title=blog.title,
                excerpt=blog.excerpt,
                image_url=blog.image_url,
                created_at=blog.created_at,
            )
            for blog in blogs
        ]

        return BlogListResponse(
            count=total_count,
            next=next_page,
            previous=prev_page,
            results=results,
        )

    @staticmethod
    def read_blog(
        db: Session,
        id: int,
    ) -> BlogResponse:
        """
        Retrieve a blog post by ID.

        Args:
            db (Session): The database session.
            id (int): The ID of the blog post to retrieve.

        Returns:
            BlogResponse: The blog post response.

        Raises:
            ValueError: If the blog post is not found.
        """
        blog = (
            db.query(Blog)
            .filter(
                Blog.id == id,
                not_(Blog.is_deleted),
            )
            .first()
        )
        if not blog:
            raise ValueError("Blog post not found.")

        return BlogResponse(
            id=blog.id,
            title=blog.title,
            excerpt=blog.excerpt,
            content=blog.content,
            image_url=blog.image_url,
            created_at=blog.created_at,
            updated_at=blog.updated_at,
        )

    @staticmethod
    def update_blog(
        db: Session,
        id: int,
        blog_update: BlogUpdate,
    ) -> BlogResponse:
        """
        Update an existing blog post by ID.

        Args:
            db (Session): The database session.
            id (int): The ID of the blog post to update.
            blog_update (BlogUpdate): The updated blog post data.

        Returns:
            BlogResponse: The updated blog post response.

        Raises:
            ValueError: If the blog post is not found or a blog post
                        with the updated title already exists.
        """
        blog = (
            db.query(Blog)
            .filter(
                Blog.id == id,
                not_(Blog.is_deleted),
            )
            .first()
        )
        if not blog:
            raise ValueError("Blog post not found.")

        update_data = blog_update.model_dump(exclude_unset=True)

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
                raise ValueError("A blog post with this title already exists.")

        for field, value in update_data.items():
            setattr(blog, field, value)

        db.commit()
        db.refresh(blog)

        return BlogResponse(
            id=blog.id,
            title=blog.title,
            excerpt=blog.excerpt,
            content=blog.content,
            image_url=blog.image_url,
            created_at=blog.created_at,
            updated_at=blog.updated_at,
        )

    @staticmethod
    def delete_blog(
        db: Session,
        id: int,
    ) -> None:
        """
        Delete a blog post by ID (soft delete).

        Args:
            db (Session): The database session.
            id (int): The ID of the blog post to delete.

        Raises:
            ValueError: If the blog post is not found.
        """
        blog_to_delete = (
            db.query(Blog)
            .filter(
                Blog.id == id,
                not_(Blog.is_deleted),
            )
            .first()
        )
        if not blog_to_delete:
            raise ValueError("Blog post not found.")

        blog_to_delete.is_deleted = True
        db.commit()
