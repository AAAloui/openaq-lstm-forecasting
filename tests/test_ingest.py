import os 
import pytest
import requests
from unittest.mock import patch, MagicMock
from etl.ingest.ingest_pm25_lyon_centre import fetch_sensor_data


def test_missing_api_key():
    """Should raise EnvironmentError if API key is not set"""
    if "OPENAQ_API_KEY" in os.environ:
        del os.environ["OPENAQ_API_KEY"]
    with pytest.raises(EnvironmentError):
        fetch_sensor_data(sensor_id=8559)


def test_invalid_api_key():
    """Should raise PermissionError if API key is invalid"""
    os.environ["OPENAQ_API_KEY"] = "invalid_key"
    with pytest.raises(PermissionError):
        fetch_sensor_data(sensor_id=8559)


@patch("etl.ingest.fetch_openaq_sample.requests.get")
def test_unauthorized_api_key(mock_get):
    """Should raise PermissionError when API returns 401 Unauthorized"""
    os.environ["OPENAQ_API_KEY"] = "valid-but-unused-key"
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = None  # prevent automatic HTTPError
    mock_get.return_value = mock_response
    with pytest.raises(PermissionError, match="Unauthorized"):
        fetch_sensor_data(sensor_id=12345)


@patch("etl.ingest.fetch_openaq_sample.requests.get")
def test_unprocessable_entity(mock_get):
    """Should raise ValueError when API returns 422 Unprocessable Entity"""
    os.environ["OPENAQ_API_KEY"] = "valid-key"
    mock_response = MagicMock(status_code=422)
    mock_response.raise_for_status.side_effect = None
    mock_get.return_value = mock_response
    with pytest.raises(ValueError, match="Unprocessable"):
        fetch_sensor_data(sensor_id=999999)


@patch("etl.ingest.fetch_openaq_sample.requests.get")
def test_bad_gateway_error(mock_get):
    """Should raise ConnectionError when API returns 502 Bad Gateway"""
    os.environ["OPENAQ_API_KEY"] = "valid-key"
    mock_response = MagicMock(status_code=502)
    mock_response.raise_for_status.side_effect = None
    mock_get.return_value = mock_response
    with pytest.raises(ConnectionError, match="Bad Gateway"):
        fetch_sensor_data(sensor_id=8559)


@patch("etl.ingest.fetch_openaq_sample.requests.get")
def test_network_error(mock_get):
    """Should raise RuntimeError on network error"""
    os.environ["OPENAQ_API_KEY"] = "valid-key"
    mock_get.side_effect = requests.exceptions.RequestException("Timeout")

    with pytest.raises(RuntimeError, match="Request failed"):
        fetch_sensor_data(sensor_id=8559)


@patch("etl.ingest.fetch_openaq_sample.requests.get")
def test_empty_results_list(mock_get):
    """Should return an empty DataFrame if results list is empty"""
    os.environ["OPENAQ_API_KEY"] = "valid-key"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"results": []}
    mock_get.return_value = mock_response

    df = fetch_sensor_data(sensor_id=8559)
    assert df.empty


@patch("etl.ingest.fetch_openaq_sample.requests.get")
def test_successful_fetch(mock_get):
    """Should return a DataFrame with sensor data"""
    os.environ["OPENAQ_API_KEY"] = "valid-key"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [
            {
                "value": 18.0,
                "period": {
                    "datetimeFrom": {"utc": "2025-05-13T00:00:00Z"},
                    "datetimeTo": {"utc": "2025-05-13T01:00:00Z"},
                },
            }
        ]
    }
    mock_get.return_value = mock_response

    df = fetch_sensor_data(sensor_id=8559)
    assert not df.empty
    assert "value" in df.columns
    assert df.iloc[0]["value"] == 18.0
    assert set(df.columns) == {"value", "datetime_from_utc", "datetime_to_utc"}


# def test_fetch_openaq_data_returns_dataframe():
#     df = fetch_openaq_data("Paris", "pm25", limit=100)
#     assert isinstance(df, pd.DataFrame)
#     assert not df.empty
#     assert "value" in df.columns
