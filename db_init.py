import os
from app import app, db, ArchetypeContent, ProfessionContent


def init_empty_db():
    """
    Функция для полной очистки и первичной настройки базы данных.
    Она создает структуру таблиц и заполняет их начальными 'заглушками'.
    """
    with app.app_context():
        print("⚠️  ВНИМАНИЕ: Начинаю пересоздание базы данных...")

        # 1. ПОЛНАЯ ОЧИСТКА
        # Удаляем все существующие таблицы, чтобы избежать конфликтов структур
        db.drop_all()

        # 2. СОЗДАНИЕ СТРУКТУРЫ
        # Создаем таблицы заново на основе классов (моделей) из app.py
        db.create_all()

        # 3. ЗАПОЛНЕНИЕ АРХЕТИПОВ (Таблица archetype_content)
        # Мы создаем 9 записей (от 1 до 9), чтобы в админке было что редактировать
        for i in range(1, 10):
            num_str = str(i)

            # ВАЖНО: Используем только те имена полей, которые есть в ArchetypeContent в app.py
            new_arch = ArchetypeContent(
                number=num_str,
                title=f"Архетип {num_str}",
                planet="Не определена",
                action_power="Ожидает заполнения...",
                shadow_side="Ожидает заполнения...",
                growth_point="Ожидает заполнения...",
                realization="Ожидает заполнения...",
                karmic_tasks="Ожидает заполнения...",
                development_cycle="Ожидает заполнения...",
                mind_power="Ожидает заполнения...",
                life_result="Ожидает заполнения...",
                partner_type="Ожидает заполнения...",
                financial_tip="Ожидает заполнения...",
                health_tips="Ожидает заполнения..."
            )
            db.session.add(new_arch)

        # 4. ЗАПОЛНЕНИЕ ПРОФЕССИЙ (Таблица profession_content)
        # Создаем 9 записей для ключевых слов вакансий
        for i in range(1, 10):
            new_prof = ProfessionContent(
                number=str(i),
                list_csv="Психолог, Аналитик, Коуч"  # Дефолтные ключи для примера
            )
            db.session.add(new_prof)

        # 5. СОХРАНЕНИЕ
        try:
            db.session.commit()
            print(f"✅ УСПЕХ: База пересоздана. Создано 9 слотов для архетипов и профессий.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ ОШИБКА при сохранении: {e}")


if __name__ == "__main__":
    init_empty_db()