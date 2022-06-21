from datetime import datetime
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

"""
Tests:
- Test invalid dates
- Test invalid zones
- Computations
"""

# Create valid url endpoint
date = datetime.today().strftime("%Y%m%d")
endpoint = f"/api/v1/prices/electricity/?zone=NO1&date={date}"

def test_get_electricity_prices_endpoint(authenticated_client):
    """ Test that we can retrieve data in valid format"""
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200

    body = response.json()

    assert type(body) == dict

    timestamps = list(body.keys())

    assert len(timestamps) >= 23  # Can be 23 hours at shortest I think (due to DST)
    assert type(body[timestamps[0]]["price_per_kwh"]) == float


def test_get_too_early_date(authenticated_clietnt):
    """ Test that we can't get data before 2014 """
    pass


def test_get_too_late_date(authenticated_client):
    """ Test that we can't get data for tomorrow unless it's past 14:00 """
    pass


def test_zones(authenticated_client):
    """ Test valid and invalid bidding zones """
    pass


def test_elprice_calculation(authenticated_client):
    """ Test that the price * currency computation is correct """
    pass
