from __future__ import annotations
import logging
from datetime import date, datetime
from bs4 import BeautifulSoup
from models import Event, infer_category
from scrapers.base import get_page, parse_price

logger = logging.getLogger(__name__)
_URL = "https://www.eventbrite.com/d/ca--sacramento/events/"

def parse_events(soup: BeautifulSoup) -> list[Event]:
    events: list[Event] = []
    for card in soup.select("a[data-testid='event-card-link']"):
        try:
            url = card.get("href", "")
            title_el = card.select_one("p[data-testid='event-card-title']")
            date_el = card.select_one("p[data-testid='event-card-date-time']")
            venue_el = card.select_one("p[data-testid='event-card-venue']")
            price_el = card.select_one("p[data-testid='event-card-price']")
            if not title_el or not date_el:
                continue
            title = title_el.get_text(strip=True)
            event_date, time_text = _parse_date_time(date_el.get_text(strip=True))
            if event_date is None:
                continue
            venue = venue_el.get_text(strip=True) if venue_el else ""
            price_text = price_el.get_text(strip=True) if price_el else ""
            is_free, price = parse_price(price_text)
            events.append(Event(
                title=title, date=event_date, time=time_text,
                venue=venue, description="",
                category=infer_category(title, ""),
                url=url, is_free=is_free, price=price,
                source="eventbrite",
            ))
        except Exception as exc:
            logger.warning("Error parsing Eventbrite card: %s", exc)
    return events

def _parse_date_time(text: str) -> tuple[date | None, str]:
    # e.g. "Sat, Jun 13, 1:00 PM"
    try:
        parts = text.split(",")
        if len(parts) >= 3:
            date_part = parts[1].strip() + " " + str(date.today().year)
            time_part = parts[2].strip()
            parsed = datetime.strptime(date_part, "%b %d %Y").date()
            today = date.today()
            if parsed < today:
                parsed = datetime.strptime(
                    parts[1].strip() + " " + str(today.year + 1), "%b %d %Y"
                ).date()
            return parsed, time_part
    except ValueError:
        pass
    return None, ""

def scrape() -> list[Event]:
    soup = get_page(_URL)
    if soup is None:
        return []
    return parse_events(soup)
