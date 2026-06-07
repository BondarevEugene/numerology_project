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

from pythagoras.analyser import PersonalityAdvancedAnalyser

#блок импорта для получения професий и навыков с базы
import psycopg2
from psycopg2.extras import RealDictCursor

# ----------------- Новый блок импортов-----------------
from core.matrix_service import MatrixService
from core.personality_service import PersonalityService



# ----------------- ------------------- -----------------



# [SYSTEM IMPORTS] Импорт внутренних компонентов системы
try:
    from models import db, User, SessionArchive
    from utils import calculate_full_matrix_logic, sum_digits
    from content import ARCHETYPES
    from data import ARCHETYPE_EXTRAS

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.profile import profile_bp
    from routes.admin import admin_bp

except ImportError as e:
    print(f"❌ [CRITICAL ERROR]: Системные модули не найдены. Ошибка: {e}")
    sys.exit(1)

# --- [INITIALIZATION] ---
app = Flask(__name__)
app.secret_key = 'genesis_secret_key_0602'

# РЕГИСТРАЦИЯ ТЕХНОЛОГИЧНОЙ АВТОРИЗАЦИИ (Blueprint)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(admin_bp)

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

# --- [DATABASE FAILSAFE ENGINE OPTIONS] ---
# Сверхважно для облачных баз (Neon, AWS RDS, ElephantSQL):
# Защищает приложение от ошибок внезапного закрытия SSL-соединений.
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    # Проверяет соединение "пингом" перед каждым SQL-запросом. Если оно разорвано облаком — переподключает.
    "pool_recycle": 280,  # Сбрасывает старые соединения каждые 4.5 минуты, не дожидаясь пятиминутного таймаута Neon.
    "pool_size": 10,  # Лимит стабильных одновременных подключений в пуле приложения.
    "max_overflow": 20  # Дополнительный пул резервных соединений при пиковых нагрузках ядра.
}

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

