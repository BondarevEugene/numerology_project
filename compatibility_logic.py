# compatibility_logic.py
from mind_logic import sum_digits


def calculate_pair_compatibility(date1, date2):
    """
    date1, date2: объекты datetime.date
    """
    # Пример: Аркан пары = (Аркан 1 + Аркан 2)
    a1 = sum_digits(date1.day)
    a2 = sum_digits(date2.day)

    pair_arcane = a1 + a2
    if pair_arcane > 22: pair_arcane -= 22

    # Здесь можно добавить расшифровку из БД или словаря SYNASTRY_TEXTS
    return {
        "score": 85,  # Заглушка для красоты
        "arcane": pair_arcane,
        "description": "Ваш союз направлен на духовное развитие..."
    }