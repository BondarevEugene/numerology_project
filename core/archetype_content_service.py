from core.archetype_service import ArchetypeService

class ArchetypeContentService:

    @staticmethod
    def get_full_profile(number):
        archetype = ArchetypeService.get(str(number))

        return {
            "title": archetype.get("title", ""),
            "planet": archetype.get("planet", ""),
            "element": archetype.get("element", ""),
            "description": archetype.get("description", ""),
            "keywords": archetype.get("keywords", ""),
            "jobs": archetype.get("jobs", []),
            "short_desc": archetype.get("short_desc", ""),
            "action_power": "Способность влиять на окружающую среду через свои сильные стороны.",
            "shadow_side": "Избыточное использование сильных качеств превращается в ограничение.",
            "growth_point": "Развитие осознанности, дисциплины и стратегического мышления.",
            "realization": "Максимальная реализация достигается через развитие ключевых талантов и их практическое применение.",
            "karmic_tasks": "Научиться использовать свои способности во благо себе и окружающим.",
            "financial_tip": "Доход растет через компетентность, ответственность и создание ценности.",
            "health_tips": "Баланс нагрузки и восстановления является обязательным условием устойчивости.",
            "partner_type": "Партнер, разделяющий жизненные ценности и поддерживающий развитие.",
            "mind_power": "Способность обучаться, адаптироваться и находить новые решения.",
            "life_result": "Создание устойчивой и осмысленной жизни через реализацию сильных сторон."
        }