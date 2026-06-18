import requests

# Константы для Психоматрицы
NODES_INFO = {
    '1': {'name': 'Характер', 'low': '...', 'mid': '...', 'high': '...'},
    # Добавь сюда свои полные тексты из старого файла
}

SYNASTRY_TEXTS = {
    1: "Союз лидеров...",
    # Добавь сюда свои полные тексты
}


def sum_digits(n):
    """Сумма цифр до однозначного (Архетип)"""
    if not n: return 0
    s = sum(int(d) for d in str(n) if d.isdigit())
    while s > 9:
        s = sum(int(d) for d in str(s))
    return s


def calculate_full_matrix_logic(d, m, y):
    """Полная логика квадрата Пифагора"""
    # 1. Строка цифр
    s_base = f"{str(d).zfill(2)}{str(m).zfill(2)}{y}"
    # 2. Доп. числа
    n1 = sum(int(x) for x in s_base if x.isdigit())
    n2 = sum(int(x) for x in str(n1))
    first_digit = int(str(d)[0]) if str(d)[0] != '0' else int(str(d)[1])
    n3 = abs(n1 - (2 * first_digit))
    n4 = sum(int(x) for x in str(n3))

    all_str = s_base + str(n1) + str(n2) + str(n3) + str(n4)
    all_digits = [int(x) for x in all_str if x.isdigit()]

    matrix_dict = {}
    for i in range(1, 10):
        cnt = all_digits.count(i)
        matrix_dict[str(i)] = str(i) * cnt if cnt > 0 else "-"

    # Заглушка для скиллов (можно заменить на твою формулу)
    user_skills = {
        "labels": ["Лидерство", "Коммуникация", "Эмпатия", "Логика", "Agile"],
        "data": [
            min(100, all_digits.count(1) * 25),
            min(100, all_digits.count(3) * 30),
            min(100, all_digits.count(2) * 20),
            min(100, all_digits.count(5) * 35),
            min(100, all_digits.count(9) * 20)
        ]
    }

    return matrix_dict, user_skills, all_digits, {}


class CareerService:
    @staticmethod
    def get_vacancies(query, country='ru'):
        """Поиск на HH.ru"""
        try:
            url = f"https://api.hh.ru/vacancies?text={query}&per_page=4"
            headers = {'User-Agent': 'GenesisPsychology/4.0'}
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                return r.json().get('items', [])
            return []
        except Exception as e:
            print(f"HH API Error: {e}")
            return []