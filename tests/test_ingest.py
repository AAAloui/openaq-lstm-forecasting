import pandas as pd
from etl.ingest.fetch_openaq_sample import fetch_openaq_data

def test_fetch_openaq_data_returns_dataframe():
    df = fetch_openaq_data("Paris", "pm25", limit=100)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "value" in df.columns
