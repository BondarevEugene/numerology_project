import os
import re
import shutil
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# Предполагаем, что CareerService описан в твоем services.py
from services import CareerService
import pdfkit
from datetime import datetime

app = Flask(__name__)
# Секретный ключ нужен для работы сессий (пароля)
app.secret_key = 'genesis_secret_key_0602'

# Настройки базы данных
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'genesis_v2.db')
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
    action_power = db.Column(db.Text)
    shadow_side = db.Column(db.Text)
    growth_point = db.Column(db.Text)
    realization = db.Column(db.Text)
    karmic_tasks = db.Column(db.Text)
    development_cycle = db.Column(db.Text)
    mind_power = db.Column(db.Text)
    life_result = db.Column(db.Text)
    partner_type = db.Column(db.Text)
    # Поля для совместимости
    financial_tip = db.Column(db.Text)
    health_tips = db.Column(db.Text)


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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def sum_digits(n):
    if not n or str(n) == '0': return 0
    s = sum(int(d) for d in str(n) if d.isdigit())
    while s > 9:
        s = sum(int(d) for d in str(s))
    return s


def get_group(d):
    return str(sum_digits(d))


# --- ЛОГИКА ПАРОЛЯ ---
@app.route('/admin-auth', methods=['POST'])
def admin_auth():
    # Простая проверка для prompt из JS
    password = request.json.get('password')
    if password == '0602':
        session['admin_logged_in'] = True
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 401


# --- РОУТЫ АДМИНКИ ---
@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return "Доступ запрещен. Используйте ключ на главной.", 403

    archetypes = ArchetypeContent.query.order_by(ArchetypeContent.number).all()
    profs = ProfessionContent.query.all()
    records = UserRecord.query.order_by(UserRecord.created_at.desc()).all()

    # Считаем статистику для графиков
    stats = {}
    for r in records:
        stats[r.archetype] = stats.get(r.archetype, 0) + 1

    return render_template('admin.html',
                           archetypes=archetypes,
                           profs=profs,
                           records=records,
                           stats=stats)


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
            # Очищаем теги ТОЛЬКО в заголовке и планете,
            # чтобы в текстах оставалось форматирование (<b>, <ul> и т.д.)
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


# --- ОСНОВНОЙ РОУТ ---
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    matrix_raw = None
    jobs = []

    if request.method == 'POST':
        user_name = request.form.get('user_name', 'Искатель')
        email = request.form.get('user_email')  # Добавляем получение email
        day = request.form.get('day', '').strip()
        month = request.form.get('month', '').strip()
        year = request.form.get('year', '').strip()
        country = request.form.get('country', 'ua')

        if day and month and year:
            group_num = get_group(day)
            result = ArchetypeContent.query.filter_by(number=str(group_num)).first()

            # Сохраняем искателя в базу (Клиенты)
            new_rec = UserRecord(
                name=user_name,
                email=email,  # <--- Передаем email в модель
                archetype=group_num
            )
            db.session.add(new_rec)
            db.session.commit()

            # Матрица Винчи
            d_r, m_r, y_r = sum_digits(day), sum_digits(month), sum_digits(year)
            matrix_raw = {
                "c1": d_r, "c2": m_r, "c3": sum_digits(d_r + m_r),
                "c4": y_r, "c5": sum_digits(d_r + y_r), "c6": sum_digits(m_r + y_r),
                "c7": sum_digits(d_r + m_r + y_r)
            }

            # Карьера
            if result:
                prof_entry = ProfessionContent.query.filter_by(number=str(result.number)).first()
                keywords = prof_entry.list_csv if prof_entry else None
                jobs = CareerService.get_vacancies(result, country=country, custom_keywords=keywords)

    return render_template('index.html', result=result, matrix_raw=matrix_raw, jobs=jobs)


# --- PDF ЭКСПОРТ ---
@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    html_content = request.form.get('html_to_pdf')
    path_wk = shutil.which("wkhtmltopdf") or r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wk)
    pdf = pdfkit.from_string(html_content, False, configuration=config, options={'encoding': "UTF-8", 'quiet': ''})
    return (pdf, 200, {'Content-Type': 'application/pdf', 'Content-Disposition': 'attachment; filename="Genesis.pdf"'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)