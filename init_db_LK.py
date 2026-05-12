# init_db_LK.py
from app import app
from models import db  # Обязательно импортируем db здесь

with app.app_context():
    try:
        # SQLAlchemy проверит базу, указанную в app.config['SQLALCHEMY_DATABASE_URI']
        # и создаст только те таблицы, которых еще нет (например, 'users')
        db.create_all()
        print("✅ Проверка структуры базы данных завершена.")
        print("✅ Таблицы (включая 'users') успешно созданы или уже существуют!")
    except Exception as e:
        print(f"❌ Ошибка при инициализации базы данных: {e}")