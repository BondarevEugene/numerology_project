from app import app, db

def create_everything():
    with app.app_context():
        # Это удалит все старые таблицы (если они были) и создаст новые
        # согласно всем полям, прописанным в твоем текущем app.py
        db.drop_all()
        db.create_all()
        print("✅ База данных успешно пересоздана со всеми новыми колонками!")

if __name__ == "__main__":
    create_everything()