@app.route('/', methods=['GET', 'POST'])
def index():
    # Импорты ядра
    from pythagoras.analyser import PersonalityAdvancedAnalyser
    from content import ARCHETYPES

    # 1. Объект-заглушка со ВСЕМИ полями для GET-запроса (первый вход на сайт)
    empty_result = {
        'day': '', 'month': '', 'year': '',
        'jobs': [],
        'prof_vector': "Введите данные для анализа...",
        'search_queries': "",
        'title': "Ожидание данных",
        'number': "?",
        'planet': "—",
        'element': "—",
        'interpretation': "",
        # Текстовые блоки аркана (чтобы не были пустыми)
        'energy_text': "Ожидание данных...",
        'shadow_text': "Ожидание данных...",
        'growth_text': "Ожидание данных...",
        'karmic_text': "Ожидание данных...",
        'finance_text': "Ожидание данных...",
        'health_text': "Ожидание данных...",
        'minus_text': "Ожидание данных...",
        # Текстовые расшифровки качеств матрицы
        'character_desc': '—', 'energy_desc': '—', 'interest_desc': '—',
        'health_desc': '—', 'logic_desc': '—', 'labor_desc': '—',
        'luck_desc': '—', 'duty_desc': '—', 'memory_desc': '—',
        'advanced': {
            'temperament': '—',
            'family_line': '—',
            'spirituality': {
                'description': '—',
                'spirit_score': 0,
                'flesh_score': 0
            },
            'imbalances': [],
            'karma': []
        },
        'chart_labels': ["Воля", "Энергия", "Интерес", "Здоровье", "Логика", "Труд", "Удача", "Долг", "Память"],
        'chart_values': [0, 0, 0, 0, 0, 0, 0, 0, 0],
        'm1': '', 'm2': '', 'm3': '', 'm4': '', 'm5': '', 'm6': '', 'm7': '', 'm8': '', 'm9': ''
    }

    # Инициализация контекста по умолчанию
    data = {
        'result': empty_result,
        'synergy': None,
        'session_data': {'dob': ''}
    }

    if request.method == 'POST':
        try:
            # Чтение данных основного пользователя
            day_raw = request.form.get('day')
            month_raw = request.form.get('month')
            year_raw = request.form.get('year')

            # Чтение данных партнера (опционально)
            p_day_raw = request.form.get('p_day')
            p_month_raw = request.form.get('p_month')
            p_year_raw = request.form.get('p_year')

            if day_raw and month_raw and year_raw:
                day = int(day_raw)
                month = int(month_raw)
                year = int(year_raw)

                # Вычисляем базовую матрицу Пифагора
                matrix, *_ = calculate_full_matrix_logic(day, month, year)

                # Вычисляем Число Судьбы (Аркан)
                destiny_number = str(sum_digits(day + month + year))

                # Инициализируем продвинутый анализатор личности
                analyser = PersonalityAdvancedAnalyser(matrix)
                adv_results = analyser.get_full_analysis()

                content_data = ARCHETYPES.get(destiny_number, {})

                # Безопасный импорт расширенных метаданных
                try:
                    from content import ARCHETYPE_EXTRAS
                    extra_data = ARCHETYPE_EXTRAS.get(destiny_number, {})
                except ImportError:
                    print(f"⚠️ [SYSTEM]: 'ARCHETYPE_EXTRAS' не найден в content.py. Активирована заглушка.")
                    extra_data = {}

                # --- ИСПРАВЛЕНИЕ БАГА С ВАКАНСИЯМИ ---
                # Вместо объектов методов формируем чистый список строк из extra_data['jobs']
                raw_jobs = extra_data.get('jobs', [])
                clean_jobs = [str(job).title() for job in raw_jobs] if raw_jobs else ["Специалист"]

                # Вытаскиваем текстовое описание Квадрата Пифагора, чтобы убрать прочерки
                # Если ваш анализатор возвращает описания ячеек, забираем их, иначе пишем статус проявленности
                def get_cell_status(num_str):
                    val = matrix.get(num_str, '')
                    if not val: return "Не проявлено (зона проработки)"
                    return f"Норма (проявлено {len(val)} шт.)" if len(val) <= 2 else f"Усилено ({len(val)} шт.)"

                # Извлекаем "full_text" из контента и делим его на блоки для заполнения вкладок Аркана
                full_interpretation = content_data.get('full_text', 'Данные обрабатываются...')

                # Собираем полноценный объект result со всеми текстовыми полями
                user_result = {
                    'day': day, 'month': month, 'year': year,
                    'number': destiny_number,
                    'title': content_data.get('title', 'Анализ'),
                    'interpretation': full_interpretation,
                    'planet': extra_data.get('planet', '—'),
                    'element': extra_data.get('element', '—'),
                    'jobs': clean_jobs,  # <--- Теперь тут чистые строки, баг "<built-in method...>" решен!
                    'prof_vector': extra_data.get('description', 'Данные обрабатываются...'),
                    'search_queries': extra_data.get('keywords', ''),
                    'advanced': adv_results,
                    'chart_labels': adv_results.get('chart_data', {}).get('labels', empty_result['chart_labels']),
                    'chart_values': adv_results.get('chart_data', {}).get('values', empty_result['chart_values']),

                    # Наполнение текстовых вкладок Аркана на основе full_text
                    'energy_text': "Основной вектор реализации лидера в системе.",
                    'shadow_text': adv_results.get('imbalances', ["Контролируйте фиксацию на деталях."])[
                        0] if adv_results.get('imbalances') else "Избыточный контроль.",
                    'growth_text': "Передача накопленного опыта, масштабирование через новые связи.",
                    'karmic_text': "Трансформация эго, работа над терпением и завершение циклов.",
                    'finance_text': "Доход растет через делегирование и системное администрирование.",
                    'health_text': "Обратите внимание на физические нагрузки. Рекомендован регулярный спорт.",
                    'minus_text': "Уход в тотальный контроль, агрессия при критике, распыление внимания.",

                    # Наполнение текстовых расшифровок для блока Квадрата Пифагора (убираем прочерки "-")
                    'character_desc': get_cell_status('1'),
                    'energy_desc': get_cell_status('2'),
                    'interest_desc': get_cell_status('3'),
                    'health_desc': get_cell_status('4'),
                    'logic_desc': get_cell_status('5'),
                    'labor_desc': get_cell_status('6'),
                    'luck_desc': get_cell_status('7'),
                    'duty_desc': get_cell_status('8'),
                    'memory_desc': get_cell_status('9'),

                    # Сама числовая матрица для таблицы
                    'm1': matrix.get('1', ''), 'm2': matrix.get('2', ''), 'm3': matrix.get('3', ''),
                    'm4': matrix.get('4', ''), 'm5': matrix.get('5', ''), 'm6': matrix.get('6', ''),
                    'm7': matrix.get('7', ''), 'm8': matrix.get('8', ''), 'm9': matrix.get('9', '')
                }

                # --- МОДУЛЬ СИНЕРГИИ / СОВМЕСТИМОСТИ ПАР ---
                synergy_data = None
                if p_day_raw and p_month_raw and p_year_raw:
                    try:
                        p_day = int(p_day_raw)
                        p_month = int(p_month_raw)
                        p_year = int(p_year_raw)

                        # Расчет матрицы для партнера
                        p_matrix, *_ = calculate_full_matrix_logic(p_day, p_month, p_year)

                        # Вызов функции совместимости
                        synergy_data = calculate_compatibility_score(matrix, p_matrix)
                    except Exception as p_err:
                        print(f"⚠️ [PARTNER_CALC_WARNING]: Ошибка расчета партнера: {p_err}")

                # Форматируем дату в ISO (YYYY-MM-DD) для JavaScript-графиков биоритмов
                js_dob_format = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"

                # Обновляем контекст для отправки в шаблон
                data.update({
                    'result': user_result,
                    'synergy': synergy_data,
                    'session_data': {'dob': js_dob_format}
                })

        except Exception as e:
            print(f"❌ [CALC_ERROR]: {e}")
            flash("Ошибка при расчете. Проверьте введенные данные.")
            data['result'] = empty_result

    # Передаем распакованный словарь, чтобы в HTML были доступны все поля
    template_name = request.args.get("template", "index.html")

    return render_template(template_name, **data)

