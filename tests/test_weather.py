from datetime import date
from unittest.mock import patch, MagicMock
from weather import WeatherDay, parse_weather_response, fetch_forecast

MOCK_API_RESPONSE = {
    "daily": {
        "time": ["2026-06-08", "2026-06-09"],
        "temperature_2m_max": [78.4, 82.1],
        "temperature_2m_min": [58.2, 61.0],
        "weathercode": [0, 3]
    }
}


def test_parse_weather_response_returns_dict_keyed_by_date():
    result = parse_weather_response(MOCK_API_RESPONSE)
    assert date(2026, 6, 8) in result
    assert date(2026, 6, 9) in result


def test_parse_weather_response_high_low():
    result = parse_weather_response(MOCK_API_RESPONSE)
    assert result[date(2026, 6, 8)].high == 78
    assert result[date(2026, 6, 8)].low == 58


def test_parse_weather_response_clear_sky():
    result = parse_weather_response(MOCK_API_RESPONSE)
    day = result[date(2026, 6, 8)]
    assert day.icon == "☀️"
    assert "Sunny" in day.condition


def test_parse_weather_response_overcast():
    result = parse_weather_response(MOCK_API_RESPONSE)
    day = result[date(2026, 6, 9)]
    assert day.icon == "☁️"


def test_fetch_forecast_calls_open_meteo():
    mock_resp = MagicMock()
    mock_resp.json.return_value = MOCK_API_RESPONSE
    mock_resp.raise_for_status.return_value = None
    with patch("weather.requests.get", return_value=mock_resp) as mock_get:
        result = fetch_forecast()
    mock_get.assert_called_once()
    call_url = mock_get.call_args[0][0]
    assert "api.open-meteo.com" in call_url
    assert "38.5816" in call_url
    assert isinstance(result, dict)
