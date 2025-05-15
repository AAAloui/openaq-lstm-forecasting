import pandas as pd


def classify_wind_direction(degrees):
    if pd.isnull(degrees):
        return "N/A"
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    ix = int((degrees + 22.5) // 45) % 8
    return dirs[ix]


# Load the files
aq_df = pd.read_csv("data/raw/sensor_output.csv",\
                    parse_dates=["datetime_from_utc"])
wx_df = pd.read_csv("data/raw/hourly_weather_lyon_centre.csv", \
                    parse_dates=["date"])

# Standardize timestamp for join
aq_df["timestamp"] = aq_df["datetime_from_utc"].dt.floor("h")
wx_df["timestamp"] = wx_df["date"].dt.floor("h")

# Join on timestamp
df = pd.merge(aq_df, wx_df, on="timestamp", how="inner")

# Feature engineering
df["No"] = range(1, len(df) + 1)
df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month
df["day"] = df["timestamp"].dt.day
df["hour"] = df["timestamp"].dt.hour
df["pm2.5"] = df["value"]
df["TEMP"] = df["temperature_2m"]
df["DEWP"] = df["dew_point_2m"]
df["PRES"] = df["surface_pressure"]
df["Iws"] = df["wind_speed_10m"]
df["cbwd"] = df["wind_direction_10m"].\
    apply(lambda deg: classify_wind_direction(deg))
df["Is"] = df["snowfall"].apply(lambda x: 1 if x > 0 else 0)
df["Ir"] = df["rain"].apply(lambda x: 1 if x > 0 else 0)

# Select only the required columns
final = df[
    [
        "No",
        "year",
        "month",
        "day",
        "hour",
        "pm2.5",
        "DEWP",
        "TEMP",
        "PRES",
        "cbwd",
        "Iws",
        "Is",
        "Ir",
    ]
]

# Save final dataset
final.to_csv("data/processed/full_training_dataset.csv", index=False)
