from __future__ import annotations
import logging
import os
from datetime import date, datetime, timedelta

import requests

from models import Event, infer_category

logger = logging.getLogger(__name__)

_API_URL = "https://app.ticketmaster.com/discovery/v2/events.json"
_TODAY = None  # patched in tests


def _today() -> date:
    return _TODAY or date.today()


def _parse_events(data: dict) -> list[Event]:
    today = _today()
    cutoff = today + timedelta(days=14)
    events: list[Event] = []

    items = data.get("_embedded", {}).get("events", [])
    for item in items:
        try:
            dates = item.get("dates", {})
            start = dates.get("start", {})
            date_str = start.get("localDate")
            if not date_str:
                continue
            event_date = date.fromisoformat(date_str)
            if event_date < today or event_date > cutoff:
                continue

            time_str = ""
            local_time = start.get("localTime")
            if local_time:
                try:
                    t = datetime.strptime(local_time, "%H:%M:%S")
                    time_str = t.strftime("%-I:%M %p")
                except ValueError:
                    pass

            venue = ""
            venues = item.get("_embedded", {}).get("venues", [])
            if venues:
                venue = venues[0].get("name", "")

            url = item.get("url", "")

            price_ranges = item.get("priceRanges", [])
            is_free = False
            price = ""
            if price_ranges:
                mn = price_ranges[0].get("min", 0)
                mx = price_ranges[0].get("max", 0)
                if mn == 0 and mx == 0:
                    is_free = True
                elif mn == mx:
                    price = f"${mn:.0f}"
                else:
                    price = f"${mn:.0f}–${mx:.0f}"

            classifications = item.get("classifications", [{}])
            segment = classifications[0].get("segment", {}).get("name", "")
            genre = classifications[0].get("genre", {}).get("name", "")
            description = f"{segment} {genre}".strip()

            title = item.get("name", "")
            category = infer_category(title, description)

            events.append(Event(
                title=title,
                date=event_date,
                time=time_str,
                venue=venue,
                description=description,
                category=category,
                url=url,
                is_free=is_free,
                price=price,
                source="ticketmaster",
            ))
        except Exception as e:
            logger.warning("Failed to parse Ticketmaster event: %s", e)

    return events


def scrape() -> list[Event]:
    api_key = os.environ.get("TICKETMASTER_API_KEY", "")
    if not api_key:
        logger.warning("TICKETMASTER_API_KEY not set, skipping")
        return []

    today = _today()
    cutoff = today + timedelta(days=14)
    params = {
        "apikey": api_key,
        "city": "Sacramento",
        "stateCode": "CA",
        "countryCode": "US",
        "size": 100,
        "startDateTime": today.strftime("%Y-%m-%dT00:00:00Z"),
        "endDateTime": cutoff.strftime("%Y-%m-%dT23:59:59Z"),
        "sort": "date,asc",
    }

    try:
        resp = requests.get(_API_URL, params=params, timeout=15)
        resp.raise_for_status()
        return _parse_events(resp.json())
    except Exception as e:
        logger.warning("Ticketmaster scrape failed: %s", e)
        return []
