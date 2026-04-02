import sqlite3
import os


def migrate():
    # Проверь имя файла базы! Если оно другое (например, 'instance/database.db'), исправь путь.
    db_path = 'database.db'

    if not os.path.exists(db_path):
        print(f"Файл {db_path} не найден! Убедись, что скрипт лежит в той же папке.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Полный список колонок из твоего Traceback, которых может не хватать
    columns_to_add = [
        ('element', 'TEXT'),
        ('tarot_arcane', 'TEXT'),
        ('development_cycle', 'TEXT'),
        ('mind_power', 'TEXT'),
        ('partner_type', 'TEXT'),
        ('financial_tip', 'TEXT'),
        ('health_tips', 'TEXT'),
        ('exit_minus', 'TEXT'),
        ('search_queries', 'TEXT')
    ]

    print(f"--- Запуск исправления базы данных {db_path} ---")

    for col_name, col_type in columns_to_add:
        try:
            # Пытаемся добавить колонку
            cursor.execute(f"ALTER TABLE archetype_content ADD COLUMN {col_name} {col_type}")
            print(f"[+] Добавлена колонка: {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"[-] Пропуск: {col_name} (уже есть)")
            else:
                print(f"[!] Ошибка на {col_name}: {e}")

    conn.commit()
    conn.close()
    print("--- Исправление завершено! Попробуй запустить app.py ---")


if __name__ == "__main__":
    migrate()