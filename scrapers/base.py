from __future__ import annotations
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def get_page(url: str) -> BeautifulSoup | None:
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "lxml")
    except Exception as exc:
        logger.warning("Failed to fetch %s: %s", url, exc)
        return None


def parse_price(text: str) -> tuple[bool, str]:
    """Return (is_free, price_string) from a price/admission text."""
    normalized = text.lower().strip()
    if not normalized or normalized in {"free", "free admission", "$0"}:
        return True, ""
    return False, text.strip()
