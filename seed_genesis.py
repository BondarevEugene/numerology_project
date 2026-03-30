import os
from app import app, db, ArchetypeContent, ProfessionContent
from content import ARCHETYPES
from data import ARCHETYPE_EXTRAS

def seed_database():
    with app.app_context():
        print("🌀 Перезагрузка Матрицы Genesis...")
        db.drop_all()
        db.create_all()

        for i in range(1, 10):
            num = str(i)
            # Берем данные из файлов контента
            core_data = ARCHETYPES.get(num, {})
            extra_data = ARCHETYPE_EXTRAS.get(num, {})

            # Создаем Архетип со всеми новыми полями
            arc = ArchetypeContent(
                number=num,
                title=core_data.get('title', f"Аркан {num}").replace('᚛ ', '').replace(' ᚜', ''),
                planet=extra_data.get('planet', 'Неизвестно'),
                action_power=core_data.get('full_text', 'Данные в разработке...'),
                shadow_side="Теневая сторона требует проработки.",
                growth_point="Точка роста в дисциплине.",
                realization="Реализация через социальные проекты.",
                karmic_tasks="Отработка личной ответственности.",
                development_cycle="1 — 4 — 7",
                mind_power="Высокий аналитический потенциал.",
                life_result="Оставление значимого наследия.",
                partner_type="Дополняющий лидер.",
                financial_tip="Инвестиции в знания.",
                health_tips="Обратите внимание на режим сна."
            )
            db.session.add(arc)

            # Создаем дефолтные маппинги для профессий
            prof = ProfessionContent(
                number=num,
                list_csv="Менеджер, Руководитель, Аналитик"
            )
            db.session.add(prof)

        db.session.commit()
        print("✅ База данных синхронизирована с кодом!")

if __name__ == "__main__":
    seed_database()