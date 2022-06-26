from datetime import datetime, timedelta


def test_get_electricity_prices_endpoint(authenticated_client):
    """ Test that we can retrieve data in valid format"""

    today = datetime.today().strftime("%Y%m%d")
    endpoint = f"/api/v1/prices/electricity/?zone=NO1&date={today}"
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200

    body = response.json()

    assert type(body) == dict

    timestamps = list(body.keys())

    assert len(timestamps) >= 23  # Can be 23 hours at shortest I think (due to DST)
    assert type(body[timestamps[0]]["price_per_kwh"]) == float


def test_get_too_early_date(authenticated_client):
    """ Test that we can't get data before 2014 """
    invalid_early_date = "20131231"
    endpoint = f"/api/v1/prices/electricity/?zone=NO1&date={invalid_early_date}"
    response = authenticated_client.get(endpoint)

    assert response.status_code == 400
    assert response.json()["detail"] == "Price data before 2014-12-12 is unavailable"


def test_get_too_late_date(authenticated_client):
    """ Test that we can't get data for tomorrow-tomorrow and tomorrow unless it's past 14:00 """
    tomorrow = (datetime.today() + timedelta(days=2)).strftime("%Y%m%d")
    endpoint = f"/api/v1/prices/electricity/?zone=NO1&date={tomorrow}"
    response = authenticated_client.get(endpoint)

    assert response.status_code == 400
    assert response.json()["detail"] == "Price data is available for tomorrow after 14:00"

    time_now = datetime.now().strftime("%H%M")

    if time_now < "1400":
        tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y%m%d")
        endpoint = f"/api/v1/prices/electricity/?zone=NO1&date={tomorrow}"
        print(endpoint)
        response = authenticated_client.get(endpoint)

        assert response.status_code == 400
        assert response.json()["detail"] == "Price data is available for tomorrow after 14:00"


def test_zones(authenticated_client):
    """ Test valid and invalid bidding zones """
    valid_zone = "NO1"
    today = datetime.today().strftime("%Y%m%d")
    endpoint = f"/api/v1/prices/electricity/?zone={valid_zone}&date={today}"
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200

    invalid_zone = "DE7"
    endpoint = f"/api/v1/prices/electricity/?zone={invalid_zone}&date={today}"
    response = authenticated_client.get(endpoint)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid zone. Valid zones are: NO1, NO2, NO3, NO4, NO5."


def test_elprice_calculation(authenticated_client):
    """ Test that the price * currency computation is correct """
    # TODO: Figure out how to test this AND adjust when moving calculation to new endpoint
    pass
