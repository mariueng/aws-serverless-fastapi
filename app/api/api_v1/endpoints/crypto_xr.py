from typing import Union
import requests

from fastapi import APIRouter, HTTPException, Response

router = APIRouter()

BASE_URL = "https://api.coingecko.com/api/v3"

@router.get("/crypto")
async def get_crypto_prices(coin: str, currency: Union[str, None]) -> Response:
    """
    Get real-time crypto prices from CoinGecko

    Args:

    - **crypto** (str): crypto currency name. Can be a single coin, e.g. "eth" or multiple coins, e.g. "eth,btc"
    - **currency** (str): currency to convert to. If not specified, will return prices in NOK.

    Returns:

    - **Response**: JSON price data in local currency
    """

    # Defaults to NOK. TODO: Update as input (?)
    if currency is None:
        vs_currencies = "nok"
    else:
        response = requests.get(BASE_URL + "/simple/supported_vs_currencies")
        supported_vs_currencies = response.json()
        if currency not in supported_vs_currencies:
            raise HTTPException(status_code=400, detail="Currency not supported")
        vs_currencies = currency
    vs_currencies = vs_currencies.lower()

    # Check for multiple coins
    if "," in coin:
        coin_symbols = coin.split(",")
    else:
        coin_symbols = [coin]

    # Get id for coin symbol(s)
    response = requests.get(BASE_URL + "/coins/list")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    all_coins = response.json()
    coin_ids = [coin_dict["id"] for coin_dict in all_coins if coin_dict["symbol"] in coin_symbols]

    # Hacky way to remove wormhole coins from list. TODO: Variable based.
    coin_ids = [coin_id for coin_id in coin_ids if "wormhole" not in coin_id]

    # Get prices for coin(s)
    _url = BASE_URL + "/simple/price?ids=%s&vs_currencies=%s" % (",".join(coin_ids), vs_currencies)
    response = requests.get(_url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
