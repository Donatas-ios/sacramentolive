from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import date
from enum import Enum


class Category(Enum):
    MUSIC = "Music"
    FOOD = "Food & Drink"
    ARTS = "Arts & Theater"
    SPORTS = "Sports"
    FAMILY = "Family"
    COMMUNITY = "Community"
    NIGHTLIFE = "Nightlife"
    FESTIVALS = "Festivals & Fairs"


# Order matters: first matching category wins. MUSIC before ARTS is intentional
# (concerts/bands are common; opera/ballet/theater checked second).
_KEYWORDS: dict[Category, list[str]] = {
    Category.MUSIC: ["music", "jazz", "band", "orchestra", "symphony",
                     "live music", "rock", "hip hop", "country", "singer", "dj set"],
    Category.FOOD: ["food", "drink", "beer", "wine", "restaurant", "dining",
                    "tasting", "brunch", "chef", "culinary", "farm to fork",
                    "cocktail", "brewery", "winery", "pop-up dinner"],
    Category.ARTS: ["art", "theater", "theatre", "gallery", "museum", "exhibition",
                    "dance", "opera", "comedy", "improv", "film", "cinema", "movie",
                    "painting", "sculpture", "ballet"],
    Category.SPORTS: ["sport", "game", "race", "run", "marathon", "basketball",
                      "baseball", "soccer", "football", "kings", "republic",
                      "athletics", "tournament", "triathlon", "cycling"],
    Category.FAMILY: ["family", "kids", "children", "youth", "school", "puppet",
                      "storytime", "playground", "toddler"],
    Category.NIGHTLIFE: ["nightlife", "nightclub", "lounge", "bar crawl", "club night",
                         "late night", "dj night", "after party"],
    Category.FESTIVALS: ["festival", "fair", "carnival", "parade", "expo",
                         "farmers market", "street fair", "block party"],
}


def _matches_any(text: str, keywords: list[str]) -> bool:
    return any(re.search(r'\b' + re.escape(kw) + r'\b', text) for kw in keywords)


def infer_category(title: str, description: str) -> Category:
    text = (title + " " + description).lower()
    for category, keywords in _KEYWORDS.items():
        if _matches_any(text, keywords):
            return category
    return Category.COMMUNITY


@dataclass
class Event:
    title: str
    date: date
    time: str
    venue: str
    description: str
    category: Category
    url: str
    is_free: bool
    price: str
    source: str
