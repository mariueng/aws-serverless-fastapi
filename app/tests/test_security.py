from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

unauthenticated_client = TestClient(app)

def test_no_api_key():
    """ Test that no api key is handled """
    today = datetime.today().strftime("%Y%m%d")
    endpoint = f"/api/v1/prices/electricity/?zone=NO1&date={today}"
    response = unauthenticated_client.get(endpoint)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_invalid_api_key(authenticated_client):
    """ Test that invalid api key is handled """
    authenticated_client.headers["Authorization"] = "Bearer shallabais"
    today = datetime.today().strftime("%Y%m%d")
    endpoint = f"/api/v1/prices/electricity/?zone=NO1&date={today}"
    response = authenticated_client.get(endpoint)

    assert response.status_code == 401
    assert response.json()["detail"] == "Forbidden"