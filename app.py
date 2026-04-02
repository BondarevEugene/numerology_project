import os
import re
import shutil
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from weasyprint import HTML
import io

# Импорт сервисов и логики (убедись, что файлы лежат рядом)
try:
    from services import CareerService
    from mind_logic import NODES_INFO
    from data import ARCHETYPE_EXTRAS, PIF_DECODE
except ImportError as e:
    print(f"⚠️ Ошибка импорта модулей: {e}")

# Импорт сырых данных для инициализации
try:
    from content import ARCHETYPES
except ImportError:
    ARCHETYPES = {}

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'genesis_secret_key_0602')

# --- КОНФИГУРАЦИЯ ПОЧТЫ ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'projectnumerology@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'ohkzqberuempfqhn')
mail = Mail(app)

basedir = os.path.abspath(os.path.dirname(__file__))
# Поддержка PostgreSQL для Render
db_url = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'genesis_v2.db'))
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# --- МОДЕЛИ ДАННЫХ ---

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
    s = sum(int(d) for d in clean_n)
    while s > 9:
        s = sum(int(d) for d in str(s))
    return s


def get_group(d):
    return str(sum_digits(d))


# --- API ЭНДПОИНТЫ ---

@app.route('/api/v1/coach/<arch_num>/<day_type>')
def api_get_coach(arch_num, day_type):
    arch = ArchetypeContent.query.filter_by(number=str(arch_num)).first()
    if not arch: return jsonify({"error": "Arch not found"}), 404
    tip = DailyCoachTip.query.filter_by(archetype_id=arch.id, day_type=day_type).first()
    if not tip: return jsonify({"error": "Tip not found"}), 404
    return jsonify({
        "body": tip.phys_content,
        "mind": tip.ment_content,
        "spirit": tip.harm_content
    })


@app.route('/api/v1/skills/<int:user_id>')
def api_get_skills(user_id):
    u = UserRecord.query.get(user_id)
    if not u: return jsonify({"error": "User not found"}), 404
    return jsonify({
        "labels": ["Лидерство", "Коммуникация", "Эмпатия", "Логика", "Agile"],
        "data": [u.s_leadership, u.s_comm, u.s_empathy, u.s_logic, u.s_agile],
        "user_name": u.name
    })


# --- ЛОГИКА ПАРОЛЯ И АДМИНКИ ---

@app.route('/admin-auth', methods=['POST'])
def admin_auth():
    password = request.json.get('password')
    if password == '0602':
        session['admin_logged_in'] = True
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 401


@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return "Доступ запрещен. Используйте ключ на главной.", 403

    archetypes = ArchetypeContent.query.order_by(ArchetypeContent.number.cast(db.Integer)).all()
    profs = ProfessionContent.query.all()
    records = UserRecord.query.order_by(UserRecord.created_at.desc()).all()
    articles = Article.query.all()
    courses = Course.query.all()

    stats = {}
    for r in records:
        stats[r.archetype] = stats.get(r.archetype, 0) + 1

    return render_template('admin.html',
                           archetypes=archetypes,
                           profs=profs,
                           records=records,
                           stats=stats,
                           articles=articles,
                           courses=courses)


@app.route('/admin/get/<num>')
def admin_get(num):
    content = ArchetypeContent.query.filter_by(number=str(num)).first()
    if content:
        cols = [c.name for c in ArchetypeContent.__table__.columns]
        return jsonify({'status': 'success', 'data': {c: getattr(content, c) for c in cols}})
    return jsonify({'status': 'error'})


@app.route('/admin/get_profs/<num>')
def admin_get_profs(num):
    prof = ProfessionContent.query.filter_by(number=str(num)).first()
    return jsonify({'list_csv': prof.list_csv if prof else ''})


@app.route('/admin/update', methods=['POST'])
def admin_update():
    if not session.get('admin_logged_in'): return jsonify({'status': 'error'}), 403
    data = request.json if request.is_json else request.form
    num = data.get('number')
    if not num: return "Missing number", 400

    content = ArchetypeContent.query.filter_by(number=str(num)).first()
    if not content:
        content = ArchetypeContent(number=str(num))
        db.session.add(content)

    for key, value in data.items():
        if hasattr(content, key) and key != 'id':
            if key in ['title', 'planet']:
                value = re.sub('<[^<]+?>', '', str(value)).strip()
            setattr(content, key, value)

    try:
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/admin/update_profs', methods=['POST'])
def admin_update_profs():
    if not session.get('admin_logged_in'): return jsonify({'status': 'error'}), 403
    data = request.json if request.is_json else request.form
    num = data.get('number')
    prof = ProfessionContent.query.filter_by(number=str(num)).first()
    if not prof:
        prof = ProfessionContent(number=str(num))
        db.session.add(prof)
    prof.list_csv = data.get('list_csv', '')
    db.session.commit()
    return redirect(url_for('admin_panel')) if not request.is_json else jsonify({'status': 'success'})


@app.route('/admin/delete-record/<int:id>', methods=['POST'])
def delete_record(id):
    if not session.get('admin_logged_in'): return "Unauthorized", 403
    rec = UserRecord.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return redirect(url_for('admin_panel'))


