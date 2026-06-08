from __future__ import annotations
import logging
from datetime import date, datetime
from bs4 import BeautifulSoup
from models import Event, infer_category
from scrapers.base import get_page, parse_price

logger = logging.getLogger(__name__)
_URL = "https://www.sacbee.com/entertainment/"

def parse_events(soup: BeautifulSoup) -> list[Event]:
    events: list[Event] = []
    for article in soup.select("article.event-card"):
        try:
            link = article.select_one("h2.event-card__headline a")
            if not link:
                continue
            title = link.get_text(strip=True)
            url = link.get("href", "")
            time_el = article.select_one("time.event-card__date")
            date_str = time_el.get("datetime", "") if time_el else ""
            event_date = _parse_date(date_str)
            if event_date is None:
                continue
            time_text_el = article.select_one("span.event-card__time")
            time_text = time_text_el.get_text(strip=True) if time_text_el else ""
            venue_el = article.select_one("span.event-card__location")
            venue = venue_el.get_text(strip=True) if venue_el else ""
            price_el = article.select_one("span.event-card__price")
            price_text = price_el.get_text(strip=True) if price_el else ""
            is_free, price = parse_price(price_text)
            events.append(Event(
                title=title, date=event_date, time=time_text,
                venue=venue, description="",
                category=infer_category(title, ""),
                url=url, is_free=is_free, price=price,
                source="sacbee",
            ))
        except Exception as exc:
            logger.warning("Error parsing SacBee event: %s", exc)
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
