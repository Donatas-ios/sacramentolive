from .google_events import scrape as scrape_google

def _try_import(module_name, func_name):
    try:
        import importlib
        mod = importlib.import_module(f".{module_name}", package="scrapers")
        return getattr(mod, func_name)
    except (ImportError, AttributeError):
        return None

scrape_visitsacramento = _try_import("visitsacramento", "scrape")
scrape_eventbrite = _try_import("eventbrite", "scrape")
scrape_do916 = _try_import("do916", "scrape")
scrape_sacramento365 = _try_import("sacramento365", "scrape")
scrape_sacbee = _try_import("sacbee", "scrape")

ALL_SCRAPERS = [s for s in [
    scrape_google,
    scrape_visitsacramento,
    scrape_eventbrite,
    scrape_do916,
    scrape_sacramento365,
    scrape_sacbee,
] if s is not None]
