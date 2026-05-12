"""
--------------------------------------------------------------------------------
PROJECT: Genesis HR® | Intelligence Systems
MODULE:  Core Application Kernel (app.py)
VERSION: 2.9.8 "ULTIMATE FULL"
DATE:    2024-05-21 (Updated: 2026-04-29)
AUTHORS: Genesis Development Team
--------------------------------------------------------------------------------
DESCRIPTION:
    Центральное управляющее ядро системы Genesis.
    Обеспечивает:
    - Отказоустойчивое соединение с БД (Failover Logic: Neon -> SQLite)
    - Протоколы авторизации и управления сессиями субъектов
    - Вычисление аналитических матриц и архетипов
    - Генерацию защищенных PDF-отчетов через шлюз wkhtmltopdf
    - Почтовую трансмиссию результатов (SMTP TLS)

CORE STACK:
    Flask, SQLAlchemy, Flask-Login, Flask-Mail, PDFKit
--------------------------------------------------------------------------------
"""

import os
import sys
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_mail import Mail, Message
import pdfkit
from sqlalchemy import create_engine, text

# [SYSTEM IMPORTS] Импорт внутренних компонентов системы
try:
    from models import db, User, SessionArchive
    from utils import calculate_full_matrix_logic, sum_digits
    from content import ARCHETYPES
    from data import ARCHETYPE_EXTRAS

    # Пытаемся импортировать Blueprint авторизации (если он в routes)
    try:
        from routes.auth import auth_bp
    except ImportError:
        from auth import auth_bp
except ImportError as e:
    print(f"❌ [CRITICAL ERROR]: Системные модули не найдены. Ошибка: {e}")
    sys.exit(1)

# --- [INITIALIZATION] ---
app = Flask(__name__)
app.secret_key = 'genesis_secret_key_0602'

# РЕГИСТРАЦИЯ ТЕХНОЛОГИЧНОЙ АВТОРИЗАЦИИ (Blueprint)
app.register_blueprint(auth_bp)

# --- [DATABASE CONFIGURATION] Конфигурация и Failover-логика ---
NEON_URL = "postgresql://neondb_owner:npg_EFN09eZPMqai@ep-damp-math-al92xna7-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require"
LOCAL_DB_URL = "sqlite:///genesis_final_v2.db"


def get_db_uri():
    """Проверка доступности основной базы и автоматический выбор узла."""
    uri = os.getenv('DATABASE_URL', NEON_URL).strip()
    try:
        # Проверка линка (таймаут 3 секунды)
        engine = create_engine(uri, connect_args={'connect_timeout': 3})
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"✅ [SYSTEM]: Внешний узел DB активен.")
        return uri
    except Exception:
        print("⚠️ [SYSTEM]: Внешний узел недоступен. Переход на локальный протокол (SQLite).")
        return LOCAL_DB_URL


app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- [MAIL SYSTEM CONFIG] ---
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='projectnumerology@gmail.com',
    MAIL_PASSWORD='ohkzqberuempfqhn',
    MAIL_DEFAULT_SENDER='projectnumerology@gmail.com'
)

