import sqlite3
import os


def migrate():
    # Путь к твоей базе данных
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'genesis_v2.db')

    if not os.path.exists(db_path):
        print(f"Файл базы не найден по пути: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Начинаем миграцию...")

    try:
        # Пробуем добавить колонку search_keywords
        cursor.execute("ALTER TABLE archetype_content ADD COLUMN search_keywords TEXT")
        print("[УСПЕХ] Колонка 'search_keywords' добавлена.")
    except sqlite3.OperationalError:
        print("[ИНФО] Колонка 'search_keywords' уже существует.")

    try:
        # На всякий случай добавим и number в таблицу профессий, если её не было
        cursor.execute("ALTER TABLE profession_content ADD COLUMN number TEXT")
        print("[УСПЕХ] Колонка 'number' добавлена в таблицу профессий.")
    except sqlite3.OperationalError:
        print("[ИНФО] Колонка 'number' в профессиях уже есть.")

    conn.commit()
    conn.close()
    print("Миграция завершена успешно. Теперь данные в безопасности!")


if __name__ == "__main__":
    migrate()