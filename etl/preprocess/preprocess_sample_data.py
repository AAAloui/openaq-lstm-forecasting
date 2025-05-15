import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
import joblib

# Paths
INPUT_PATH = "data/raw/openaq_paris_pm25.csv"
OUTPUT_PATH = "data/processed/processed_paris_pm25.csv"
SCALER_PATH = "models/minmax_scaler.pkl"


def load_data(filepath):
    print(f"Loading data from {filepath}")
    return pd.read_csv(filepath, parse_dates=["datetime"])


def clean_and_prepare(df):
    # Drop rows with missing values
    df.dropna(subset=["value", "datetime"], inplace=True)

    # Set datetime as index
    df.set_index("datetime", inplace=True)
    df.sort_index(inplace=True)

    # Resample to hourly if needed
    df = df.resample("1H").mean()

    # Fill remaining NaNs (optional)
    df.fillna(method="ffill", inplace=True)

    return df


def scale_data(df):
    scaler = MinMaxScaler(feature_range=(0, 1))
    values = df.values.reshape(-1, 1)  # reshape for scaler
    scaled = scaler.fit_transform(values)
    df_scaled = pd.DataFrame(scaled, index=df.index, columns=["pm25_scaled"])

    return df_scaled, scaler


def save_outputs(df, scaler):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(SCALER_PATH), exist_ok=True)

    df.to_csv(OUTPUT_PATH)
    joblib.dump(scaler, SCALER_PATH)

    print(f"Saved processed data to {OUTPUT_PATH}")
    print(f"Saved scaler to {SCALER_PATH}")


if __name__ == "__main__":
    df_raw = load_data(INPUT_PATH)
    df_clean = clean_and_prepare(df_raw)
    df_scaled, scaler = scale_data(df_clean)
    save_outputs(df_scaled, scaler)
