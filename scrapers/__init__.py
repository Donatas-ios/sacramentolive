from .google_events import scrape as scrape_google
from .visitsacramento import scrape as scrape_visitsacramento
from .eventbrite import scrape as scrape_eventbrite
from .do916 import scrape as scrape_do916
from .sacramento365 import scrape as scrape_sacramento365
from .sacbee import scrape as scrape_sacbee

ALL_SCRAPERS = [
    scrape_google,
    scrape_visitsacramento,
    scrape_eventbrite,
    scrape_do916,
    scrape_sacramento365,
    scrape_sacbee,
]
