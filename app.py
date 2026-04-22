import os
from flask import Flask, render_template, request, session
from flask_mail import Mail, Message
from sqlalchemy import create_engine

# 1. Основное приложение
app = Flask(__name__)
app.secret_key = 'genesis_secret_key_0602'

# 2. Настройка источников данных
NEON_URL = "postgresql://neondb_owner:npg_7uV2YfNbIeWd@ep-black-water-a2o4465m-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"
LOCAL_DB_URL = "sqlite:///backup_archetypes.db"

# 2.1. Проверка доступности Neon (Failover)
def select_database():
    primary = os.getenv('DATABASE_URL', NEON_URL)
    try:
        # Пробуем быстрое подключение (таймаут 3 сек)
        engine = create_engine(primary, connect_args={'connect_timeout': 3})
        with engine.connect() as conn:
            print("🔌 Подключено к основной базе (Neon)")
            return primary
    except Exception as e:
        print(f"⚠️ Neon недоступен, использую локальный бекап. Ошибка: {e}")
        return LOCAL_DB_URL

app.config['SQLALCHEMY_DATABASE_URI'] = select_database()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Импорт моделей и инициализация БД
from models import db, ArchetypeContent, UserRecord, Article

if 'sqlalchemy' not in app.extensions:
    db.init_app(app)

# 4. Импорт логики (Services & Mind Logic)
try:
    from services import CareerService
    from mind_logic import calculate_full_matrix_logic, NODES_INFO, sum_digits
except ImportError as e:
    print(f"⚠️ Ошибка импорта: {e}")

# 5. Конфигурация почты
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='projectnumerology@gmail.com',
    MAIL_PASSWORD='ohkzqberuempfqhn'
)
mail = Mail(app)

# --- МОДЕЛИ ДАННЫХ (ПОЛНЫЙ СПИСОК ИЗ ТВОЕГО ФАЙЛА) ---
# 1. Получаем основные данные архетипа из БД Neon
archetype_db = ArchetypeContent.query.filter_by(number=str(archetype_id)).first()


class ArchetypeContent(db.Model):
    __tablename__ = 'archetype_content'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True)
    title = db.Column(db.String(200))
    planet = db.Column(db.String(100))
    element = db.Column(db.String(50))
    tarot_arcane = db.Column(db.String(100))
    action_power = db.Column(db.Text)
    shadow_side = db.Column(db.Text)
    growth_point = db.Column(db.Text)
    realization = db.Column(db.Text)
    karmic_tasks = db.Column(db.Text)
    development_cycle = db.Column(db.Text)
    mind_power = db.Column(db.Text)
    life_result = db.Column(db.Text)
    partner_type = db.Column(db.Text)
    financial_tip = db.Column(db.Text)
    health_tips = db.Column(db.Text)
    exit_minus = db.Column(db.Text)
    search_queries = db.Column(db.Text)
    coach_tips = db.relationship('DailyCoachTip', backref='archetype', lazy=True)


class DailyCoachTip(db.Model):
    __tablename__ = 'daily_coach_tips'
    id = db.Column(db.Integer, primary_key=True)
    archetype_id = db.Column(db.Integer, db.ForeignKey('archetype_content.id'))
    day_type = db.Column(db.String(20))
    phys_content = db.Column(db.Text)
    ment_content = db.Column(db.Text)
    harm_content = db.Column(db.Text)


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    title = db.Column(db.String(200))
    platform = db.Column(db.String(100))
    link = db.Column(db.String(500))
    archetype_num = db.Column(db.String(10))


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ProfessionContent(db.Model):
    __tablename__ = 'profession_content'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10))
    list_csv = db.Column(db.Text)


class UserRecord(db.Model):
    __tablename__ = 'user_records'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    archetype = db.Column(db.String(10))
    s_leadership = db.Column(db.Integer, default=50)
    s_comm = db.Column(db.Integer, default=50)
    s_empathy = db.Column(db.Integer, default=50)
    s_logic = db.Column(db.Integer, default=50)
    s_agile = db.Column(db.Integer, default=50)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def sum_digits(n):
    if not n or str(n) == '0': return 0
    clean_n = "".join(filter(str.isdigit, str(n)))
    if not clean_n: return 0
    s = sum(int(d) for d in clean_n)
    while s > 9: s = sum(int(d) for d in str(s))
    return s


def get_group(d):
    return str(sum_digits(d))


