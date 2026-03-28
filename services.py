import requests


class CareerService:
    @staticmethod
    def get_vacancies(archetype, country='ua'):
        """Универсальный и стабильный поиск вакансий"""
        if not archetype:
            return []

        # Берем ключевые слова из админки
        query = getattr(archetype, 'search_keywords', None)

        if not query or len(str(query).strip()) < 2:
            print(f"DEBUG: [!] Ключевые слова для группы {archetype.number} не заданы.")
            return []

        # Формируем чистый поисковый запрос без лишних пробелов
        # Превращаем "Директор, Менеджер" -> "директор OR менеджер"
        words = [w.strip().lower() for w in query.split(',') if w.strip()]
        clean_query = " OR ".join(words)

        # HH.ru ID стран: Украина = 5, Россия = 1, Казахстан = 40
        area_id = 5 if country == 'ua' else 1

        print(f"DEBUG: [→] Страна: {country} (ID: {area_id}), Поиск: '{clean_query}'")

        return CareerService._get_hh_vacancies(clean_query, area_id)

    @staticmethod
    def _get_hh_vacancies(query, area_id=5):
        """Поиск через HH.ru API"""
        url = "https://api.hh.ru/vacancies"
        params = {
            "text": query,  # Поисковая строка с OR
            "area": area_id,  # Локация
            "per_page": 5,  # Лимит 5 вакансий
            "order_by": "relevance",
            "search_field": "name"  # Ищем ТОЛЬКО в названии вакансии для точности
        }
        headers = {
            "User-Agent": "GenesisPsychologyApp/1.0 (support@genesis.com)"
        }

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=5)

            if resp.status_code == 200:
                data = resp.json()
                raw_items = data.get('items', [])

                if not raw_items:
                    print(f"DEBUG: [!] HH.ru вернул 0 вакансий для запроса: '{query}' в локации {area_id}")
                    return []

                print(f"DEBUG: [✓] HH.ru нашел вакансий: {len(raw_items)}")

                jobs = []
                for item in raw_items:
                    # Обработка зарплаты
                    salary_data = item.get('salary')
                    salary_text = "З/п по результатам собеседования"

                    if salary_data:
                        s_from = salary_data.get('from')
                        s_to = salary_data.get('to')
                        cur = salary_data.get('currency', '')

                        if s_from and s_to:
                            salary_text = f"{s_from}-{s_to} {cur}"
                        elif s_from:
                            salary_text = f"от {s_from} {cur}"
                        elif s_to:
                            salary_text = f"до {s_to} {cur}"

                    jobs.append({
                        'name': item.get('name'),
                        'employer': {'name': item.get('employer', {}).get('name', 'Компания')},
                        'alternate_url': item.get('alternate_url'),
                        'salary': {'from': salary_text, 'currency': ''}
                    })
                return jobs
            else:
                print(f"DEBUG: [!] Ошибка API HH.ru: {resp.status_code} - {resp.text}")

        except Exception as e:
            print(f"DEBUG: [❌] Критическая ошибка при запросе к HH.ru: {e}")

        return []