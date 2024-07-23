from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.db.database import get_db
from api.v1.models.blog import Blog
from main import app

client = TestClient(app)


@pytest.fixture
def db_session_mock():
    return MagicMock()


@pytest.fixture(autouse=True)
def override_get_db(db_session_mock):
    app.dependency_overrides[get_db] = lambda: db_session_mock
    yield
    app.dependency_overrides[get_db] = None


def test_create_blog_success(db_session_mock):
    """Checks if a new blog post can be created successfully and
    validates the response data."""
    new_blog_data = {
        "title": "New Blog Post",
        "excerpt": "A summary of the blog post...",
        "content": "The content of the blog post...",
        "image_url": "image-url-link",
    }

    # Mocking the behavior of the database session
    db_session_mock.query.return_value.filter.return_value.first.return_value = None
    db_session_mock.add.side_effect = lambda x: setattr(x, "id", 1)
    db_session_mock.commit.side_effect = lambda: None
    db_session_mock.refresh.side_effect = lambda blog: setattr(
        blog, "created_at", datetime.now(timezone.utc)
    ) or setattr(blog, "updated_at", datetime.now(timezone.utc))

    # Creating the mock blog object
    blog_mock = Blog(**new_blog_data)
    blog_mock.id = 1
    blog_mock.created_at = datetime.now(timezone.utc)
    blog_mock.updated_at = datetime.now(timezone.utc)

    db_session_mock.query.return_value.filter.return_value.first.return_value = None
    db_session_mock.add.side_effect = lambda x: setattr(x, "id", blog_mock.id)
    db_session_mock.commit.side_effect = lambda: None
    db_session_mock.refresh.side_effect = lambda x: setattr(
        x, "created_at", blog_mock.created_at
    ) or setattr(x, "updated_at", blog_mock.updated_at)

    response = client.post("/api/v1/blogs", json=new_blog_data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["title"] == new_blog_data["title"]
    assert response_data["excerpt"] == new_blog_data["excerpt"]
    assert response_data["content"] == new_blog_data["content"]
    assert response_data["image_url"] == new_blog_data["image_url"]
    assert "created_at" in response_data
    assert "updated_at" in response_data


def test_create_blog_conflict(db_session_mock):
    """Simulates a conflict scenario by creating a blog post with a title that
    already exists, then checks for the correct status code and error message."""
    # Arrange
    new_blog_data = {
        "title": "Existing Blog Post",
        "excerpt": "A summary of the blog post...",
        "content": "The content of the blog post...",
        "image_url": "image-url-link",
    }

    # Mock the database query for checking existing blog
    db_session_mock.query.return_value.filter.return_value.first.return_value = Blog(
        title="Existing Blog Post", excerpt="...", content="...", image_url="..."
    )

    # Act
    response = client.post("/api/v1/blogs", json=new_blog_data)

    # Assert
    assert response.status_code == 409
    assert response.json()["detail"] == "A blog post with this title already exists."


def test_create_blog_internal_server_error(db_session_mock):
    """Simulates an internal server error and checks for the
    correct status code and error message."""
    new_blog_data = {
        "title": "New Blog Post",
        "excerpt": "A summary of the blog post...",
        "content": "The content of the blog post...",
        "image_url": "image-url-link",
    }

    db_session_mock.query.side_effect = Exception("Unexpected error")

    response = client.post("/api/v1/blogs", json=new_blog_data)

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error."


def test_create_blog_invalid_data():
    """Sends invalid data (e.g., empty title) and checks for validation errors."""
    invalid_blog_data = {
        "title": "",
        "excerpt": "A summary of the blog post...",
        "content": "The content of the blog post...",
        "image_url": "image-url-link",
    }

    response = client.post("/api/v1/blogs", json=invalid_blog_data)
    assert response.status_code == 422


def test_create_blog_boundary_testing(db_session_mock):
    """Tests the maximum length constraints for the title and excerpt fields,
    ensuring the API handles boundary conditions correctly."""

    boundary_blog_data = {
        "title": "T" * 255,  # Maximum allowed length for title
        "excerpt": "E" * 300,  # Maximum allowed length for excerpt
        "content": "Content of the blog post...",
        "image_url": "image-url-link",
    }

    # Mocking the behavior of the database session
    db_session_mock.query.return_value.filter.return_value.first.return_value = None
    db_session_mock.add.side_effect = lambda x: setattr(x, "id", 1)
    db_session_mock.commit.side_effect = lambda: None
    db_session_mock.refresh.side_effect = lambda x: setattr(
        x, "created_at", datetime.now(timezone.utc)
    ) or setattr(x, "updated_at", datetime.now(timezone.utc))

    response = client.post("/api/v1/blogs", json=boundary_blog_data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["title"] == boundary_blog_data["title"]
    assert response_data["excerpt"] == boundary_blog_data["excerpt"]
    assert response_data["content"] == boundary_blog_data["content"]
    assert response_data["image_url"] == boundary_blog_data["image_url"]
    assert "created_at" in response_data
    assert "updated_at" in response_data
    assert isinstance(
        response_data["created_at"], str
    )  # Check if it's a string representation of a datetime
    assert isinstance(response_data["updated_at"], str)
