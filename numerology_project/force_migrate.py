import sqlite3
import os


def migrate():
    # 1. Пытаемся найти файл базы в разных местах
    possible_paths = [
        'database.db',
        'instance/database.db',
        'numerology.db',
        '../database.db'
    ]

    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break

    if not db_path:
        print("❌ Файл базы данных не найден. Убедись, что ты запускаешь скрипт в папке проекта.")
        return

    print(f"✅ Найдена база данных по пути: {os.path.abspath(db_path)}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Список ВСЕХ колонок из твоей ошибки (Traceback)
    new_columns = [
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

    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE archetype_content ADD COLUMN {col_name} {col_type}")
            print(f"➕ Колонка [{col_name}] успешно добавлена.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"ℹ️ Колонка [{col_name}] уже была добавлена ранее.")
            else:
                print(f"⚠️ Ошибка при добавлении [{col_name}]: {e}")

    conn.commit()
    conn.close()
    print("\n🚀 Миграция завершена. Теперь запускай app.py!")


if __name__ == "__main__":
    migrate()