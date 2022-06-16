from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

"""
Tests:
- Test invalid dates
- Test invalid zones
- Computations
"""

endpoint = "/api/v1/electricity/?zone=NO1&date=20200101"

def test_get_electricity_prices():
    response = client.get(endpoint)
    assert response.status_code == 200
    assert response.json() == 2
