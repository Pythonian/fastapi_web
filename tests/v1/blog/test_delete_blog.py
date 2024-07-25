from datetime import datetime
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


def test_successful_soft_delete_blog_post(db_session_mock):
    """Test successful soft deletion of a blog post."""
    blog = Blog(
        id=1,
        title="Test Blog Post",
        excerpt="This is a test excerpt",
        content="This is the content of the test blog post",
        image_url="http://example.com/image.png",
        created_at=datetime(2024, 7, 22, 12, 0, 0),
        updated_at=datetime(2024, 7, 22, 12, 0, 0),
        is_deleted=False,
    )

    db_session_mock.query().filter().first.return_value = blog

    response = client.delete("/api/v1/blogs/1")

    assert response.status_code == 204
    db_session_mock.commit.assert_called_once()


def test_delete_invalid_blog_id(db_session_mock):
    """Test deletion of blog post with invalid ID."""
    response = client.delete("/api/v1/blogs/abc")

    assert response.status_code == 422


def test_blog_post_not_found(db_session_mock):
    """Simulate a request to delete a blog post that does not exist."""
    db_session_mock.query.return_value.filter.return_value.first.return_value = None

    response = client.delete("/api/v1/blogs/1")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Blog post not found."


def test_internal_server_error(db_session_mock, mocker):
    """Simulate an internal server error by raising a generic exception."""
    mocker.patch(
        "api.v1.services.blog.BlogService.delete_blog",
        side_effect=Exception("Internal server error"),
    )

    response = client.delete("/api/v1/blogs/1")

    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "Internal server error."


def test_database_error(db_session_mock, mocker):
    """Simulate a database error by raising an SQLAlchemyError."""
    mocker.patch(
        "api.v1.services.blog.BlogService.delete_blog",
        side_effect=SQLAlchemyError("Database error"),
    )

    response = client.delete("/api/v1/blogs/1")

    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "Database error occurred."
