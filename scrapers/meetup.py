from __future__ import annotations
import logging
import re
from datetime import date, datetime, timedelta

from bs4 import BeautifulSoup
from models import Event, infer_category

logger = logging.getLogger(__name__)

_URL = "https://www.meetup.com/find/?location=Sacramento%2C+CA&source=EVENTS&distance=25mi"
_TODAY = None  # patched in tests

_MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|" \
          "January|February|March|April|May|June|July|August|September|October|November|December"


def _today() -> date:
    return _TODAY or date.today()


def _parse_date_time(text: str) -> tuple[date | None, str]:
    today = _today()
    # Patterns: "Sat, Jun 20 · 2:00 PM PDT" or "Mon, Jun 15 · 10:00 AM PDT"
    match = re.search(
        rf'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s*({_MONTHS})\s+(\d+)\s*[·•]\s*(\d+:\d+\s*[AP]M)',
        text, re.IGNORECASE
    )
    if match:
        month_str, day_str, time_str = match.group(1), match.group(2), match.group(3)
        for fmt in ("%b %d", "%B %d"):
            try:
                dt = datetime.strptime(f"{month_str} {day_str}", fmt)
                d = dt.replace(year=today.year).date()
                if d < today:
                    d = d.replace(year=today.year + 1)
                return d, time_str.strip()
            except ValueError:
                continue

    # Fallback: "Monthly · Mon, Jun 15 · ..."
    match2 = re.search(
        rf'({_MONTHS})\s+(\d+)',
        text, re.IGNORECASE
    )
    if match2:
        for fmt in ("%b %d", "%B %d"):
            try:
                dt = datetime.strptime(f"{match2.group(1)} {match2.group(2)}", fmt)
                d = dt.replace(year=today.year).date()
                if d < today:
                    d = d.replace(year=today.year + 1)
                return d, ""
            except ValueError:
                continue

    return None, ""


def scrape() -> list[Event]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.warning("playwright not installed, skipping Meetup")
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
            page.wait_for_timeout(4000)
            for _ in range(5):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1500)
            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "lxml")
        seen_urls: set[str] = set()

        for link in soup.select("a[href*='/events/']"):
            try:
                raw_text = link.get_text(separator=" ", strip=True)
                if not raw_text or len(raw_text) < 10:
                    continue

                url = link.get("href", "")
                # strip tracking params
                url = url.split("?")[0]
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                # skip online-only events
                if "Online" in raw_text and "·" not in raw_text:
                    continue

                event_date, time_str = _parse_date_time(raw_text)
                if not event_date or event_date < today or event_date > cutoff:
                    continue

                # title is everything before the date pattern
                title = re.split(
                    r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),|Monthly\s*·',
                    raw_text, maxsplit=1
                )[0].strip()
                # strip leading junk like "4 seats left"
                title = re.sub(r'^\d+\s+seats?\s+left\s*', '', title, flags=re.IGNORECASE).strip()
                if not title:
                    continue

                # group name after "by "
                venue = ""
                by_match = re.search(r'\bby\s+(.+?)(?:\s*icon|\s*\d|\s*$)', raw_text, re.IGNORECASE)
                if by_match:
                    venue = by_match.group(1).strip()

                # online check
                is_online = bool(re.search(r'\bOnline\b', raw_text, re.IGNORECASE))
                if is_online:
                    venue = "Online"

                category = infer_category(title, "")

                events.append(Event(
                    title=title,
                    date=event_date,
                    time=time_str,
                    venue=venue,
                    description="",
                    category=category,
                    url=url,
                    is_free=False,
                    price="",
                    source="meetup",
                ))
            except Exception as e:
                logger.warning("Failed to parse Meetup event: %s", e)

    except Exception as e:
        logger.warning("Meetup Playwright scrape failed: %s", e)

    return events
