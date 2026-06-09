from __future__ import annotations
import logging
import os
import re
from datetime import date, datetime, timedelta

from models import Event, infer_category

logger = logging.getLogger(__name__)

_TODAY = None  # patched in tests

_SEARCHES = [
    "events in Sacramento CA this week",
    "events in Sacramento CA next week",
    "free events in Sacramento CA",
]


def _today() -> date:
    return _TODAY or date.today()


def _parse_date(date_info: dict) -> date | None:
    today = _today()
    start = date_info.get("start_date", "")
    when = date_info.get("when", "")

    # "Jun 11" or "Jun 11 – 13"
    for text in [start, when]:
        m = re.search(
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d+)',
            text, re.IGNORECASE
        )
        if m:
            for fmt in ("%b %d", "%B %d"):
                try:
                    dt = datetime.strptime(f"{m.group(1)} {m.group(2)}", fmt)
                    d = dt.replace(year=today.year).date()
                    if d < today - timedelta(days=1):
                        d = d.replace(year=today.year + 1)
                    return d
                except ValueError:
                    continue
    return None


def _parse_time(when: str) -> str:
    m = re.search(r'(\d+(?::\d+)?\s*[AP]M)', when, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def _best_url(ticket_info: list[dict], fallback: str) -> str:
    # Prefer "more info" links from the original venue over ticket resellers
    resellers = {"stubhub", "viagogo", "eventticketscenter", "rateyourseats", "tixel"}
    more_info = [t for t in ticket_info if t.get("link_type") == "more info"]
    tickets = [t for t in ticket_info if t.get("link_type") == "tickets"]

    for group in [more_info, tickets]:
        for t in group:
            url = t.get("link", "")
            source = t.get("source", "").lower()
            if not any(r in source for r in resellers):
                return url

    return fallback


def _scrape_query(api_key: str, query: str) -> list[dict]:
    try:
        from serpapi import GoogleSearch
        params = {
            "engine": "google_events",
            "q": query,
            "location": "Sacramento, California",
            "api_key": api_key,
            "num": "10",
        }
        results = GoogleSearch(params).get_dict()
        return results.get("events_results", [])
    except Exception as e:
        logger.warning("SerpAPI query '%s' failed: %s", query, e)
        return []


def scrape() -> list[Event]:
    api_key = os.environ.get("SERPAPI_KEY", "")
    if not api_key:
        logger.warning("SERPAPI_KEY not set, skipping")
        return []

    today = _today()
    cutoff = today + timedelta(days=14)
    seen_titles: set[str] = set()
    events: list[Event] = []

    for query in _SEARCHES:
        for item in _scrape_query(api_key, query):
            try:
                title = item.get("title", "").strip()
                if not title:
                    continue

                date_info = item.get("date", {})
                event_date = _parse_date(date_info)
                if not event_date or event_date < today or event_date > cutoff:
                    continue

                dedup_key = (title.lower(), event_date)
                if dedup_key in seen_titles:
                    continue
                seen_titles.add(dedup_key)

                time_str = _parse_time(date_info.get("when", ""))
                venue = item.get("venue", {}).get("name", "Sacramento")
                ticket_info = item.get("ticket_info", [])
                fallback_url = item.get("link", "")
                url = _best_url(ticket_info, fallback_url)

                # Free detection
                description = item.get("description", "")
                is_free = bool(re.search(r'\bfree\b', title + " " + description, re.IGNORECASE))
                price = ""
                if not is_free:
                    # Check ticket_info for price hints — SerpAPI doesn't always include price
                    # but "free" in source name is a signal
                    for t in ticket_info:
                        src = t.get("source", "").lower()
                        if "free" in src:
                            is_free = True
                            break

                category = infer_category(title, description)

                events.append(Event(
                    title=title,
                    date=event_date,
                    time=time_str,
                    venue=venue,
                    description=description[:200] if description else "",
                    category=category,
                    url=url,
                    is_free=is_free,
                    price=price,
                    source="google_events",
                ))
            except Exception as e:
                logger.warning("Failed to parse SerpAPI event: %s", e)

    return events
