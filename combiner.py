from __future__ import annotations
import re
from datetime import date, timedelta
from models import Event


def _normalize(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower())


def combine(sources: list[list[Event]]) -> list[Event]:
    today = date.today()
    cutoff = today + timedelta(days=14)

    seen: dict[tuple[str, date], Event] = {}
    for source in sources:
        for event in source:
            if event.date < today or event.date > cutoff:
                continue
            key = (_normalize(event.title), event.date)
            if key not in seen:
                seen[key] = event
            else:
                existing = seen[key]
                seen[key] = Event(
                    title=existing.title,
                    date=existing.date,
                    time=existing.time or event.time,
                    venue=existing.venue or event.venue,
                    description=existing.description or event.description,
                    category=existing.category,
                    url=existing.url,
                    is_free=existing.is_free or event.is_free,
                    price=existing.price or event.price,
                    source=existing.source,
                )

    return sorted(seen.values(), key=lambda e: (e.date, e.time or "", e.title))
