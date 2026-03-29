import os
import re
import shutil
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from services import CareerService
import pdfkit
from leela_module.leela_logic import leela_bp

app = Flask(__name__)

# Регистрация модуля Лилы
app.register_blueprint(leela_bp, url_prefix='/leela')

# Настройки базы данных
basedir = os.path.abspath(os.path.dirname(__file__))
# Используем genesis_v2.db как в твоем исходнике
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

    # ТРИАДА (Сила, Тень, Рост)
    action_power = db.Column(db.Text)  # Вектор Силы (Голубой блок)
    shadow_side = db.Column(db.Text)  # Теневая Ловушка (Красный блок)
    growth_point = db.Column(db.Text)  # Точка Роста (Золотой блок)

    # ОСНОВНЫЕ БЛОКИ
    realization = db.Column(db.Text)  # Социальная реализация
    karmic_tasks = db.Column(db.Text)  # Кармические задачи
    development_cycle = db.Column(db.Text)  # Цикл развития
    mind_power = db.Column(db.Text)  # Потенциал Разума

    # ДОПОЛНИТЕЛЬНО
    dharma = db.Column(db.Text)
    life_result = db.Column(db.Text)
    financial_tip = db.Column(db.Text)
    health_tips = db.Column(db.Text)
    partner_type = db.Column(db.Text)  # Совместимость

    # ТЕХНИЧЕСКИЕ (оставляем для совместимости)
    search_keywords = db.Column(db.Text)
    power_vector = db.Column(db.Text)
    shadow_trap = db.Column(db.Text)
    cycle = db.Column(db.Text)


class ProfessionContent(db.Model):
    __tablename__ = 'profession_content'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10))
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    list_csv = db.Column(db.Text)


# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def sum_digits(n):
    if not n or str(n) == '0': return 0
    s = sum(int(d) for d in str(n) if d.isdigit())
    while s > 9:
        s = sum(int(d) for d in str(s))
    return s


def get_group(d):
    return str(sum_digits(d))


# --- РОУТЫ АДМИНКИ ---

@app.route('/admin/get_profs/<num>')
def admin_get_profs(num):
    prof = ProfessionContent.query.filter_by(number=str(num)).first()
    return jsonify({'status': 'success', 'list_csv': prof.list_csv if prof else ''})


@app.route('/admin/update_profs', methods=['POST'])
def admin_update_profs():
    data = request.json
    num = data.get('number')
    if not num: return jsonify({'status': 'error'})
    prof = ProfessionContent.query.filter_by(number=str(num)).first()
    if not prof:
        prof = ProfessionContent(number=str(num))
        db.session.add(prof)
    prof.list_csv = data.get('list_csv', '')
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/admin/get/<num>')
def admin_get(num):
    content = ArchetypeContent.query.filter_by(number=str(num)).first()
    if content:
        cols = [c.name for c in ArchetypeContent.__table__.columns]
        return jsonify({
            'status': 'success',
            'data': {c: getattr(content, c) for c in cols}
        })
    return jsonify({'status': 'error', 'message': 'Архетип не найден'})


@app.route('/admin/update', methods=['POST'])
def admin_update():
    data = request.json
    num = data.get('number')
    if not num: return jsonify({'status': 'error'})

    content = ArchetypeContent.query.filter_by(number=str(num)).first()
    if not content:
        content = ArchetypeContent(number=str(num))
        db.session.add(content)

    for key, value in data.items():
        if hasattr(content, key) and key != 'id':
            # Очистка заголовка от HTML тегов
            if key == 'title':
                value = re.sub('<[^<]+?>', '', value).strip()
            setattr(content, key, value)

    db.session.commit()
    return jsonify({'status': 'success'})


# --- ОСНОВНОЙ РОУТ ---

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    dharma_data = None
    matrix_raw = None
    compatibility_result = None
    jobs = []

    if request.method == 'POST':
        day = request.form.get('day', '').strip()
        month = request.form.get('month', '').strip()
        year = request.form.get('year', '').strip()
        p_day = request.form.get('p_day', '').strip()
        country = request.form.get('country', 'ua')

        if day and month and year:
            group_num = get_group(day)
            result = ArchetypeContent.query.filter_by(number=str(group_num)).first()

            # Дхарма
            try:
                d_num = sum_digits(int(day) + int(month))
                dharma_data = ArchetypeContent.query.filter_by(number=str(d_num)).first()
            except:
                dharma_data = None

            # Матрица Винчи
            d_r, m_r, y_r = sum_digits(day), sum_digits(month), sum_digits(year)
            matrix_raw = {
                "c1": d_r, "c2": m_r, "c3": sum_digits(d_r + m_r),
                "c4": y_r, "c5": sum_digits(d_r + y_r), "c6": sum_digits(m_r + y_r),
                "c7": sum_digits(d_r + m_r + y_r)
            }

            # Совместимость
            if p_day:
                pair_num = sum_digits(sum_digits(day) + sum_digits(p_day))
                compatibility_result = ArchetypeContent.query.filter_by(number=str(pair_num)).first()

            # Карьера (HH.ru)
            if result:
                prof_entry = ProfessionContent.query.filter_by(number=str(result.number)).first()
                keywords = prof_entry.list_csv if prof_entry else None
                jobs = CareerService.get_vacancies(result, country=country, custom_keywords=keywords)

    return render_template('index.html',
                           result=result,
                           dharma_data=dharma_data,
                           matrix_raw=matrix_raw,
                           compatibility_result=compatibility_result,
                           jobs=jobs)


# --- ЭКСПОРТ PDF ---

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    html_content = request.form.get('html_to_pdf')
    if not html_content: return "Ошибка данных", 400

    # Авто-поиск пути wkhtmltopdf (для Render и Windows)
    path_wk = shutil.which("wkhtmltopdf") or r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

    options = {
        'page-size': 'A4', 'margin-top': '10mm', 'margin-right': '10mm',
        'margin-bottom': '10mm', 'margin-left': '10mm', 'encoding': "UTF-8",
        'no-outline': None, 'enable-local-file-access': None, 'quiet': ''
    }

    try:
        config = pdfkit.configuration(wkhtmltopdf=path_wk)
        pdf = pdfkit.from_string(html_content, False, configuration=config, options=options)
        return (pdf, 200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename="Genesis_Report.pdf"'
        })
    except Exception as e:
        return f"Ошибка PDF: {e}", 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)