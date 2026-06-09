from __future__ import annotations
import logging
import re
from datetime import date, datetime, timedelta

from bs4 import BeautifulSoup
from models import Event, infer_category

logger = logging.getLogger(__name__)

_URL = "https://sacramento365.com/events/"
_TODAY = None  # patched in tests


def _today() -> date:
    return _TODAY or date.today()


def _parse_date_range(text: str) -> date | None:
    today = _today()
    text = text.strip()
    # For ranges like "May 12 - Jun 09, 2026", take start date
    range_match = re.match(r'(\w+ \d+)\s*[-–]', text)
    if range_match:
        year_match = re.search(r'\b(20\d\d)\b', text)
        year = int(year_match.group(1)) if year_match else today.year
        try:
            d = datetime.strptime(range_match.group(1), "%b %d").replace(year=year).date()
            return d
        except ValueError:
            pass

    for fmt in ("%b %d, %Y", "%B %d, %Y", "%b %d", "%B %d"):
        try:
            dt = datetime.strptime(text.rstrip(','), fmt)
            if '%Y' not in fmt:
                dt = dt.replace(year=today.year)
                if dt.date() < today:
                    dt = dt.replace(year=today.year + 1)
            return dt.date()
        except ValueError:
            continue
    return None


def scrape() -> list[Event]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.warning("playwright not installed, skipping Sacramento365")
        return []

    today = _today()
    cutoff = today + timedelta(days=14)
    events: list[Event] = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/124.0.0.0 Safari/537.36"
            )
            page.goto(_URL, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "lxml")
        cards = soup.select(".topten-item")

        for card in cards:
            try:
                link = card.select_one('a[href*="/event/"]')
                if not link:
                    continue
                url = link.get("href", "")

                title_el = card.select_one(".topten-title, h2, h3")
                title = title_el.get_text(strip=True) if title_el else ""
                if not title:
                    title = card.get_text(separator=" ", strip=True).split("|")[0].strip()
                if not title:
                    continue

                text = card.get_text(separator=" ", strip=True)
                date_match = re.search(
                    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*'
                    r'\s+\d+(?:\s*[-–]\s*(?:\w+\s+)?\d+)?,?\s*\d{4}',
                    text, re.IGNORECASE
                )
                if not date_match:
                    date_match = re.search(
                        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d+',
                        text, re.IGNORECASE
                    )
                if not date_match:
                    continue

                event_date = _parse_date_range(date_match.group(0))
                if not event_date or event_date < today or event_date > cutoff:
                    continue

                venue_match = re.search(r'\bat\b\s+(.+?)(?:\s*\||\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)|\s*$)', text)
                venue = venue_match.group(1).strip() if venue_match else "Sacramento"

                events.append(Event(
                    title=title,
                    date=event_date,
                    time="",
                    venue=venue,
                    description="",
                    category=infer_category(title, ""),
                    url=url,
                    is_free=False,
                    price="",
                    source="sacramento365",
                ))
            except Exception as e:
                logger.warning("Failed to parse Sacramento365 card: %s", e)

    except Exception as e:
        logger.warning("Sacramento365 Playwright scrape failed: %s", e)

    return events
