import requests


class CareerService:
    @staticmethod
    def get_vacancies(archetype_num, country='ua', custom_keywords=None):
        """
        archetype_num: строка или число (1-9)
        custom_keywords: строка с ключевыми словами через запятую
        """
        # Если ключи не переданы из БД, ставим базовые, чтобы поиск не упал
        query = custom_keywords if custom_keywords else "Консультант, Менеджер"

        words = [w.strip() for w in str(query).split(',') if w.strip()]
        clean_query = " OR ".join(words)

        # Логика регионов HH.ru
        area_id = 5 if country == 'ua' else 1

        print(f"DEBUG: [→] HH.ru Поиск для группы {archetype_num}: '{clean_query}'")
        return CareerService._get_hh_vacancies(clean_query, area_id)

    @staticmethod
    def _get_hh_vacancies(query, area_id=5):
        url = "https://api.hh.ru/vacancies"
        params = {
            "text": query,
            "area": area_id,
            "per_page": 6,
            "order_by": "relevance"
        }
        headers = {"User-Agent": "GenesisApp/1.0"}

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            if resp.status_code == 200:
                raw_items = resp.json().get('items', [])
                jobs = []
                for item in raw_items:
                    salary_data = item.get('salary')
                    salary_text = "По результатам собеседования"
                    if salary_data:
                        f, t = salary_data.get('from'), salary_data.get('to')
                        cur = salary_data.get('currency', '')
                        salary_text = f"от {f} {cur}" if f and not t else f"{f}-{t} {cur}" if f and t else f"до {t} {cur}"

                    jobs.append({
                        'name': item.get('name'),
                        'employer': {'name': item.get('employer', {}).get('name', 'Компания')},
                        'alternate_url': item.get('alternate_url'),
                        'salary': {'from': salary_text}
                    })
                return jobs
        except Exception as e:
            print(f"DEBUG: [❌] HH.ru Error: {e}")
        return []