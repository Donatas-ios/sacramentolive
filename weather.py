from __future__ import annotations
from dataclasses import dataclass
from datetime import date
import requests

_WMO_MAP: list[tuple[set[int], str, str]] = [
    ({0},                       "☀️",  "Sunny"),
    ({1},                       "🌤️", "Mainly Clear"),
    ({2},                       "⛅",  "Partly Cloudy"),
    ({3},                       "☁️",  "Overcast"),
    ({45, 48},                  "🌫️", "Foggy"),
    ({51, 53, 55},              "🌦️", "Drizzle"),
    ({61, 63, 65},              "🌧️", "Rainy"),
    ({71, 73, 75, 77},          "🌨️", "Snowy"),
    ({80, 81, 82},              "🌧️", "Showers"),
    ({85, 86},                  "🌨️", "Snow Showers"),
    ({95, 96, 99},              "⛈️",  "Thunderstorm"),
]

_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=38.5816&longitude=-121.4944"
    "&daily=temperature_2m_max,temperature_2m_min,weather_code"
    "&temperature_unit=fahrenheit"
    "&timezone=America%2FLos_Angeles"
    "&forecast_days=14"
)


@dataclass
class WeatherDay:
    high: int
    low: int
    icon: str
    condition: str


def _wmo_to_weather(code: int) -> tuple[str, str]:
    for codes, icon, condition in _WMO_MAP:
        if code in codes:
            return icon, condition
    return "🌡️", "Unknown"


def parse_weather_response(data: dict) -> dict[date, WeatherDay]:
    daily = data["daily"]
    result: dict[date, WeatherDay] = {}
    for iso, hi, lo, code in zip(
        daily["time"],
        daily["temperature_2m_max"],
        daily["temperature_2m_min"],
        daily["weather_code"],
    ):
        icon, condition = _wmo_to_weather(int(code))
        result[date.fromisoformat(iso)] = WeatherDay(
            high=round(hi), low=round(lo), icon=icon, condition=condition
        )
    return result


def fetch_forecast() -> dict[date, WeatherDay]:
    resp = requests.get(_URL, timeout=10)
    resp.raise_for_status()
    return parse_weather_response(resp.json())
