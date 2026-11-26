import json
from pathlib import Path

import astro_tools as at


def test_cards():
    cards = json.load(open(Path(__file__).parent / "data" / "tarot_major_arcana.json", encoding="utf-8"))
    assert [c["number"] for c in cards] == list(range(22))
    assert at.get_card("Шут")["slug"] == "shut"
    assert at.get_card("the world")["number"] == 21


def test_compat():
    assert at.get_compatibility("oven", "lev")["aspect_en"] == "trine"
    assert at.get_compatibility("lev", "oven")["aspect_en"] == "trine"
    assert at.get_compatibility("oven", "vesy")["aspect_en"] == "opposition"
    assert at.get_compatibility("oven", "rak")["aspect_en"] == "square"
    assert at.get_compatibility("oven", "oven")["aspect_en"] == "conjunction"
    rows = json.load(open(Path(__file__).parent / "data" / "zodiac_compatibility.json", encoding="utf-8"))
    assert len(rows) == 78


def test_life_path():
    assert at.life_path("14.03.1990") == 9
    assert at.life_path("29.11.1980") == 4
    # мастер-число: 2+9+1+1+2+0+0+0 ... проверяем, что 11 не сворачивается
    for d in ("29.09.1980", "20.07.2000", "29.02.2000"):
        n = at.life_path(d)
        assert n in at.LIFE_PATH
