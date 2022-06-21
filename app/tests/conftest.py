import pytest
from app.core.config import API_KEYS

from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """
    Return an API Client
    """
    app.dependency_overrides = {}
    return TestClient(app)


@pytest.fixture
def authenticated_client(client: TestClient) -> TestClient:
    """
    Return an authenticated API Client
    """
    access_token = API_KEYS[0]

    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}",
    }

    return client