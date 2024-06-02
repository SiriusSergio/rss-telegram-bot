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

    # Process hourly data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_apparent_temperature_max = daily.Variables(1).ValuesAsNumpy()
    daily_daylight_duration = daily.Variables(2).ValuesAsNumpy()
    daily_uv_index_max = daily.Variables(3).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(4).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
    daily_data["daylight_duration"] = daily_daylight_duration
    daily_data["uv_index_max"] = daily_uv_index_max
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_dataframe = pd.DataFrame(data = daily_data)
    return daily_dataframe.to_string(index=None)

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
