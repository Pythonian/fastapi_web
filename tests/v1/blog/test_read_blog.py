from datetime import datetime
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


def test_successful_retrieval_of_blog_post(db_session_mock):
    blog = Blog(
        id=1,
        title="Sample Blog Post",
        excerpt="This is a sample excerpt.",
        content="Sample content for the blog post.",
        image_url="https://example.com/sample.jpg",
        created_at=datetime(2024, 7, 22, 12, 0, 0),
        updated_at=datetime(2024, 7, 22, 12, 30, 0),
    )

    db_session_mock.query().filter().first.return_value = blog

    response = client.get("/api/v1/blogs/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Sample Blog Post"
    assert data["excerpt"] == "This is a sample excerpt."
    assert data["content"] == "Sample content for the blog post."
    assert data["image_url"] == "https://example.com/sample.jpg"
    assert data["created_at"] == "2024-07-22T12:00:00"
    assert data["updated_at"] == "2024-07-22T12:30:00"


def test_invalid_blog_post_id():
    response = client.get("/api/v1/blogs/abc")

    assert response.status_code == 422


def test_deleted_blog_post_not_found(db_session_mock):
    """Simulate a request to retrieve a blog post that has been deleted."""
    db_session_mock.query.return_value.filter.return_value.first.return_value = None

    response = client.get("/api/v1/blogs/1")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Blog post not found."


def test_invalid_method():
    response = client.post("/api/v1/blogs/1")

    assert response.status_code == 405
    data = response.json()
    assert data["detail"] == "Method Not Allowed"


def test_internal_server_error(mocker):
    mocker.patch("api.v1.routes.blog", side_effect=Exception("Test exception"))

    response = client.get("/api/v1/blogs/1")

    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "Internal server error."
