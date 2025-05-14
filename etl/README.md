# 🛠️ ETL Pipeline

This directory contains the ETL (Extract, Transform, Load) logic for the OpenAQ Air Quality Forecasting project. The goal is to build reproducible, scalable, and testable pipelines that prepare datasets for training, evaluation, and monitoring.

---

## 📁 Structure

```
etl/
├── ingest/
│ ├── fetch_openaq_sample.py # Pulls PM2.5 data from OpenAQ
│ ├── fetch_weather_sample.py # Pulls weather data (e.g. from Meteostat/Open-Meteo)
│
├── preprocess/
│ ├── merge_aq_weather.py # Joins OpenAQ and weather datasets into a unified format
│ ├── preprocess_sample_data.py # Cleans, scales, and prepares data for modeling 
```


---

## 🔄 Pipeline Stages

### 1. Ingest
Fetches raw hourly data from APIs and stores it in `data/raw/`.

- **Air Quality**: PM2.5 measurements from OpenAQ
- **Weather**: Temperature, dew point, pressure, wind speed/direction, rain, and snow

### 2. Merge
Combines air quality and weather datasets by timestamp, producing a single dataset aligned for training.

### 3. Preprocess
Cleans and prepares the data:
- Extracts year/month/day/hour from timestamps
- Categorizes wind direction
- Scales numerical values
- Outputs training-ready CSV files in `data/processed/`

---

## 🧪 Testing

ETL steps are covered by unit and data quality tests in the `/tests/` directory. These tests are run on every push via GitHub Actions.

