from time import sleep

COIN_GECKO_SLEEP_TIME = 3

def test_get_btc_to_nok(authenticated_client):
    """ Test that we can get the BTC to NOK price """
    endpoint = "http://localhost:8000/api/v1/prices/crypto?coin=btc&currency=nok"
    sleep(COIN_GECKO_SLEEP_TIME)
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200


def test_currency_is_none(authenticated_client):
    """ Test that we can omit the currency """
    endpoint = "http://localhost:8000/api/v1/prices/crypto?coin=btc"
    sleep(COIN_GECKO_SLEEP_TIME)
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200


def test_supported_currency(authenticated_client):
    """ Test that we can identify supported currency other than default nok """
    endpoint = "http://localhost:8000/api/v1/prices/crypto?coin=btc&currency=usd"
    sleep(COIN_GECKO_SLEEP_TIME)
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200


def test_unsupported_currency(authenticated_client):
    """ Test that we handle unsupported currency requests """
    endpoint = "http://localhost:8000/api/v1/prices/crypto?coin=btc&currency=bengazi"
    sleep(COIN_GECKO_SLEEP_TIME)
    response = authenticated_client.get(endpoint)

    assert response.status_code == 400
    assert response.json()["detail"] == "Currency not supported"


def test_unsupported_coin(authenticated_client):
    """ Test that we can handle unsupported coin requests """
    endpoint = "http://localhost:8000/api/v1/prices/crypto?coin=troikabønner&currency=nok"
    sleep(COIN_GECKO_SLEEP_TIME)
    response = authenticated_client.get(endpoint)

    assert response.status_code == 400