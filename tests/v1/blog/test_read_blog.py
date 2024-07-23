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
    data = response.json()
    assert "detail" in data
    assert isinstance(data["detail"], list)
    assert any("msg" in error for error in data["detail"])
