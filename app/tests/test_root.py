from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)




def test_ping():
    response = client.get("/")
    assert response.status_code == 200
    assert response.content == "Contact owner for 🔑"