# --- API И АДМИНКА (ВСЕ ТВОИ РОУТЫ) ---
@app.route('/api/v1/coach/<arch_num>/<day_type>')
def api_get_coach(arch_num, day_type):
    arch = ArchetypeContent.query.filter_by(number=str(arch_num)).first()
    if not arch: return jsonify({"error": "Arch not found"}), 404
    tip = DailyCoachTip.query.filter_by(archetype_id=arch.id, day_type=day_type).first()
    if not tip: return jsonify({"error": "Tip not found"}), 404
    return jsonify({"body": tip.phys_content, "mind": tip.ment_content, "spirit": tip.harm_content})


@app.route('/api/v1/skills/<int:user_id>')
def api_get_skills(user_id):
    u = UserRecord.query.get(user_id)
    if not u: return jsonify({"error": "User not found"}), 404
    return jsonify({
        "labels": ["Лидерство", "Коммуникация", "Эмпатия", "Логика", "Agile"],
        "data": [u.s_leadership, u.s_comm, u.s_empathy, u.s_logic, u.s_agile],
        "user_name": u.name
    })


@app.route('/admin-auth', methods=['POST'])
def admin_auth():
    if request.json.get('password') == '0602':
        session['admin_logged_in'] = True
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 401


@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'): return "Доступ запрещен", 403
    archetypes = ArchetypeContent.query.order_by(ArchetypeContent.number.cast(db.Integer)).all()
    records = UserRecord.query.order_by(UserRecord.created_at.desc()).all()
    return render_template('admin.html', archetypes=archetypes, records=records)


# --- ГЛАВНЫЙ РОУТ (ИСПРАВЛЕННЫЙ) ---
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    matrix_raw = None
    matrix_desc = {}
    extra = {}
    jobs = []
    calc = None
    bio_matrix = None
    compatibility = None

    # Тренды (статьи)
    trends = Article.query.filter_by(category='Trends').limit(3).all()

    if request.method == 'POST':
        user_name = request.form.get('user_name', 'Искатель')
        day = request.form.get('day', '').strip()
        month = request.form.get('month', '').strip()
        year = request.form.get('year', '').strip()
        email = request.form.get('email', '')

        if day and month and year:
            archetype_id = sum_digits(day + month + year)

            # Получаем все данные архетипа (все 18 полей)
            db_content = ArchetypeContent.query.filter_by(number=str(archetype_id)).first()

            if db_content:
                result = db_content
                result.day, result.month, result.year = day, month, year

                # Для совместимости со старыми элементами шаблона
                extra = {
                    'planet': db_content.planet,
                    'element': db_content.element,
                    'tarot': db_content.tarot_arcane
                }

                # Вакансии
                search_q = db_content.search_queries if db_content.search_queries else "Консультант"
                try:
                    jobs = CareerService.get_vacancies(archetype_id, custom_keywords=search_q)
                except:
                    jobs = []

            # Матрица Пифагора
            try:
                matrix_raw = calculate_full_matrix_logic(day, month, year)
                matrix_desc = {k: NODES_INFO[k].get(v, "...") for k, v in matrix_raw.items() if k in NODES_INFO}
            except:
                pass

            # Биоэнергетика
            y_s = year[-2:] if len(year) >= 2 else year
            bio_matrix = {
                "physical": sum_digits(day), "energy": sum_digits(month), "emotional": sum_digits(y_s),
                "intellectual": sum_digits(int(day) + int(month)),
                "creative": sum_digits(int(month) + int(y_s)),
                "spiritual": sum_digits(int(day) + int(y_s))
            }

            # Сохранение в историю поиска
            try:
                new_rec = UserRecord(user_name=user_name, email=email, birth_date=f"{day}.{month}.{year}",
                                     archetype=db_content.title if db_content else "Архетип")
                db.session.add(new_rec)
                db.session.commit()
            except:
                db.session.rollback()

    return render_template('index.html',
                           result=result, matrix_raw=matrix_raw, matrix_desc=matrix_desc,
                           jobs=jobs, trends=trends, extra=extra, bio_matrix=bio_matrix)


