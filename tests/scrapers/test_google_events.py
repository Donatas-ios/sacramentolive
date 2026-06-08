from pathlib import Path
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from scrapers.google_events import scrape, parse_events

FIXTURE = Path(__file__).parent / "fixtures" / "google_events.html"


def test_parse_events_returns_list():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    assert isinstance(events, list)


def test_parse_events_finds_jazz_festival():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    titles = [e.title for e in events]
    assert "Sacramento Jazz Festival" in titles


def test_parse_events_free_flag():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    jazz = next(e for e in events if "Jazz" in e.title)
    assert jazz.is_free is True


def test_parse_events_paid_event():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    beer = next(e for e in events if "Beer" in e.title)
    assert beer.is_free is False
    assert beer.price == "$10"


def test_parse_events_url_is_original():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    jazz = next(e for e in events if "Jazz" in e.title)
    assert jazz.url == "https://www.sacjazz.com/tickets"


def test_scrape_returns_list_on_network_failure():
    with patch("scrapers.google_events.get_page", return_value=None):
        result = scrape()
    assert result == []
