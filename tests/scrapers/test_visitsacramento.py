from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
from scrapers.visitsacramento import scrape, parse_events

FIXTURE = Path(__file__).parent / "fixtures" / "visitsacramento.html"

def test_parse_finds_both_events():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    assert len(events) == 2

def test_parse_event_title():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    assert events[0].title == "Farm to Fork Festival"

def test_parse_event_url_is_original():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    assert events[0].url == "https://visitsacramento.com/events/farm-to-fork-2026/"

def test_parse_free_event():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    assert events[0].is_free is True

def test_scrape_returns_empty_on_failure():
    with patch("scrapers.visitsacramento.get_page", return_value=None):
        assert scrape() == []
