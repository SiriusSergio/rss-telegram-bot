import os
import requests
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

from dotenv import load_dotenv

load_dotenv()

def get_weather():
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
    	"latitude": 52.52,
    	"longitude": 13.41,
    	"current": "temperature_2m",
	    "timezone": "GMT",
	    "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process daily data. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()

    return current_temperature_2m

def send_message(message):

    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')

    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

    params = {
        'chat_id' : TELEGRAM_CHANNEL_ID,
        'text' : message
    }

    res = requests.post(url, params=params)
    res.raise_for_status()
    return res.json()


if __name__ == '__main__':
    weather = get_weather()
    send_message(weather)
