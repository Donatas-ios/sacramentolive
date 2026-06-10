#!/usr/bin/env python3
"""
Run all scrapers, combine results, fetch weather, and generate docs/index.html.
"""
import logging
import sys
from combiner import combine
from generator import generate
from trivia_generator import generate_trivia
from museums_generator import generate_museums
from restaurants_generator import generate_restaurants
from feedback_generator import generate_feedback
from weather import fetch_forecast
from scrapers import ALL_SCRAPERS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting SacramentoLive scrape run")

    all_events = []
    for scrape_fn in ALL_SCRAPERS:
        name = scrape_fn.__module__
        try:
            events = scrape_fn()
            logger.info("%s: %d events", name, len(events))
            all_events.append(events)
        except Exception as exc:
            logger.error("%s failed: %s", name, exc)
            all_events.append([])

    combined = combine(all_events)
    logger.info("Combined: %d unique events", len(combined))

    try:
        weather = fetch_forecast()
        logger.info("Weather: %d days fetched", len(weather))
    except Exception as exc:
        logger.error("Weather fetch failed: %s", exc)
        weather = {}

    generate(combined, weather)
    logger.info("Generated docs/index.html")

    generate_trivia()
    logger.info("Generated docs/trivia.html")

    generate_museums()
    logger.info("Generated docs/museums.html")

    generate_restaurants()
    logger.info("Generated docs/restaurants.html")

    generate_feedback()
    logger.info("Generated docs/feedback.html")


if __name__ == "__main__":
    main()
