import sqlite3
import os

def migrate():
    # Путь к базе данных
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'genesis_v2.db')

    if not os.path.exists(db_path):
        print(f"Файл базы не найден по пути: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Начинаем финальную миграцию...")

    # 1. Добавляем ключевые слова для поиска вакансий
    try:
        cursor.execute("ALTER TABLE archetype_content ADD COLUMN search_keywords TEXT")
        print("[УСПЕХ] Колонка 'search_keywords' добавлена в archetype_content.")
    except sqlite3.OperationalError:
        print("[ИНФО] Колонка 'search_keywords' уже существует.")

    # 2. Добавляем номер в таблицу профессий
    try:
        cursor.execute("ALTER TABLE profession_content ADD COLUMN number TEXT")
        print("[УСПЕХ] Колонка 'number' добавлена в profession_content.")
    except sqlite3.OperationalError:
        print("[ИНФО] Колонка 'number' уже есть.")

    # 3. ДОБАВЛЯЕМ list_csv (то, из-за чего упал прошлый билд)
    try:
        cursor.execute("ALTER TABLE profession_content ADD COLUMN list_csv TEXT")
        print("[УСПЕХ] Колонка 'list_csv' добавлена в profession_content.")
    except sqlite3.OperationalError:
        print("[ИНФО] Колонка 'list_csv' уже существует.")

    conn.commit()
    conn.close()
    print("Миграция завершена. База полностью готова!")

if __name__ == "__main__":
    migrate()