# --- PDF (ИСПРАВЛЕННЫЙ ПУТЬ ДЛЯ GOOGLE) ---
@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    # Настройка для Google Cloud (Linux)
    path_wk = shutil.which("wkhtmltopdf") or '/usr/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=path_wk)

    user_name = request.form.get('user_name', 'Искатель')
    day = request.form.get('day')
    month = request.form.get('month')
    year = request.form.get('year')

    if not day: return "Нет данных даты", 400

    # 1. Расчет группы (как в основной логике)
    # Важно: используем ту же функцию sum_digits, что и в начале файла
    d_r = sum_digits(day)
    group_num = str(d_r)

    # 2. Получение данных из БД
    result = ArchetypeContent.query.filter_by(number=group_num).first()

    if not result:
        return f"Ошибка: Архетип {group_num} не найден в базе данных", 404

    # 3. Расчет Психоматрицы (Пифагора)
    # Собираем строку из всех чисел даты и доп. чисел
    m_r = sum_digits(month)
    y_r = sum_digits(year)
    # Дополнительные числа Пифагора
    n1 = sum(int(d) for d in (day + month + year))
    n2 = sum(int(d) for d in str(n1))
    # n3 = n1 - (первая цифра дня * 2)
    first_digit = int(day[0] if day[0] != '0' else day[1])
    n3 = abs(n1 - (first_digit * 2))
    n4 = sum(int(d) for d in str(n3))

    all_digits = day + month + year + str(n1) + str(n2) + str(n3) + str(n4)

    matrix = {}
    for i in range(1, 10):
        cnt = all_digits.count(str(i))
        matrix[str(i)] = str(i) * cnt if cnt > 0 else "-"

        # Данные для шаблона pdf_print_template (УМ, ДЕЙСТВИЕ и т.д.)
        calc = {
            'mind': d_r,
            'action': m_r,
            'realization': y_r,
            'final': sum_digits(d_r + m_r + y_r),
            'dharma': sum_digits(d_r + m_r)
        }

        # Рендерим (используем pdf_template.html, который с таблицами)
        rendered_html = render_template('pdf_template.html',
                                        result=result,
                                        matrix=matrix,
                                        calc=calc,
                                        user_name=user_name,
                                        day=day, month=month, year=year)

        path_wk = shutil.which("wkhtmltopdf") or '/usr/bin/wkhtmltopdf'
        if not path_wk and os.path.exists(r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'):
            path_wk = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

        options = {
            'page-size': 'A4',
            'encoding': "UTF-8",
            'enable-local-file-access': '',
            'quiet': ''
        }

        try:
            pdf = pdfkit.from_string(rendered_html, False, configuration=config, options=options)
            return (pdf, 200, {
                'Content-Type': 'application/pdf',
                'Content-Disposition': f'attachment; filename="Genesis_Report.pdf"'
            })
        except Exception as e:
            return f"Ошибка PDFKit: {str(e)}", 500

    # 5. Конфигурация PDF
    path_wk = shutil.which("wkhtmltopdf") or r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wk)

    options = {
        'page-size': 'A4',
        'encoding': "UTF-8",
        'margin-top': '15mm',
        'margin-bottom': '15mm',
        'enable-local-file-access': ''
    }

    try:
        pdf = pdfkit.from_string(rendered_html, False, configuration=config, options=options)
        return (pdf, 200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': f'attachment; filename="Genesis_Report_{user_name}.pdf"'
        })
    except Exception as e:
        return f"Ошибка генерации: {str(e)}", 500


@app.route('/send_pdf', methods=['POST'])
def send_pdf():
    email = request.form.get('email')
    html_content = request.form.get('html_to_pdf')
    user_name = request.form.get('user_name', 'Искатель')

    if not email: return "Email не указан", 400

    path_wk = shutil.which("wkhtmltopdf") or r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    try:
        config = pdfkit.configuration(wkhtmltopdf=path_wk)
        pdf = pdfkit.from_string(html_content, False, configuration=config)

        msg = Message(f"Ваш отчет Genesis: {user_name}",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = f"Здравствуйте, {user_name}! Во вложении ваш персональный цифровой анализ Genesis."
        msg.attach("Genesis_Report.pdf", "application/pdf", pdf)
        mail.send(msg)
        return "Отчет успешно отправлен на вашу почту!"
    except Exception as e:
        return f"Ошибка отправки: {str(e)}", 500


@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        recipient = request.form.get('email')
        html_content = request.form.get('html_content')

        if not recipient:
            return "Email не указан", 400

        msg = Message("Ваш цифровой профиль | Genesis Psychology",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[recipient])

        # Оборачиваем в базовый HTML, чтобы стили подхватились в почте
        msg.html = f"""
        <html>
            <body style="background-color: #050505; color: #b8b8b8; padding: 20px;">
                {html_content}
            </body>
        </html>
        """

        mail.send(msg)
        return "OK", 200
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return str(e), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    # Пытаемся взять порт из системы (для облака), если его нет — ставим 5000 (стандарт Flask)
    # Порт 8080 в Windows часто заблокирован системными службами
    port = int(os.environ.get('PORT', 5000))

    try:
        print(f"🚀 Запуск сервера на http://0.0.0.0:{port}")
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        print(f"❌ Не удалось запустить на порту {port}: {e}")
        # Если 5000 тоже занят, пробуем 5001
        app.run(host='0.0.0.0', port=5001, debug=True)
