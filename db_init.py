from app import app, db, ArchetypeContent


def init_empty_db():
    with app.app_context():
        # Сносим старое и создаем структуру
        db.drop_all()
        db.create_all()

        # Создаем 9 пустых записей
        for i in range(1, 10):
            num_str = str(i)
            # Инициализируем объект со всеми полями как пустые строки
            empty_arch = ArchetypeContent(
                number=num_str,
                title=f"Архетип {num_str}",
                dharma=f"Здесь будет трактовка Дхармы для числа {num_str}..."
            )
            db.session.add(empty_arch)

        db.session.commit()
        print("✅ База данных готова к заполнению через админку (9 пустых слотов).")


if __name__ == "__main__":
    init_empty_db()