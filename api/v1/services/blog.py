from sqlalchemy import not_
from sqlalchemy.orm import Session

from api.v1.models.blog import Blog
from api.v1.schemas.blog import (
    BlogCreateSchema,
    BlogListItemResponseSchema,
    BlogListResponseSchema,
    BlogResponseSchema,
    BlogUpdateSchema,
)


class BlogService:
    @staticmethod
    def create_blog(
        db: Session,
        blog: BlogCreateSchema,
    ) -> BlogResponseSchema:
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

        return BlogResponseSchema(
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
    ) -> BlogListResponseSchema:
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

    @staticmethod
    def read_blog(
        db: Session,
        id: int,
    ) -> BlogResponseSchema:
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

        return BlogResponseSchema.model_validate(blog.__dict__)

    @staticmethod
    def update_blog(
        db: Session,
        id: int,
        blog_update: BlogUpdateSchema,
    ) -> BlogResponseSchema:
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

        return BlogResponseSchema(
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
