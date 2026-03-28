import requests
import re


class CareerService:
    # Список слов, которые не несут смысла для поиска вакансий, но есть в описаниях
    STOP_WORDS = {
        'душа', 'карма', 'архетип', 'число', 'энергия', 'вселенная',
        'вибрация', 'сильный', 'человек', 'способность', 'нумерология'
    }

    @staticmethod
    def _clean_query(text):
        """Очищает текст от 'эзотерики' и оставляет только проф. ключи"""
        if not text: return ""
        # Убираем пунктуацию и приводим к нижнему регистру
        words = re.findall(r'\w+', text.lower())
        # Фильтруем стоп-слова и короткие предлоги
        filtered = [w for w in words if w not in CareerService.STOP_WORDS and len(w) > 2]
        # Берем первые 3-4 значимых слова для точного поиска
        return " ".join(filtered[:4])

    @staticmethod
    def get_vacancies(archetype):
        """Интеллектуальный подбор вакансий"""
        if not archetype: return []

        # 1. Сначала проверяем, есть ли в админке спец. поле для поиска (самый точный путь)
        search_query = getattr(archetype, 'search_keywords', None)

        # 2. Если нет — берем Число Ума (mind_power), чистим его от воды и ищем по нему
        if not search_query and hasattr(archetype, 'mind_power'):
            search_query = CareerService._clean_query(archetype.mind_power)

        # 3. Крайний случай — название архетипа
        if not search_query:
            search_query = archetype.title

        try:
            # area=1 (Москва), area=2 (Питер), area=16 (Казань). Можно убрать для поиска по всей РФ.
            url = "https://api.hh.ru/vacancies"
            params = {
                'text': search_query,
                'per_page': 5,
                'order_by': 'relevance',
                'schedule': 'remote'  # Добавим фильтр 'удаленка', это модно
            }
            headers = {'User-Agent': 'GenesisPsychologyApp/1.0'}

            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json().get('items', [])
        except Exception as e:
            print(f"HH API Error: {e}")

        return []