from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
from scrapers.sacramento365 import scrape, parse_events

FIXTURE = Path(__file__).parent / "fixtures" / "sacramento365.html"

def test_parse_finds_two_events():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    assert len(parse_events(soup)) == 2

def test_parse_event_title():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    assert parse_events(soup)[0].title == "Riverfront Summer Concert"

def test_parse_event_url():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    assert parse_events(soup)[0].url == "https://sacramento365.com/event/riverfront-concert/"

def test_parse_free_event():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    assert parse_events(soup)[0].is_free is True

def test_scrape_returns_empty_on_failure():
    with patch("scrapers.sacramento365.get_page", return_value=None):
        assert scrape() == []
