import sqlite3
import os


def migrate():
    # Находим твою базу в папке проекта
    db_path = os.path.join(os.getcwd(), 'genesis_v2.db')

    if not os.path.exists(db_path):
        print(f"Файл базы не найден: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("Обновляем локальную базу данных...")

    # Добавляем все недостающие колонки по очереди
    columns_to_add = [
        ("archetype_content", "search_keywords"),
        ("profession_content", "number"),
        ("profession_content", "list_csv")
    ]

    for table, column in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT")
            print(f"[OK] Колонка {column} добавлена в {table}.")
        except sqlite3.OperationalError:
            print(f"[!] Колонка {column} уже есть в {table}.")

    conn.commit()
    conn.close()
    print("Миграция завершена! Перезапусти app.py.")


if __name__ == "__main__":
    migrate()