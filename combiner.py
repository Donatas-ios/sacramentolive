from __future__ import annotations
import re
from datetime import date, timedelta
from models import Event


def _normalize(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower())


def _completeness(e: Event) -> int:
    return sum([
        bool(e.description), bool(e.time), bool(e.venue),
        bool(e.price), bool(e.url),
    ])


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
                if _completeness(event) > _completeness(existing):
                    # keep original url but take richer record
                    merged = Event(
                        title=existing.title,
                        date=existing.date,
                        time=event.time or existing.time,
                        venue=event.venue or existing.venue,
                        description=event.description or existing.description,
                        category=existing.category,
                        url=existing.url,
                        is_free=existing.is_free or event.is_free,
                        price=event.price or existing.price,
                        source=existing.source,
                    )
                    seen[key] = merged

    return sorted(seen.values(), key=lambda e: (e.date, e.time, e.title))
