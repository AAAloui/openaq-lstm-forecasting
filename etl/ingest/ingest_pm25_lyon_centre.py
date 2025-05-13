import requests
import pandas as pd
import os

def fetch_sensor_data(sensor_id, limit=100):
    api_key = os.getenv("OPENAQ_API_KEY")
    if not api_key:
        raise EnvironmentError("Please set the OPENAQ_API_KEY environment variable.")

    # url = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements?limit={limit}"
    url = f"https://api.openaq.org/v3/sensors/{sensor_id}/hours?datetime_from=2025-05-13&datetime_to=2025-05-14"

    headers = {
        "x-api-key": api_key
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    if "results" not in data:
        raise ValueError("No 'results' key in the response.")

    measurements = [
        {
            'value': item['value'],
            'datetime_from_utc': item['period']['datetimeFrom']['utc'],
            'datetime_to_utc': item['period']['datetimeTo']['utc']
        }
        for item in data['results']
    ]

    return pd.DataFrame(measurements)

# Usage
sensor_id = 8559  # or 12345, etc.
df = fetch_sensor_data(sensor_id, limit=100)

# Save and download CSV
df.to_csv("data/raw/sensor_output.csv", index=False)
