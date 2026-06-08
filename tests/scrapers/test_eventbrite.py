from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
from scrapers.eventbrite import scrape, parse_events

FIXTURE = Path(__file__).parent / "fixtures" / "eventbrite.html"

def test_parse_finds_two_events():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    assert len(parse_events(soup)) == 2

def test_parse_event_title():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    assert events[0].title == "Sacramento Craft Beer Festival"

def test_parse_event_url():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    assert "eventbrite.com/e/craft-beer-festival" in events[0].url

def test_parse_free_event():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    events = parse_events(soup)
    yoga = next(e for e in events if "Yoga" in e.title)
    assert yoga.is_free is True

def test_scrape_returns_empty_on_failure():
    with patch("scrapers.eventbrite.get_page", return_value=None):
        assert scrape() == []
