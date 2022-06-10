import os
import requests
import xmltodict
import json

from fastapi import status, Response, APIRouter, HTTPException
from datetime import datetime, timedelta
from pytz import timezone

from .currency_xr import get_exchange_rates

router = APIRouter()

entsoe_url = "https://transparency.entsoe.eu/api?documentType=A44&in_Domain=%s&out_Domain=%s&periodStart=%s2300&periodEnd=%s2300&securityToken=%s"

ZONES: dict = {
    "NO1": "10YNO-1--------2",
    "NO2": "10YNO-2--------T",
    "NO3": "10YNO-3--------J",
	"NO4": "10YNO-4--------9",
	"NO5": "10Y1001A1001A48H",
}

LOCAL_TZ = timezone("Europe/Oslo")
dawn_zero: datetime = datetime(2014, 12, 12, 0, 0, 0, tzinfo=LOCAL_TZ)


def is_valid_time_period(date_time: datetime) -> bool:
    """
    Checks if the time period is valid.
    """
    now: datetime = datetime.now(tz=LOCAL_TZ)
    start_of_today: datetime = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=LOCAL_TZ)
    tomorrow: datetime = start_of_today + timedelta(days=1)

    if date_time.date() < tomorrow.date():
        return True
    elif date_time.date() == tomorrow.date():
        return now > start_of_today + timedelta(hours=14)
    return False


@router.get("/electricity")
async def get_electricity_prices(zone: str, date_str: str) -> Response:
    """
    Endpoint that fetches data and calculates electricity prices for zone and date.
    args:
        zone (str): Bidding zone (e.g. NO1)
        date (str): Date in format YYYYMMDD
    returns:
        Response: JSON with electricity prices for zone and date
    """

    # Construct URL
    # TODO: Check that all inputs are sanitized (think they are...)
    _datetime: datetime = datetime.strptime(date_str, '%Y%m%d')
    _datetime: datetime = LOCAL_TZ.localize(_datetime)

    if not is_valid_time_period(_datetime):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price data is available for tomorrow after 14:00")

    if _datetime < dawn_zero:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price data before 2014-112-12 is unavailable")

    if zone not in ZONES:
        zones_str: str = ",".join(ZONES.keys())
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid zone. Valid zones are: {zones_str}.")

    start_date: str = str((_datetime - timedelta(days=1)).strftime('%Y%m%d'))
    end_date: str = str(_datetime.strftime('%Y%m%d'))
    _entsoe_url: str = entsoe_url % (ZONES[zone], ZONES[zone], start_date, end_date, os.getenv("ENTSOE_SECRET_KEY"))

    # Retrieve and parse data from Entsoe API
    response: Response = requests.get(_entsoe_url)

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not fetch data from Entsoe API")

    dict_xml: dict = xmltodict.parse(response.content)
    time_series = dict_xml['Publication_MarketDocument']['TimeSeries']

    # If the request is done late in the day, you might receive the forecast for the next next day as well.
    # TODO: Find a cleaner way to do this.
    if isinstance(time_series, list):
        # Choose the most recent period
        period = time_series[0]['Period']
    else:
        period = time_series['Period']

    # Get Exchange rate
    response = get_exchange_rates("EUR", "NOK", _datetime.strftime("%Y-%m-%d"))
    
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not obtain exchange rate")

    exchange_rate = float(response.body)

    # Calculate priceForecast
    time_series_forecast = {}

    # Get localized time
    start_date_wo_tz = period['timeInterval']['start']
    dt_obj = datetime.strptime(start_date_wo_tz, '%Y-%m-%dT%H:%M%z')
    loc_start_date = dt_obj.replace(tzinfo=timezone('UTC')).astimezone(timezone('Europe/Oslo'))

    for point in period['Point']:
        position = int(point['position'])
        price_amount = float(point['price.amount'])
        price_per_kwh = float(price_amount) / 1000
        start_period = loc_start_date + timedelta(hours=(position - 1))
        end_period = loc_start_date + timedelta(hours=(position))
        time_series_forecast[start_period.isoformat()] = {
            "price_per_kwh": round(price_per_kwh * exchange_rate, 4),
            "valid_from": start_period,
            "valid_to": end_period
        }

    return Response(
        content=json.dumps(time_series_forecast, indent=4, default=str), status_code=status.HTTP_200_OK)
