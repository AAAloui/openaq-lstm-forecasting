import os, pytest 
import pandas as pd
from etl.ingest.fetch_openaq_sample import fetch_openaq_data

from etl.ingest.ingest_pm25_lyon_centre import fetch_sensor_data

def test_missing_api_key():
    """Should raise EnvironmentError if API key is not set"""
    if "OPENAQ_API_KEY" in os.environ:
        del os.environ["OPENAQ_API_KEY"]
    with pytest.raises(EnvironmentError):
        fetch_sensor_data(sensor_id=8559)


# def test_fetch_openaq_data_returns_dataframe():
#     df = fetch_openaq_data("Paris", "pm25", limit=100)
#     assert isinstance(df, pd.DataFrame)
#     assert not df.empty
#     assert "value" in df.columns
