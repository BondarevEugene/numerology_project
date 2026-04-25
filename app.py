import os
from flask import Flask
from sqlalchemy import create_engine
from models import db
from flask_login import LoginManager  # импорт логинменеджера

# 1. Инициализация приложения
app = Flask(__name__)
app.secret_key = 'genesis_secret_key_0602'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Куда перенаправлять, если доступ закрыт


@login_manager.user_loader
def load_user(user_id):
    from models import User  # Импорт внутри, чтобы избежать циклической ссылки
    return db.session.get(User, int(user_id))


# 2. Настройка Failover базы данных
NEON_URL = ("postgresql://neondb_owner:npg_7uV2YfNbIeWd@ep-black-water-a2o4465m-pooler.eu-central-1.aws.neon.tech"
            "/neondb?sslmode=require")
LOCAL_DB_URL = "sqlite:///genesis_v2.db"


# 3. СНАЧАЛА ОПРЕДЕЛЯЕМ ФУНКЦИЮ
def get_db_uri():
    uri = os.getenv('DATABASE_URL', NEON_URL)
    try:
        engine = create_engine(uri, connect_args={'connect_timeout': 2})
        with engine.connect() as conn:
            return uri
    except:
        return LOCAL_DB_URL


# 3. ВЫЗЫВАЕМ ФУНКЦИЮ
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 4. Привязка базы
db.init_app(app)
with app.app_context():
    db.create_all()  # Это создаст таблицы в Neon, если их еще нет

# 5. РЕГИСТРАЦИЯ МОДУЛЕЙ (Импортируем ТОЛЬКО после инициализации db)
with app.app_context():
    try:
        # Импортируем внутри контекста, чтобы избежать циклических ссылок
        from routes.auth import auth_bp
        from routes.profile import profile_bp
        from routes.main import main_bp
        from routes.admin import admin_bp

        # Проверяем, не зарегистрированы ли они уже (на всякий случай)
        if 'auth' not in app.blueprints:
            app.register_blueprint(auth_bp)
        if 'profile' not in app.blueprints:
            app.register_blueprint(profile_bp)
        if 'main' not in app.blueprints:
            app.register_blueprint(main_bp)
        if 'admin' not in app.blueprints:
            app.register_blueprint(admin_bp)

        print("✅ Все модули успешно зарегистрированы (без дублей)")
    except Exception as e:
        print(f"❌ Ошибка регистрации: {e}")

# --- ВОТ ВСТАВКА КУСКА КОДА про авторизацию ---
with app.app_context():
    try:
        db.create_all()
        print("✅ База данных синхронизирована (таблицы созданы/обновлены)")
    except Exception as e:
        print(f"❌ Критическая ошибка при создании таблиц: {e}")
# ------------------------------------


# 4. РЕГИСТРАЦИЯ МОДУЛЕЙ (Blueprints)
# Указываем путь через точку: папка.файл
try:
    from routes.main import main_bp
    from routes.admin import admin_bp

    print("✅ Модули main и admin успешно подключены из папки routes")
except ModuleNotFoundError as e:
    print(f"❌ Ошибка: Не могу найти файлы в папке routes. Проверь наличие __init__.py. {e}")

# 5. Настройка почты (если нужна глобально)
from flask_mail import Mail

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='projectnumerology@gmail.com',
    MAIL_PASSWORD='ohkzqberuempfqhn'
)
mail = Mail(app)


# 6. Вспомогательный роут для синхронизации (если его нет в admin.py)
@app.route('/sync_all')
def sync_trigger():
    from services import sync_data_to_local
    if sync_data_to_local():
        return "Данные успешно синхронизированы в локальный бекап"
    return "Ошибка синхронизации", 500


@app.route('/admin/sync')
def admin_sync():
    """Роут для ручного запуска синхронизации баз"""
    try:
        from services import sync_data_to_local
        if sync_data_to_local():
            return "✅ Данные успешно перенесены из облака Neon в локальный бекап!", 200
        else:
            return "❌ Ошибка: Синхронизация не удалась. Проверь консоль сервера.", 500
    except Exception as e:
        return f"❌ Критическая ошибка при импорте или работе: {str(e)}", 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
