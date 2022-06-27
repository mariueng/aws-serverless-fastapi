from app.main import app
from fastapi.testclient import TestClient


def test_ping():
    with TestClient(app) as client:
        response = client.get("/")
        content = response.json()
        assert response.status_code == 200
        assert content == "Contact owner for 🔑 ಠ_ಠ", f"Expected response to be 'Contact owner for 🔑 ಠ_ಠ', but was '{content}'"