import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# Configuration
CITY = "Paris"
PARAMETER = "pm25"
LIMIT = 10000  # Max records per request
OUTPUT_DIR = "data/raw"
OUTPUT_FILE = f"{OUTPUT_DIR}/openaq_{CITY.lower()}_{PARAMETER}.csv"

def fetch_openaq_data(city, parameter, limit):
    url = "https://api.openaq.org/v2/measurements"
    params = {
        "city": city,
        "parameter": parameter,
        "limit": limit,
        "sort": "desc",
        "order_by": "datetime",
        "date_from": (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ"),  # last 7 days
        "date_to": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    print(f"Fetching data for {city}, parameter: {parameter}")
    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json()["results"]

    if not results:
        print("No data retrieved.")
        return None

    # Convert to DataFrame
    df = pd.DataFrame(results)
    df = df[["location", "parameter", "value", "unit", "date", "coordinates"]]
    df["datetime"] = df["date"].apply(lambda x: x["utc"])
    df["latitude"] = df["coordinates"].apply(lambda x: x.get("latitude"))
    df["longitude"] = df["coordinates"].apply(lambda x: x.get("longitude"))
    df.drop(columns=["date", "coordinates"], inplace=True)
    return df

def save_to_csv(df, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Saved {len(df)} rows to {filepath}")

if __name__ == "__main__":
    df = fetch_openaq_data(CITY, PARAMETER, LIMIT)
    if df is not None:
        save_to_csv(df, OUTPUT_FILE)
