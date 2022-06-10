import math
import requests
import xmltodict
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Response, status

nb_url = "https://data.norges-bank.no/api/data/EXR/B.%s.%s.SP?format=sdmx-generic-2.1&startPeriod=%s&endPeriod=%s&locale=en"

router = APIRouter()


@router.get("/currency")
def get_exchange_rates(from_currency: str, to_currency: str, date: str) -> Response:
    """
    Returns the exchange rate for a given currency and date.
    args:
        from_currency (str): Currency to convert from (e.g. NOK)
        to_currency (str): Currency to convert to (e.g. USD)
        date (datetime): Date to convert (e.g. 2020-01-01)
    returns:
        Response: JSON with exchange rate for currency and date
    """
    end_date = datetime.strptime(date, '%Y-%m-%d')

    if from_currency == to_currency:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Currency cannot be the same.")
    if end_date.date() > datetime.now().date():
        end_date = datetime.now()
    # TODO: Check for available currencies (?)

    # Construct URL
    start_date = (end_date - timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    _url = nb_url % (from_currency, to_currency, start_date, end_date)

    # Fetch data
    response = requests.get(_url)

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not fetch data from Norges Bank API")

    # Parse data
    dict_xml: dict = xmltodict.parse(response.content)
    series = dict_xml['message:GenericData']['message:DataSet']['generic:Series']
    values = series['generic:Attributes']['generic:Value']

    multiplicator: int
    for attr in values:
        if attr['@id'] == 'UNIT_MULT':
            multiplicator = int(attr['@value'])

    observations = series['generic:Obs']

    try:
        res = float(observations[len(observations) - 1]['generic:ObsValue']['@value']) / math.pow(10, multiplicator)
    except RuntimeError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not calculate exchange rate")

    return Response(content=str(res), status_code=status.HTTP_200_OK)