# --- ОСНОВНОЙ РОУТ ПОРТАЛА ---

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    matrix_raw = None
    matrix_desc = {}
    extra = {}
    jobs = []
    calc = None
    user_id = None
    trends = Article.query.filter_by(category='Trends').order_by(Article.created_at.desc()).limit(3).all()

    if request.method == 'POST':
        user_name = request.form.get('user_name', 'Искатель')
        email = request.form.get('user_email')
        day = request.form.get('day', '').strip()
        month = request.form.get('month', '').strip()
        year = request.form.get('year', '').strip()
        country = request.form.get('country', 'ua')

        if day and month and year:
            group_num = get_group(day)
            result = ArchetypeContent.query.filter_by(number=str(group_num)).first()

            if 'ARCHETYPE_EXTRAS' in globals():
                extra = ARCHETYPE_EXTRAS.get(str(group_num), {})

            new_rec = UserRecord(
                name=user_name, email=email, archetype=group_num,
                s_leadership=75, s_comm=80, s_empathy=65, s_logic=70, s_agile=60
            )
            db.session.add(new_rec)
            db.session.commit()
            user_id = new_rec.id

            d_r, m_r, y_r = sum_digits(day), sum_digits(month), sum_digits(year)
            calc = {
                'mind': d_r, 'action': m_r, 'realization': y_r,
                'final': sum_digits(d_r + m_r + y_r),
                'dharma': sum_digits(d_r + m_r)
            }
            matrix_raw = {
                "c1": d_r, "c2": m_r, "c3": y_r,
                "c4": calc['dharma'], "c5": sum_digits(d_r + y_r),
                "c6": sum_digits(m_r + y_r), "c7": calc['final']
            }

            if 'NODES_INFO' in globals():
                all_digits = f"{day}{month}{year}{calc['mind']}{calc['action']}{calc['realization']}{calc['final']}"
                for n_id, info in NODES_INFO.items():
                    cnt = all_digits.count(n_id)
                    lvl = "low" if cnt <= 1 else "mid" if cnt <= 3 else "high"
                    matrix_desc[n_id] = {"name": info["name"], "text": info[lvl], "count": cnt}

            if result:
                prof_entry = ProfessionContent.query.filter_by(number=str(result.number)).first()
                keywords = result.search_queries if hasattr(result, 'search_queries') and result.search_queries else (
                    prof_entry.list_csv if prof_entry else None)
                try:
                    jobs = CareerService.get_vacancies(result.number, country=country, custom_keywords=keywords)
                except:
                    jobs = []

    return render_template('index.html',
                           result=result, matrix_raw=matrix_raw, matrix_desc=matrix_desc,
                           jobs=jobs, calc=calc, trends=trends, extra=extra,
                           user_id=user_id, pif_decode=PIF_DECODE if 'PIF_DECODE' in globals() else {})


# --- ЭКСПОРТ И ОТПРАВКА PDF (ОБНОВЛЕНО НА WEASYPRINT) ---

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    try:
        user_name = request.form.get('user_name', 'Искатель')
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')

        if not day: return "Нет данных даты", 400

        group_num = str(sum_digits(day))
        result = ArchetypeContent.query.filter_by(number=group_num).first()
        if not result: return f"Архетип {group_num} не найден", 404

        # Расчет Психоматрицы
        m_r, y_r = sum_digits(month), sum_digits(year)
        n1 = sum(int(d) for d in (day + month + year))
        n2 = sum(int(d) for d in str(n1))
        first_digit = int(day[0] if day[0] != '0' else day[1])
        n3 = abs(n1 - (first_digit * 2))
        n4 = sum(int(d) for d in str(n3))
        all_digits = day + month + year + str(n1) + str(n2) + str(n3) + str(n4)

        matrix = {str(i): (str(i) * all_digits.count(str(i)) if all_digits.count(str(i)) > 0 else "-") for i in
                  range(1, 10)}
        calc = {
            'mind': sum_digits(day), 'action': m_r, 'realization': y_r,
            'final': sum_digits(sum_digits(day) + m_r + y_r),
            'dharma': sum_digits(sum_digits(day) + m_r)
        }

        rendered_html = render_template('pdf_template.html',
                                        result=result, matrix=matrix, calc=calc,
                                        user_name=user_name, day=day, month=month, year=year)

        pdf = HTML(string=rendered_html).write_pdf()
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="Genesis_Report_{user_name}.pdf"'
        return response
    except Exception as e:
        return f"Ошибка генерации PDF: {str(e)}", 500


@app.route('/send_pdf', methods=['POST'])
def send_pdf():
    try:
        email = request.form.get('email')
        html_content = request.form.get('html_to_pdf')
        user_name = request.form.get('user_name', 'Искатель')

        if not email or not html_content: return "Данные не полные", 400

        pdf = HTML(string=html_content).write_pdf()
        msg = Message(f"Ваш отчет Genesis: {user_name}",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = f"Здравствуйте, {user_name}! Во вложении ваш персональный цифровой анализ Genesis."
        msg.attach(f"Genesis_Report_{user_name}.pdf", "application/pdf", pdf)
        mail.send(msg)
        return "Отчет успешно отправлен!"
    except Exception as e:
        return f"Ошибка отправки: {str(e)}", 500


@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        recipient = request.form.get('email')
        html_content = request.form.get('html_content')
        if not recipient: return "Email не указан", 400

        msg = Message("Ваш цифровой профиль | Genesis Psychology",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[recipient])
        msg.html = f"<html><body style='background-color: #050505; color: #b8b8b8; padding: 20px;'>{html_content}</body></html>"
        mail.send(msg)
        return "OK", 200
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)