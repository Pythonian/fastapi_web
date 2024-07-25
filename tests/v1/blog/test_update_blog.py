from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from api.db.database import get_db
from api.v1.models.blog import Blog
from main import app

client = TestClient(app)


@pytest.fixture
def db_session_mock():
    """Create a mock database session."""
    return MagicMock()


@pytest.fixture(autouse=True)
def override_get_db(db_session_mock):
    """Override the get_db dependency with a mock session."""
    app.dependency_overrides[get_db] = lambda: db_session_mock
    yield
    app.dependency_overrides[get_db] = None


def test_update_blog_success(db_session_mock):
    """Test successful blog post update."""
    existing_blog = Blog(
        id=1,
        title="Existing Blog Post",
        excerpt="A summary of the blog post...",
        content="The content of the blog post...",
        image_url="image-url-link",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    updated_data = {
        "title": "Updated Blog Post",
        "excerpt": "An updated summary...",
        "content": "Updated content...",
        "image_url": "updated-image-url-link",
    }

    db_session_mock.query.return_value.filter.return_value.first.side_effect = [
        existing_blog,  # Return the existing blog for the first query
        None,  # Return None for the second query to simulate no conflict
    ]
    db_session_mock.commit.side_effect = lambda: None
    db_session_mock.refresh.side_effect = lambda blog: setattr(
        blog, "updated_at", datetime.now(timezone.utc)
    )

    response = client.patch(f"/api/v1/blogs/{existing_blog.id}", json=updated_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == updated_data["title"]
    assert response_data["excerpt"] == updated_data["excerpt"]
    assert response_data["content"] == updated_data["content"]
    assert response_data["image_url"] == updated_data["image_url"]
    assert "updated_at" in response_data


def test_update_blog_conflict(db_session_mock):
    """Test blog post update with conflicting title."""
    existing_blog = Blog(
        id=1,
        title="Existing Blog Post",
        excerpt="A summary of the blog post...",
        content="The content of the blog post...",
        image_url="image-url-link",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    conflicting_blog = Blog(
        id=2,
        title="Updated Blog Post",
        excerpt="Another summary...",
        content="Another content...",
        image_url="another-image-url-link",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    updated_data = {
        "title": "Updated Blog Post",
        "excerpt": "An updated summary...",
        "content": "Updated content...",
        "image_url": "updated-image-url-link",
    }

    db_session_mock.query.return_value.filter.return_value.first.side_effect = [
        existing_blog,  # Return the existing blog for the first query
        conflicting_blog,  # Return the conflicting blog for the second query
    ]

    response = client.patch(f"/api/v1/blogs/{existing_blog.id}", json=updated_data)

    assert response.status_code == 409
    assert response.json()["detail"] == "A blog post with this title already exists."


def test_update_blog_not_found(db_session_mock):
    """Test blog post update when not found."""
    updated_data = {
        "title": "Updated Blog Post",
        "excerpt": "An updated summary...",
        "content": "Updated content...",
        "image_url": "updated-image-url-link",
    }

    db_session_mock.query.return_value.filter.return_value.first.return_value = None

    response = client.patch("/api/v1/blogs/999", json=updated_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Blog post not found."


def test_update_blog_internal_server_error(db_session_mock):
    """Test blog post update with internal server error."""
    updated_data = {
        "title": "Updated Blog Post",
        "excerpt": "An updated summary...",
        "content": "Updated content...",
        "image_url": "updated-image-url-link",
    }

    db_session_mock.query.side_effect = Exception("Unexpected error")

    response = client.patch("/api/v1/blogs/1", json=updated_data)

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error."


def test_update_blog_invalid_data(db_session_mock):
    """Test blog post update with invalid data."""
    existing_blog = Blog(
        id=1,
        title="Existing Blog Post",
        excerpt="A summary of the blog post...",
        content="The content of the blog post...",
        image_url="image-url-link",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    invalid_data = {
        "title": "Short",
        "excerpt": "An updated summary...",
    }

    db_session_mock.query.return_value.filter.return_value.first.side_effect = [
        existing_blog,  # Return the existing blog for the first query
        None,  # Return None for the second query to simulate no conflict
    ]
    db_session_mock.commit.side_effect = lambda: None
    db_session_mock.refresh.side_effect = lambda blog: setattr(
        blog, "updated_at", datetime.now(timezone.utc)
    )

    response = client.patch(f"/api/v1/blogs/{existing_blog.id}", json=invalid_data)

    assert response.status_code == 422


def test_update_blog_boundary_testing(db_session_mock):
    """Test maximum length constraints for title and excerpt."""
    existing_blog = Blog(
        id=1,
        title="Existing Blog Post",
        excerpt="A summary of the blog post...",
        content="The content of the blog post...",
        image_url="image-url-link",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    boundary_blog_data = {
        "title": "T" * 255,  # Maximum allowed length for title
        "excerpt": "E" * 300,  # Maximum allowed length for excerpt
        "content": "Content of the blog post...",
        "image_url": "image-url-link",
    }

    db_session_mock.query.return_value.filter.return_value.first.side_effect = [
        existing_blog,  # Return the existing blog for the first query
        None,  # Return None for the second query to simulate no conflict
    ]
    db_session_mock.commit.side_effect = lambda: None
    db_session_mock.refresh.side_effect = lambda blog: setattr(
        blog, "updated_at", datetime.now(timezone.utc)
    )

    response = client.patch(
        f"/api/v1/blogs/{existing_blog.id}", json=boundary_blog_data
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == boundary_blog_data["title"]
    assert response_data["excerpt"] == boundary_blog_data["excerpt"]
    assert response_data["content"] == boundary_blog_data["content"]
    assert response_data["image_url"] == boundary_blog_data["image_url"]
    assert "updated_at" in response_data


def test_database_error(db_session_mock, mocker):
    """Test database error during blog post update."""
    updated_data = {
        "title": "Updated Blog Post",
        "excerpt": "An updated summary...",
        "content": "Updated content...",
        "image_url": "updated-image-url-link",
    }

    mocker.patch(
        "api.v1.services.blog.BlogService.update_blog",
        side_effect=SQLAlchemyError("Database error"),
    )

    response = client.patch("/api/v1/blogs/1", json=updated_data)

    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "Database error occurred."
