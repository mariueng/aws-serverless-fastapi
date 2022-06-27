from datetime import datetime


today = datetime.today().strftime("%Y%m%d")


def test_get_exchange_rate(authenticated_client):
    """ Test that we can retrieve floating point exchange rate """
    endpoint = f"/api/v1/prices/currency/?from_currency=USD&to_currency=NOK&date={today}"
    response = authenticated_client.get(endpoint)
    status_code = response.status_code
    body = response.json()

    assert status_code == 200, f"Expected status code 200, got {status_code}"
    assert type(body) == float, f"Expected type float, got {type(body)}"


def test_get_same_conversion(authenticated_client):
    """ Test that we can handle invalid same currency conversion requests """
    endpoint = f"/api/v1/prices/currency/?from_currency=USD&to_currency=USD&date={today}"
    response = authenticated_client.get(endpoint)
    status_code = response.status_code
    body = response.json()

    expected_status_code = 400
    assert status_code == expected_status_code, f"Expected status code {expected_status_code}, got {status_code}"
    expected_detail = "Currency can not be the same"
    assert body["detail"] == expected_detail, f"Expected body detail '{expected_detail}', got {body['detail']}"


def test_get_invalid_conversion(authenticated_client):
    """ Test that we can handle invalid currency conversion requests """
    endpoint = f"/api/v1/prices/currency/?from_currency=USD&to_currency=BENG&date={today}"
    response = authenticated_client.get(endpoint)
    status_code = response.status_code
    body = response.json()

    assert status_code == 400, f"Expected status code 400, got {status_code}"
    expected_detail = "Could not fetch data from Norges Bank API"
    assert body["detail"] == expected_detail, f"Expected body detail '{expected_detail}', got {body['detail']}"

