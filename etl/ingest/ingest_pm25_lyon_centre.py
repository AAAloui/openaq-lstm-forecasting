import os
import requests
import pandas as pd


def fetch_sensor_data(sensor_id, limit=100):
    api_key = os.getenv("OPENAQ_API_KEY")
    if not api_key:
        raise EnvironmentError("Please set the OPENAQ_API_KEY environment variable.")

    url = (
        f"https://api.openaq.org/v3/sensors/{sensor_id}/hours"
        "?datetime_from=2025-05-13&datetime_to=2025-05-14"
    )
    headers = {"x-api-key": api_key}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 401:
            raise PermissionError("Unauthorized: Check your API key (401).")
        elif response.status_code == 403:
            raise PermissionError(
                "Forbidden: You don't have permission to access this resource \
                    (403)."
            )
        elif response.status_code == 422:
            raise ValueError(
                "Unprocessable Entity: The server could not process your \
                    request (422)."
            )
        elif response.status_code == 502:
            raise ConnectionError("Bad Gateway: OpenAQ server error (502).")

        response.raise_for_status()

        data = response.json()
        if "results" not in data:
            raise ValueError("No 'results' key in the response.")

        measurements = [
            {
                "value": item["value"],
                "datetime_from_utc": item["period"]["datetimeFrom"]["utc"],
                "datetime_to_utc": item["period"]["datetimeTo"]["utc"],
            }
            for item in data["results"]
        ]

        return pd.DataFrame(measurements)

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")


if __name__ == "__main__":
    sensor_id = 8559
    df = fetch_sensor_data(sensor_id, limit=100)
    df.to_csv("data/raw/sensor_output.csv", index=False)
