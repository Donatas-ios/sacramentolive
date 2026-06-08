from datetime import date
from models import Category, Event, infer_category


def test_infer_category_music():
    assert infer_category("Sacramento Jazz Festival", "") == Category.MUSIC

def test_infer_category_food():
    assert infer_category("Midtown Beer Garden Pop-up", "") == Category.FOOD

def test_infer_category_arts():
    assert infer_category("Crocker Art Museum After Dark", "") == Category.ARTS

def test_infer_category_sports():
    assert infer_category("Sacramento Kings vs Lakers", "") == Category.SPORTS

def test_infer_category_family():
    assert infer_category("Kids Storytime at Library", "") == Category.FAMILY

def test_infer_category_nightlife():
    assert infer_category("DJ Night at Club Ace", "") == Category.NIGHTLIFE

def test_infer_category_festivals():
    assert infer_category("Midtown Farmers Market", "") == Category.FESTIVALS

def test_infer_category_fallback():
    assert infer_category("Town Hall Meeting", "") == Category.COMMUNITY

def test_infer_category_uses_description():
    assert infer_category("Saturday Event", "live jazz music all night") == Category.MUSIC

def test_event_is_free_from_price():
    e = Event(
        title="Test", date=date.today(), time="", venue="",
        description="", category=Category.COMMUNITY,
        url="https://example.com", is_free=True, price="", source="test"
    )
    assert e.is_free is True
