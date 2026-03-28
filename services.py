import requests


class CareerService:
    @staticmethod
    def get_vacancies(archetype, country='ua', custom_keywords=None):
        """Поиск вакансий. Использует переданные ключи или ключи из архетипа."""
        if not archetype:
            return []

        # Приоритет: 1. Ключи из админки (переданные) 2. Ключи из основной таблицы
        query = custom_keywords if custom_keywords else getattr(archetype, 'search_keywords', None)

        if not query or len(str(query).strip()) < 2:
            print(f"DEBUG: [!] Ключевые слова для группы {archetype.number} не найдены.")
            return []

        # 1. Разбиваем по запятой
        # 2. Убираем пробелы по краям каждого слова
        # 3. Убираем пустые элементы (если кто-то поставил лишнюю запятую)
        words = [w.strip() for w in str(query).split(',') if w.strip()]

        # 4. Соединяем через " OR " (важно: OR должен быть большими буквами для HH.ru)
        clean_query = " OR ".join(words)

        # HH.ru ID стран: Украина = 5, Остальные (РФ/Мир) = 1
        area_id = 5 if country == 'ua' else 1

        print(f"DEBUG: [→] HH.ru Поиск (ИТОГ): '{clean_query}' (Area: {area_id})")
        return CareerService._get_hh_vacancies(clean_query, area_id)

    @staticmethod
    @staticmethod
    def _get_hh_vacancies(query, area_id=5):
        """Поиск через HH.ru API - Расширенная версия"""
        url = "https://api.hh.ru/vacancies"

        # Убираем search_field, чтобы искать и в названии, и в описании
        params = {
            "text": query,
            "area": area_id,
            "per_page": 5,
            "order_by": "relevance",
            # "search_field": "name"  <-- УДАЛЯЕМ ИЛИ КОММЕНТИРУЕМ ЭТО
        }

        headers = {
            "User-Agent": "GenesisPsychologyApp/1.0 (support@genesis.com)"
        }

        try:
            # Добавим принудительную проверку кодировки и таймаут
            resp = requests.get(url, params=params, headers=headers, timeout=10)

            print(f"DEBUG: [🌐] Отправлен URL: {resp.url}")  # Проверим, что ссылка правильная

            if resp.status_code == 200:
                data = resp.json()
                raw_items = data.get('items', [])

                # Если по Украине (5) пусто, попробуем на секунду расширить на весь мир (для теста)
                if not raw_items:
                    print(f"DEBUG: [!] По локации {area_id} пусто. Пробую расширенный поиск...")

                print(f"DEBUG: [✓] HH.ru вернул вакансий: {len(raw_items)}")

                jobs = []
                for item in raw_items:
                    salary_data = item.get('salary')
                    salary_text = "З/п по результатам собеседования"
                    if salary_data:
                        s_from = salary_data.get('from');
                        s_to = salary_data.get('to');
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
                        'salary': {'from': salary_text}
                    })
                return jobs
            else:
                print(f"DEBUG: [!] Ошибка API HH.ru: {resp.status_code} - {resp.text}")

        except Exception as e:
            print(f"DEBUG: [❌] Критическая ошибка API: {e}")

        return []