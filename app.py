import os
import requests
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

from dotenv import load_dotenv

load_dotenv()

def get_weather():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	    "latitude": 55.7426,
	    "longitude": 37.7778,
	    "daily": ["temperature_2m_max", "apparent_temperature_max", "daylight_duration", "uv_index_max", "precipitation_sum"]
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_relative_humidity_2m = current.Variables(0).Value()
    current_apparent_temperature = current.Variables(1).Value()
    current_precipitation = current.Variables(2).Value()

    
    # daily_dataframe = pd.DataFrame(data = daily_data)
    # return daily_dataframe.to_string(index=None)
    return [
            f"Current time {current.get('time')}",
            f"Current relative_humidity_2m {current_relative_humidity_2m}",
            f"Current apparent_temperature {current_apparent_temperature}",
            f"Current precipitation {current_precipitation}"
        ]

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
