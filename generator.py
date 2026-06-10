from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from models import Event
from weather import WeatherDay
from on_this_day import get_fact_for_date
from capitol_svg import CAPITOL_SVG, TREE_SVG

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_DEFAULT_OUTPUT = Path(__file__).parent / "docs" / "index.html"


@dataclass
class DayView:
    date: date
    weather: WeatherDay | None
    events: list[Event]


def _build_days(
    events: list[Event],
    weather: dict[date, WeatherDay],
) -> list[DayView]:
    today = date.today()
    days: list[DayView] = []
    by_date: dict[date, list[Event]] = {}
    for event in events:
        by_date.setdefault(event.date, []).append(event)

    for i in range(14):
        d = today + timedelta(days=i)
        days.append(DayView(
            date=d,
            weather=weather.get(d),
            events=by_date.get(d, []),
        ))
    return days


def generate(
    events: list[Event],
    weather: dict[date, WeatherDay],
    output_path: Path = _DEFAULT_OUTPUT,
) -> None:
    env = Environment(loader=FileSystemLoader(str(_TEMPLATE_DIR)), autoescape=False)
    template = env.get_template("index.html.j2")
    today = date.today()
    days = _build_days(events, weather)
    today_fact = get_fact_for_date(today)
    html = template.render(days=days, today_fact=today_fact,
                           capitol_svg=CAPITOL_SVG, tree_svg=TREE_SVG)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
