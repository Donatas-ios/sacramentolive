from __future__ import annotations
import json
import logging
import re
from datetime import date, datetime, timedelta

from models import Event, infer_category

logger = logging.getLogger(__name__)

_URL = "https://www.eventbrite.com/d/ca--sacramento/events/"
_TODAY = None  # patched in tests


def _today() -> date:
    return _TODAY or date.today()


def _parse_events(items: list[dict]) -> list[Event]:
    today = _today()
    cutoff = today + timedelta(days=14)
    events: list[Event] = []

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
            url = raw.get("url", "")
            if url and "?" in url:
                url = url.split("?")[0]

            description = raw.get("description", "")
            if len(description) > 200:
                description = description[:200]

            location = raw.get("location", {})
            addr = location.get("address", {})
            venue_name = location.get("name", addr.get("addressLocality", "Sacramento"))

            is_free = raw.get("isAccessibleForFree", False)
            price = ""
            offers = raw.get("offers", {})
            if isinstance(offers, dict):
                low = offers.get("lowPrice")
                high = offers.get("highPrice")
                if low is not None:
                    if float(low) == 0:
                        is_free = True
                    elif low == high or high is None:
                        price = f"${float(low):.0f}"
                    else:
                        price = f"${float(low):.0f}–${float(high):.0f}"

            category = infer_category(title, description)

            events.append(Event(
                title=title,
                date=event_date,
                time=time_str,
                venue=venue_name,
                description=description,
                category=category,
                url=url,
                is_free=is_free,
                price=price,
                source="eventbrite",
            ))
        except Exception as e:
            logger.warning("Failed to parse Eventbrite event: %s", e)

    return events


def scrape() -> list[Event]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.warning("playwright not installed, skipping Eventbrite")
        return []

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

        jsonld_blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL
        )
        for block in jsonld_blocks:
            try:
                data = json.loads(block)
                items = data.get("itemListElement", [])
                if items:
                    return _parse_events(items)
            except (json.JSONDecodeError, AttributeError):
                continue

    except Exception as e:
        logger.warning("Eventbrite Playwright scrape failed: %s", e)

    return []
