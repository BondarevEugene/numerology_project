import os
import time
import logging
from flask import Flask, jsonify, request, redirect, url_for
from flask_mail import Mail, Message
from flask_migrate import Migrate
from models import db, Order, UserRecord, Article

# =========================================================
# 1. ИНИЦИАЛИЗАЦИЯ И ЛОГИРОВАНИЕ
# =========================================================

app = Flask(__name__)

# Настраиваем «черный ящик» (логи).
# Уровень INFO позволит тебе видеть в консоли Google Cloud важные отчеты о работе.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================================================
# 2. КОНФИГУРАЦИЯ (Настройка систем)
# =========================================================

# Настройка Базы Данных: берем адрес из облака (DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Настройки «живучести» базы:
# pool_recycle — перезапуск соединения каждые 280 сек (чтобы не протухло)
# pool_pre_ping — проверка связи с базой перед каждым запросом
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 280,
    "pool_pre_ping": True,
}

# Секретный ключ для защиты сессий и куки
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-777')

# Почтовый модуль (SMTP): через него сайт будет слать отчеты клиентам
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

# =========================================================
# 3. ПОДКЛЮЧЕНИЕ МОДУЛЕЙ (Интеграция систем)
# =========================================================

db.init_app(app)  # Связываем базу данных с приложением
migrate = Migrate(app, db)  # Включаем систему миграций (изменения структуры таблиц)
mail = Mail(app)  # Запускаем почтовый движок

# Импортируем Блюпринты (Blueprints) — это части сайта, разделенные по папкам.
# Важно импортировать их здесь, чтобы избежать «зацикливания» программы.
from routes.main import main_bp
from routes.admin import admin_bp
from leela_module.leela_logic import leela_bp

# Регистрируем эти части в главном приложении:
app.register_blueprint(main_bp)  # Главная страница и расчеты
app.register_blueprint(admin_bp, url_prefix='/admin')  # Панель управления (доступ по /admin)
app.register_blueprint(leela_bp, url_prefix='/lila')  # Модуль игры Лила (доступ по /lila)


# =========================================================
# 4. ФУНКЦИИ УПРАВЛЕНИЯ (Logic Units)
# =========================================================

# Вместо before_first_request используем контекст приложения
with app.app_context():
    try:
        db.create_all()
        print("✅ Таблицы проверены/созданы успешно.")
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}")


@app.route('/')
def root():
    """
    Главный переключатель:
    Когда кто-то заходит просто на домен, этот код перенаправляет
    его на главную страницу модуля 'main'.
    """
    try:
        return redirect(url_for('main.index'))
    except Exception:
        # Если главная сломана, шлем на Лилу, чтобы юзер не видел ошибку
        return redirect('/lila')


@app.route('/api/payment/create', methods=['POST'])
def create_payment():
    """
    Движок платежей:
    Принимает данные (email, сумма), создает запись о заказе в базе
    и выдает ID заказа. В будущем сюда цепляется Юкасса или эквайринг.
    """
    try:
        data = request.get_json()
        email = data.get('email', 'guest@example.com')
        amount = data.get('amount', 199.0)

        # Генерируем уникальный номер заказа (префикс GEN + время)
        order_ref = f"GEN-{int(time.time())}"
        new_order = Order(order_id=order_ref, user_email=email, amount=amount, status='pending')

        db.session.add(new_order)  # Кладем в корзину БД
        db.session.commit()  # Сохраняем в БД навсегда

        return jsonify({'status': 'success', 'order_id': order_ref})
    except Exception as e:
        db.session.rollback()  # Если произошел сбой, откатываем изменения (чтобы не мусорить)
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/stats')
def get_stats():
    """
    Сбор разведданных (Визуализация):
    Считает количество пользователей в базе и отдает цифру для графиков.
    """
    try:
        user_count = UserRecord.query.count()
        return jsonify({
            'total_users': user_count,
            'server_status': 'operational',
            'server_time': time.strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception:
        return jsonify({'status': 'error', 'message': 'Database offline'})


# =========================================================
# 5. ОБРАБОТЧИКИ ОШИБОК (Заглушки)
# =========================================================

@app.errorhandler(404)
def page_not_found(e):
    """ Если боец зашел не туда — мягко возвращаем в строй """
    return "Такой страницы нет. Вернитесь на <a href='/'>базу</a>", 404


# =========================================================
# 6. КОМАНДА НА ЗАПУСК (Ignition)
# =========================================================

if __name__ == '__main__':
    # Берем порт, который нам выделил Google (обычно 8080)
    port = int(os.environ.get("PORT", 8080))
    # threaded=True — позволяет серверу обрабатывать несколько людей одновременно
    app.run(host='0.0.0.0', port=port, threaded=True)