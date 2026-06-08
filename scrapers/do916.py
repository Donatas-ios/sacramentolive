from __future__ import annotations
import logging
from datetime import date, datetime
from bs4 import BeautifulSoup
from models import Event, infer_category
from scrapers.base import get_page, parse_price

logger = logging.getLogger(__name__)
_URL = "https://do916.com/events"

def parse_events(soup: BeautifulSoup) -> list[Event]:
    events: list[Event] = []
    for item in soup.select("div.event-item"):
        try:
            link = item.select_one("h3.event-title a")
            if not link:
                continue
            title = link.get_text(strip=True)
            url = link.get("href", "")
            date_el = item.select_one("div.event-date")
            date_str = date_el.get("data-date", "") if date_el else ""
            event_date = _parse_date(date_str)
            if event_date is None:
                continue
            time_el = item.select_one("div.event-time")
            time_text = time_el.get_text(strip=True) if time_el else ""
            venue_el = item.select_one("div.event-venue")
            venue = venue_el.get_text(strip=True) if venue_el else ""
            price_el = item.select_one("div.event-price")
            price_text = price_el.get_text(strip=True) if price_el else ""
            is_free, price = parse_price(price_text)
            events.append(Event(
                title=title, date=event_date, time=time_text,
                venue=venue, description="",
                category=infer_category(title, ""),
                url=url, is_free=is_free, price=price,
                source="do916",
            ))
        except Exception as exc:
            logger.warning("Error parsing Do916 event: %s", exc)
    return events

def _parse_date(text: str) -> date | None:
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None

def scrape() -> list[Event]:
    soup = get_page(_URL)
    if soup is None:
        return []
    return parse_events(soup)
