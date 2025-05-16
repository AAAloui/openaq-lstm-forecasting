import pandas as pd
from etl.preprocess.preprocess_sample_data import clean_and_prepare, scale_data


def test_clean_and_prepare_removes_nans():
    """Test that the clean_and_prepare function removes NaN values."""
    df = pd.DataFrame({
        "datetime": pd.date_range("2024-01-01", periods=3, freq="H"),
        "value": [10, None, 30]
    })
    df_clean = clean_and_prepare(df)
    assert df_clean.isnull().sum().sum() == 0


def test_scale_data_output_range():
    """Test that the scale_data function scales values to the range [0, 1]."""
    df = pd.DataFrame({"value": [10, 20, 30]},
                      index=pd.date_range("2024-01-01", periods=3, freq="H"))
    df_scaled, scaler = scale_data(df)
    assert df_scaled["pm25_scaled"].min() >= 0
    assert df_scaled["pm25_scaled"].max() <= 1
