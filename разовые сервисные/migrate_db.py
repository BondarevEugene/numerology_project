import sqlite3


def migrate():
    # Укажи здесь имя своего файла базы данных
    db_path = 'database.db'

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Список всех колонок, которые SQLAlchemy ожидает увидеть (согласно твоей ошибке)
    # Формат: (имя_колонки, тип)
    required_columns = [
        ('element', 'TEXT'),
        ('development_cycle', 'TEXT'),
        ('exit_minus', 'TEXT'),
        ('tarot_arcane', 'TEXT'),
        ('mind_power', 'TEXT'),
        ('partner_type', 'TEXT'),
        ('financial_tip', 'TEXT'),
        ('health_tips', 'TEXT')
    ]

    print(f"--- Начало миграции базы данных {db_path} ---")

    for col_name, col_type in required_columns:
        try:
            # Пробуем добавить колонку
            cursor.execute(f"ALTER TABLE archetype_content ADD COLUMN {col_name} {col_type}")
            print(f"[+] Колонка '{col_name}' успешно добавлена.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"[-] Колонка '{col_name}' уже существует, пропуск.")
            else:
                print(f"[!] Ошибка при добавлении '{col_name}': {e}")

    conn.commit()
    conn.close()
    print("--- Миграция завершена! Теперь можешь запускать app.py ---")


if __name__ == "__main__":
    migrate()