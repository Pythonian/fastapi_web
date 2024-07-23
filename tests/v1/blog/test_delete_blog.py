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


def test_successful_soft_delete_blog_post(db_session_mock):
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
    response = client.delete("/api/v1/blogs/abc")

    assert response.status_code == 422
