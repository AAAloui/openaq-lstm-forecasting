import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to 
# assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 45.757731999933235,
    "longitude": 4.854214000165473,
    "hourly": [
        "temperature_2m",
        "dew_point_2m",
        "surface_pressure",
        "wind_direction_10m",
        "wind_speed_10m",
        "rain",
        "snowfall",
    ],
    "forecast_days": 16,
}
responses = openmeteo.weather_api(url, params=params)

response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_dew_point_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_surface_pressure = hourly.Variables(2).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(3).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
hourly_rain = hourly.Variables(5).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(6).ValuesAsNumpy()

hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left",
    )
}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["dew_point_2m"] = hourly_dew_point_2m
hourly_data["surface_pressure"] = hourly_surface_pressure
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["rain"] = hourly_rain
hourly_data["snowfall"] = hourly_snowfall

hourly_dataframe = pd.DataFrame(data=hourly_data)
# print(hourly_dataframe)

hourly_dataframe.to_csv("data/raw/hourly_weather_lyon_centre.csv", index=False)
