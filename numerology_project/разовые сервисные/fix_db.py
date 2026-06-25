from app import app
from models import db, ArchetypeContent


def populate_archetypes():
    with app.app_context():
        # 1. Проверяем, есть ли уже данные
        if ArchetypeContent.query.count() > 0:
            print("💡 В базе уже есть данные.")
            return

        print("🚀 Инициализация текстов архетипов...")

        # 2. Определяем доступные колонки в модели
        columns = ArchetypeContent.__table__.columns.keys()
        print(f"🔍 Найденные колонки в базе: {columns}")

        for i in range(1, 23):
            # Создаем пустой объект
            new_arcane = ArchetypeContent()

            # 3. Заполняем только те поля, которые реально существуют
            if 'number' in columns:
                new_arcane.number = str(i)

            if 'title' in columns:
                new_arcane.title = f"Архетип №{i}"

            # Проверяем, как называется поле для текста (одно из этих)
            text_fields = ['content', 'description', 'content_text', 'text']
            for field in text_fields:
                if field in columns:
                    setattr(new_arcane, field,
                            f"Это подробное описание для Аркана №{i}. Вы можете изменить его в админке.")
                    break

            # Поля для советов (shadow/advice)
            if 'shadow' in columns:
                new_arcane.shadow = "Теневые проявления в разработке..."
            if 'advice' in columns:
                new_arcane.advice = "Рекомендации по развитию в разработке..."

            db.session.add(new_arcane)

        try:
            db.session.commit()
            print("✅ 22 заготовки созданы успешно!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Ошибка при сохранении: {e}")


if __name__ == "__main__":
    populate_archetypes()