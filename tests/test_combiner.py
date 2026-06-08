from datetime import date, timedelta
from models import Category, Event
from combiner import combine

TODAY = date.today()

def make_event(title="Test Event", days_ahead=1, source="test",
               is_free=False, price="$10", url="https://example.com",
               description="", time="7pm", venue="Downtown") -> Event:
    return Event(
        title=title, date=TODAY + timedelta(days=days_ahead),
        time=time, venue=venue, description=description,
        category=Category.COMMUNITY, url=url,
        is_free=is_free, price=price, source=source
    )


def test_combine_returns_events_sorted_by_date():
    events = [make_event(days_ahead=3), make_event(days_ahead=1), make_event(days_ahead=2)]
    result = combine([events])
    dates = [e.date for e in result]
    assert dates == sorted(dates)


def test_combine_filters_past_events():
    past = make_event(days_ahead=-1)
    future = make_event(days_ahead=1)
    result = combine([[past, future]])
    assert past not in result
    assert future in result


def test_combine_filters_beyond_14_days():
    far = make_event(days_ahead=15)
    near = make_event(days_ahead=14)
    result = combine([[far, near]])
    assert far not in result
    assert near in result


def test_combine_deduplicates_same_title_same_date():
    e1 = make_event(title="Jazz Festival", days_ahead=1, source="google", url="https://a.com")
    e2 = make_event(title="Jazz Festival", days_ahead=1, source="eventbrite", url="https://b.com", description="Great show")
    result = combine([[e1], [e2]])
    assert len(result) == 1


def test_combine_deduplication_prefers_more_complete_record():
    e1 = make_event(title="Jazz Festival", days_ahead=1, description="", url="https://a.com")
    e2 = make_event(title="Jazz Festival", days_ahead=1, description="Great show", url="https://b.com")
    result = combine([[e1], [e2]])
    assert result[0].description == "Great show"


def test_combine_deduplication_normalizes_title_case():
    e1 = make_event(title="jazz festival", days_ahead=1)
    e2 = make_event(title="Jazz Festival", days_ahead=1)
    result = combine([[e1], [e2]])
    assert len(result) == 1


def test_combine_merges_multiple_sources():
    a = [make_event(title="Event A", days_ahead=1)]
    b = [make_event(title="Event B", days_ahead=2)]
    result = combine([a, b])
    assert len(result) == 2
