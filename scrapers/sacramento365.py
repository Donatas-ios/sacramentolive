from __future__ import annotations
import logging
from datetime import date, datetime
from bs4 import BeautifulSoup
from models import Event, infer_category
from scrapers.base import get_page, parse_price

logger = logging.getLogger(__name__)
_URL = "https://sacramento365.com"

def parse_events(soup: BeautifulSoup) -> list[Event]:
    events: list[Event] = []
    for row in soup.select("div.views-row"):
        try:
            link = row.select_one("h3.field-content a")
            if not link:
                continue
            title = link.get_text(strip=True)
            url = link.get("href", "")
            date_el = row.select_one("span.date-display-single")
            date_text = date_el.get_text(strip=True) if date_el else ""
            event_date = _parse_date(date_text)
            if event_date is None:
                continue
            time_el = row.select_one("div.views-field-field-start-time")
            time_text = time_el.get_text(strip=True) if time_el else ""
            venue_el = row.select_one("div.views-field-field-location")
            venue = venue_el.get_text(strip=True) if venue_el else ""
            price_el = row.select_one("div.views-field-field-admission")
            price_text = price_el.get_text(strip=True) if price_el else ""
            is_free, price = parse_price(price_text)
            events.append(Event(
                title=title, date=event_date, time=time_text,
                venue=venue, description="",
                category=infer_category(title, ""),
                url=url, is_free=is_free, price=price,
                source="sacramento365",
            ))
        except Exception as exc:
            logger.warning("Error parsing Sacramento365 row: %s", exc)
    return events

def _parse_date(text: str) -> date | None:
    for fmt in ("%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None

def scrape() -> list[Event]:
    soup = get_page(_URL)
    if soup is None:
        return []
    return parse_events(soup)
