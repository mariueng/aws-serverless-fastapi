from datetime import datetime, timedelta


def test_get_exchange_rate(authenticated_client):
    """ Test that we can retrieve floating point exchange rate """
    today = datetime.today().strftime("%Y%m%d")
    endpoint = f"/api/v1/prices/currency/?from_currency=USD&to_currency=NOK&date={today}"
    response = authenticated_client.get(endpoint)
    status_code = response.status_code
    body = response.json()

    assert status_code == 200, f"Expected status code 200, got {status_code}"
    assert type(body) == float, f"Expected type float, got {type(body)}"