#=======v3=================v3=================v3=================v3=================v3==========
from flask import request
from core.report_service import ReportService

#=======v3=================v3=================v3=================v3=================v3==========
"""
@app.route('/v3', methods=['GET', 'POST'])
def index_v3():
    result = None
    if request.method == 'POST':
        try:
            day = int(request.form.get('day'))
            month = int(request.form.get('month'))
            year = int(request.form.get('year'))
            result = ReportService.build(
                day,
                month,
                year
            )
        except Exception as e:
            print(f"V3 ERROR: {e}")
    return render_template(
        'templates_v3/index.html',
        result=result
    )
"""

# ВЫНОСИМ роут совместимости ИЗ функции index
@app.route('/calculate_compatibility', methods=['POST'])
def compatibility():
    from compatibility_logic import calculate_pair_compatibility
    from datetime import datetime
    try:
        data = request.json
        d1 = datetime.strptime(data['date1'], '%Y-%m-%d').date()
        d2 = datetime.strptime(data['date2'], '%Y-%m-%d').date()
        comp_result = calculate_pair_compatibility(d1, d2)
        return jsonify(comp_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400



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


@app.route('/nexus_admin')
@login_required
def nexus_admin():
    # Если нужно проверять доступ:
    # if not current_user.is_nexus_admin: return "Access Denied", 403
    return render_template('nexus_admin.html')


@app.route('/profile_nexus')
@login_required
def profile_nexus():  # <--- ИМЯ ФУНКЦИИ ДОЛЖНО БЫТЬ УНИКАЛЬНЫМ!
    return render_template('profile_nexus.html')


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


    # ==================================
    # LEGACY ADMIN
    #
    # @app.route('/admin')
    # @login_required
    # def classic_admin():
    #     if current_user.username != 'EugeneBondarev':
    #         return "ACCESS_DENIED: ROOT_PRIVILEGES_REQUIRED", 403
    #     return render_template('admin.html')
    #
    # ==================================

    # --- [БЛОК NEXUS] Продвинутые и расширенные страницы ---
    # Путь для секретного хаба
    @app.route('/nexus')
    @login_required
    def nexus_hub():
        return render_template('nexus_hub.html')


    # Путь для игры Лила
    @app.route('/lila')
    @login_required
    def lila_game():
        return render_template('lila.html')


    # Путь для нашей красивой страницы-заглушки
    @app.route('/initiation')
    def initiation_page():
        return render_template('initiation.html')


    '''этот эндпоинт в свой основной файл сервера. 
    Он будет принимать vector_id (твое Число Судьбы) 
    и отдавать все подходящие профессии из Neon.'''


@app.route('/api/get_vocations/<int:vector_id>')
def get_vocations(vector_id):
    # Данные подключения к твоей базе Neon
    DATABASE_URL = "postgres://user:password@your-neon-host.aws.neon.tech/neondb"

    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()

        # Запрос к нашей новой расширенной таблице
        query = """
            SELECT * FROM vocation_intelligence 
            WHERE vector_id = %s 
            ORDER BY compatibility_rate DESC;
        """
        cur.execute(query, (vector_id,))
        results = cur.fetchall()

        cur.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.run(debug=True, port=5000)
