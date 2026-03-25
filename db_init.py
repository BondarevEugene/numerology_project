from app import app, db, ArchetypeContent, ProfessionContent
from content import ARCHETYPES  # Тот самый файл с текстами


def seed_database():
    with app.app_context():
        # Очищаем старые данные, чтобы не было дублей
        db.drop_all()
        db.create_all()
        print("База данных пересоздана.")

        # Загружаем Архетипы
        for number, data in ARCHETYPES.items():
            # Превращаем текст в HTML для красоты (заменяем переносы строк на <p>)
            formatted_text = data['full_text'].strip().replace('\n\n', '</p><p>').replace('\n', '<br>')
            formatted_text = f"<p>{formatted_text}</p>"

            # Делаем заголовки жирными и крупными (Markdown-style -> HTML)
            formatted_text = formatted_text.replace('###', '<h3 style="color:#b08d57; font-family:Cinzel;">')
            # Закрываем теги h3 (упрощенно)
            formatted_text = formatted_text.replace(':', ':</h3>', 1)

            new_arch = ArchetypeContent(
                number=number,
                title=data['title'],
                full_text=formatted_text
            )
            db.session.add(new_arch)

        # Загружаем базовые профессии (заглушки, которые ты потом поправишь в админке)
        for i in range(1, 10):
            new_prof = ProfessionContent(
                number=str(i),
                list_csv="Управление, Бизнес, Аналитика, Креатив"
            )
            db.session.add(new_prof)

        db.session.commit()
        print("Данные успешно загружены в базу!")


if __name__ == "__main__":
    seed_database()