# Инициализация сервисов
db.init_app(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# --- [CORE ROUTING] ---

@app.route('/', methods=['GET', 'POST'])  # РАЗРЕШИЛИ POST
def index():
    """
    Главный входной шлюз.
    Обеспечивает отображение интерфейса даже без расчета.
    """
    result = None

    # Объект-заглушка, чтобы блоки не исчезали до расчета
    empty_result = {
        'jobs': [],
        'prof_vector': "Введите данные для анализа...",
        'search_queries': "",
        'title': "Ожидание данных",
        'number': "?",
        'planet': "—",
        'element': "—"
    }

    if request.method == 'POST':
        try:
            # Получаем данные из формы в сайдбаре
            day = int(request.form.get('day'))
            month = int(request.form.get('month'))
            year = int(request.form.get('year'))

            # Вызываем вашу логику расчета
            matrix, *_ = calculate_full_matrix_logic(day, month, year)
            arcane_key = str(sum_digits(day + month + year))

            # Подтягиваем данные из контента
            content_data = ARCHETYPES.get(arcane_key, {})
            extra_data = ARCHETYPE_EXTRAS.get(arcane_key, {})

            # Формируем итоговый объект для шаблона
            result = {
                'day': day, 'month': month, 'year': year,
                'number': arcane_key,
                'title': content_data.get('title', 'Анализ'),
                'planet': extra_data.get('planet', '—'),
                'element': extra_data.get('element', '—'),
                'jobs': extra_data.get('jobs', []),  # Передаем вакансии
                'prof_vector': extra_data.get('description', 'Данные обрабатываются...'),
                'search_queries': extra_data.get('keywords', '')
            }
        except Exception as e:
            print(f"❌ [CALC_ERROR]: {e}")
            flash("Ошибка при расчете. Проверьте введенные данные.")
            result = empty_result
    else:
        # Если это просто открытие страницы (GET), показываем пустые блоки
        result = empty_result

    return render_template('index.html', result=result)


@app.route('/profile')
@login_required
def profile():
    """Личный кабинет субъекта с аналитикой матрицы."""
    try:
        u_date = current_user.birth_date
        d, m, y = u_date.day, u_date.month, u_date.year

        # Полная логика вычисления из модуля utils
        matrix, *_ = calculate_full_matrix_logic(d, m, y)
        arcane_key = str(sum_digits(d + m + y))

        content_data = ARCHETYPES.get(arcane_key, {})
        extra_data = ARCHETYPE_EXTRAS.get(arcane_key, {})

        # Архив последних сессий доступа
        user_sessions = SessionArchive.query.filter_by(user_id=current_user.id) \
            .order_by(SessionArchive.created_at.desc()).limit(5).all()

        return render_template('profile.html',
                               user=current_user,
                               matrix=matrix,
                               arcane_key=arcane_key,
                               content=content_data,
                               extra=extra_data,
                               user_sessions=user_sessions)
    except Exception as e:
        print(f"❌ [PROFILE_ERROR]: {e}")
        return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Инициация нового субъекта в системе (резервный роут)."""
    if request.method == 'POST':
        # (Вся логика обычно в auth_bp, но сохраняем для совместимости)
        flash('Используйте протокол авторизации Blueprint')
        return redirect(url_for('auth.register'))

    # Возвращаем твой HTML-шаблон регистрации, если он нужен здесь
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Вход в систему под защищенным ключом."""
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            return redirect(url_for('profile'))
        flash('INVALID ACCESS KEY')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Завершение текущей сессии."""
    logout_user()
    return redirect(url_for('login'))


# --- [PDF GENERATION ENGINE] ---

@app.route('/generate_pdf_report', methods=['POST'])
@login_required
def generate_pdf_report():
    """Генерация PDF-отчета и отправка по Email."""
    try:
        data = request.get_json()
        email = data.get('email')
        stats = data.get('stats')

        # Формирование печатной формы
        rendered_html = render_template(
            'pdf_print_template.html',
            user_name=current_user.full_name,
            day=current_user.birth_date.day,
            month=current_user.birth_date.month,
            year=current_user.birth_date.year,
            calc=stats,
            result={'title': 'Genesis Personal Analysis'}
        )

        # Путь к исполняемому файлу wkhtmltopdf
        path_wk = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wk) if os.path.exists(path_wk) else None

        options = {
            'encoding': "UTF-8",
            'enable-local-file-access': None,
            'quiet': ''
        }

        pdf = pdfkit.from_string(rendered_html, False, configuration=config, options=options)

        # Трансмиссия письма
        msg = Message(
            subject=f"Genesis HR | Отчет: {current_user.full_name}",
            recipients=[email]
        )
        msg.body = f"Внимание! Сформирован зашифрованный цифровой профиль для: {current_user.full_name}"
        msg.attach(f"Genesis_{current_user.full_name}.pdf", "application/pdf", pdf)

        mail.send(msg)
        return "OK", 200
    except Exception as e:
        print(f"❌ [PDF_ENGINE_ERROR]: {e}")
        return str(e), 500


# --- [KERNEL START] Запуск ядра системы ---
if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print(f"✅ [SYSTEM]: Ядро Genesis HR функционирует в режиме {datetime.now().year}")
        except Exception as e:
            print(f"⚠️ [STARTUP_WARN]: {e}")


    # --- [БЛОК NEXUS] Продвинутые и расширенные страницы ---
    # Путь для секретного хаба
    @app.route('/nexus')
    @login_required
    def nexus_hub():
        return render_template('nexus_hub.html')


    # Путь для расширенного профиля Nexus
    @app.route('/profile_nexus')
    @login_required
    def profile_nexus():
        return render_template('profile_nexus.html')


    @app.route('/initiation')
    def initiation():
        return render_template('initiation.html')


    # Путь для игры Лила
    @app.route('/lila')
    @login_required
    def lila_game():
        return render_template('lila.html')


    # Путь для нашей красивой страницы-заглушки
    @app.route('/initiation')
    def initiation_page():
        return render_template('initiation.html')


    # Запуск сервера
    app.run(debug=True, port=5000)
