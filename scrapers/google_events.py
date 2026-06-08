from __future__ import annotations
import logging
from datetime import date, datetime
from bs4 import BeautifulSoup
from models import Event, infer_category
from scrapers.base import get_page, parse_price

logger = logging.getLogger(__name__)

_URL = "https://www.google.com/search?q=sacramento+events&ibp=htl;events"


def parse_events(soup: BeautifulSoup) -> list[Event]:
    events: list[Event] = []
    # Google events panel cards — class names may change; update if scraper breaks
    for card in soup.select("div.vwMtPb"):
        try:
            link = card.select_one("a.odIJnf")
            if not link:
                continue
            url = link.get("href", "")
            title_el = link.select_one("div.YOGjf")
            if not title_el:
                continue
            title_text = title_el.get_text(strip=True)

            details = [d.get_text(strip=True) for d in link.select("div.cEZxRc")]
            date_text = details[0] if len(details) > 0 else ""
            time_text = details[1] if len(details) > 1 else ""
            venue_text = details[2] if len(details) > 2 else ""

            price_el = link.select_one("div.pDavDe")
            price_text = price_el.get_text(strip=True) if price_el else ""
            is_free, price = parse_price(price_text)

            event_date = _parse_date(date_text)
            if event_date is None:
                continue

            events.append(Event(
                title=title_text,
                date=event_date,
                time=time_text,
                venue=venue_text,
                description="",
                category=infer_category(title_text, ""),
                url=url,
                is_free=is_free,
                price=price,
                source="google",
            ))
        except Exception as exc:
            logger.warning("Error parsing Google event card: %s", exc)
    return events


def _parse_date(text: str) -> date | None:
    for fmt in ("%A, %B %d", "%B %d", "%a, %b %d"):
        try:
            parsed = datetime.strptime(text, fmt)
            today = date.today()
            candidate = parsed.replace(year=today.year).date()
            if candidate < today:
                candidate = parsed.replace(year=today.year + 1).date()
            return candidate
        except ValueError:
            continue
    return None


def scrape() -> list[Event]:
    soup = get_page(_URL)
    if soup is None:
        return []
    return parse_events(soup)
