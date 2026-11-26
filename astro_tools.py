#!/usr/bin/env python3
"""Таро, знаки зодиака и число жизненного пути: небольшой набор инструментов без зависимостей.

Примеры:
    python astro_tools.py tarot shut
    python astro_tools.py compat oven lev
    python astro_tools.py lifepath 14.03.1990
"""
import json
import sys
from datetime import datetime
from pathlib import Path

DATA = Path(__file__).parent / "data"

LIFE_PATH = {
    1: "лидерство, самостоятельность, инициатива",
    2: "партнёрство, дипломатичность, чуткость",
    3: "творчество, общительность, самовыражение",
    4: "порядок, надёжность, системная работа",
    5: "перемены, свобода, любопытство",
    6: "забота, ответственность, семья",
    7: "анализ, поиск смысла, уединение",
    8: "достижения, деньги, организаторские способности",
    9: "завершение, сочувствие, широкий взгляд",
    11: "мастер-число: интуиция и вдохновение",
    22: "мастер-число: масштабные практические цели",
    33: "мастер-число: служение и наставничество",
}


def _load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def get_card(query):
    """Найти карту старшего аркана по слагу, русскому или английскому названию, или номеру."""
    q = str(query).strip().lower()
    for card in _load("tarot_major_arcana.json"):
        if q in (card["slug"], card["name_ru"].lower(), card["name_en"].lower(), str(card["number"])):
            return card
    return None


def get_compatibility(a, b):
    """Аспект и отношение стихий для пары знаков (слаги вроде oven, lev; порядок не важен)."""
    a, b = a.strip().lower(), b.strip().lower()
    for row in _load("zodiac_compatibility.json"):
        if {row["sign_a"], row["sign_b"]} == {a, b}:
            return row
    return None


def life_path(date_str):
    """Число жизненного пути по дате ДД.ММ.ГГГГ (пифагорейская редукция, мастер-числа 11, 22, 33)."""
    d = datetime.strptime(date_str, "%d.%m.%Y")
    total = sum(int(ch) for ch in d.strftime("%d%m%Y"))
    while total > 9 and total not in (11, 22, 33):
        total = sum(int(ch) for ch in str(total))
    return total


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    cmd, args = argv[1], argv[2:]
    if cmd == "tarot":
        card = get_card(" ".join(args))
        if not card:
            print("Карта не найдена")
            return 2
        print(f"{card['number']} — {card['name_ru']} ({card['name_en']}), {card['element_ru']}, {card['correspondence']}")
        print("Прямое положение:", ", ".join(card["keywords_upright"]))
        print("Перевёрнутое:", ", ".join(card["keywords_reversed"]))
        print("Подробнее:", card["url"])
    elif cmd == "compat" and len(args) == 2:
        row = get_compatibility(*args)
        if not row:
            print("Пара не найдена")
            return 2
        print(f"{row['sign_a']} + {row['sign_b']}: {row['aspect_ru']}, {row['elements_relation']}")
        print(row["summary"])
        if row["page_url"]:
            print("Подробнее:", row["page_url"])
    elif cmd == "lifepath":
        n = life_path(args[0])
        print(f"Число жизненного пути: {n} — {LIFE_PATH[n]}")
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
