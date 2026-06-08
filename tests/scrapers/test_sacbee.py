from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
from scrapers.sacbee import scrape, parse_events

FIXTURE = Path(__file__).parent / "fixtures" / "sacbee.html"

def test_parse_finds_two_events():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    assert len(parse_events(soup)) == 2

def test_parse_event_title():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    assert parse_events(soup)[0].title == "Blues on the River"

def test_parse_event_url():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    assert "sacbee.com" in parse_events(soup)[0].url

def test_parse_free_event():
    soup = BeautifulSoup(FIXTURE.read_text(), "lxml")
    assert parse_events(soup)[0].is_free is True

def test_scrape_returns_empty_on_failure():
    with patch("scrapers.sacbee.get_page", return_value=None):
        assert scrape() == []
