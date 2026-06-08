from datetime import date, timedelta
from pathlib import Path
from models import Category, Event
from weather import WeatherDay
from generator import generate, DayView

TODAY = date.today()


def _make_event(title="Test Event", days=1, is_free=False) -> Event:
    return Event(
        title=title, date=TODAY + timedelta(days=days),
        time="7pm", venue="Downtown", description="",
        category=Category.MUSIC, url="https://example.com/event",
        is_free=is_free, price="$10", source="test"
    )


def test_generate_creates_docs_index(tmp_path):
    events = [_make_event()]
    weather = {TODAY + timedelta(days=1): WeatherDay(high=78, low=58, icon="☀️", condition="Sunny")}
    output = tmp_path / "index.html"
    generate(events, weather, output_path=output)
    assert output.exists()


def test_generate_html_contains_event_title(tmp_path):
    events = [_make_event(title="Jazz Night")]
    weather = {}
    output = tmp_path / "index.html"
    generate(events, weather, output_path=output)
    assert "Jazz Night" in output.read_text()


def test_generate_html_contains_free_badge(tmp_path):
    events = [_make_event(is_free=True)]
    weather = {}
    output = tmp_path / "index.html"
    generate(events, weather, output_path=output)
    assert "FREE" in output.read_text()


def test_generate_html_contains_weather(tmp_path):
    events = [_make_event()]
    weather = {TODAY + timedelta(days=1): WeatherDay(high=78, low=58, icon="☀️", condition="Sunny")}
    output = tmp_path / "index.html"
    generate(events, weather, output_path=output)
    html = output.read_text()
    assert "Sunny" in html
    assert "78" in html


def test_generate_html_contains_share_button(tmp_path):
    events = [_make_event()]
    weather = {}
    output = tmp_path / "index.html"
    generate(events, weather, output_path=output)
    assert "shareEvent" in output.read_text()


def test_generate_html_links_to_original_url(tmp_path):
    events = [_make_event()]
    weather = {}
    output = tmp_path / "index.html"
    generate(events, weather, output_path=output)
    assert "https://example.com/event" in output.read_text()
