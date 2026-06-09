from __future__ import annotations
import json
import logging
import re
from datetime import date, datetime, timedelta

from bs4 import BeautifulSoup
from models import Event, infer_category

logger = logging.getLogger(__name__)

_URL = "https://www.eventbrite.com/d/ca--sacramento/events/"
_TODAY = None  # patched in tests


def _today() -> date:
    return _TODAY or date.today()


def _parse_price(text: str) -> tuple[bool, str]:
    if re.search(r'\bfree\b', text, re.IGNORECASE):
        return True, ""
    if re.search(r'From\s*\$0\.00', text, re.IGNORECASE):
        return True, ""
    m = re.search(r'From\s*(\$[\d.]+)', text, re.IGNORECASE)
    if m:
        return False, m.group(1)
    m2 = re.search(r'(\$[\d]+(?:\.\d+)?(?:\s*[-–]\s*\$[\d]+(?:\.\d+)?)?)', text)
    if m2:
        return False, m2.group(1)
    return False, ""


def scrape() -> list[Event]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.warning("playwright not installed, skipping Eventbrite")
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
            page.goto(_URL, wait_until="networkidle", timeout=30000)
            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "lxml")

        # Build URL -> card text map for price/time/venue extraction
        url_to_card: dict[str, str] = {}
        for a in soup.select('a[href*="eventbrite.com/e/"]'):
            url = a.get("href", "").split("?")[0]
            if url in url_to_card:
                continue
            card = a
            for _ in range(8):
                card = card.parent
                text = card.get_text(separator=" | ", strip=True)
                if len(text) > 40:
                    url_to_card[url] = text
                    break

        # Parse events from JSON-LD (reliable source of title/date/venue)
        jsonld_blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL
        )
        for block in jsonld_blocks:
            try:
                data = json.loads(block)
                items = data.get("itemListElement", [])
                if not items:
                    continue
                for item in items:
                    try:
                        raw = item.get("item", item)
                        date_str = raw.get("startDate", "")
                        if not date_str:
                            continue
                        event_date = date.fromisoformat(date_str[:10])
                        if event_date < today or event_date > cutoff:
                            continue

                        time_str = ""
                        if len(date_str) > 10:
                            try:
                                dt = datetime.fromisoformat(date_str)
                                time_str = dt.strftime("%-I:%M %p")
                            except ValueError:
                                pass

                        title = raw.get("name", "")
                        url = raw.get("url", "").split("?")[0]
                        if not title or not url:
                            continue

                        location = raw.get("location", {})
                        addr = location.get("address", {})
                        venue = location.get("name", addr.get("addressLocality", "Sacramento"))

                        # Enrich with price/time from card DOM
                        card_text = url_to_card.get(url, "")
                        is_free, price = _parse_price(card_text)

                        # Better time from card if available
                        if card_text and not time_str:
                            t_match = re.search(
                                r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\w*\s*[•·]\s*(\d+:\d+\s*[AP]M)',
                                card_text, re.IGNORECASE
                            )
                            if t_match:
                                time_str = t_match.group(1).strip()

                        events.append(Event(
                            title=title,
                            date=event_date,
                            time=time_str,
                            venue=venue,
                            description="",
                            category=infer_category(title, ""),
                            url=url,
                            is_free=is_free,
                            price=price,
                            source="eventbrite",
                        ))
                    except Exception as e:
                        logger.warning("Failed to parse Eventbrite event: %s", e)
                return events  # only process first matching block
            except (json.JSONDecodeError, AttributeError):
                continue

    except Exception as e:
        logger.warning("Eventbrite Playwright scrape failed: %s", e)

    return events
