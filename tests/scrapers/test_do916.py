from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
from scrapers.do916 import scrape, parse_events

FIXTURE = Path(__file__).parent / "fixtures" / "do916.html"

def test_parse_finds_two_events():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    assert len(parse_events(soup)) == 2

def test_parse_event_title():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    assert events[0].title == "Midtown Gallery Opening"

def test_parse_event_url():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    assert events[0].url == "https://do916.com/events/gallery-opening-june15"

def test_parse_free_event():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    assert events[0].is_free is True

def test_scrape_returns_empty_on_failure():
    with patch("scrapers.do916.get_page", return_value=None):
        assert scrape() == []
