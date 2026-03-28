import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from services import CareerService

app = Flask(__name__)

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
    mind_power = db.Column(db.Text)
    action_power = db.Column(db.Text)
    realization = db.Column(db.Text)
    power_vector = db.Column(db.Text)
    shadow_trap = db.Column(db.Text)
    growth_point = db.Column(db.Text)
    cycle = db.Column(db.Text)
    karmic_tasks = db.Column(db.Text)
    dharma = db.Column(db.Text)  # Здесь храним тот самый текст про долг души
    life_result = db.Column(db.Text)
    search_keywords = db.Column(db.Text)
    full_text = db.Column(db.Text)
    shadow_side = db.Column(db.Text)
    avoid_spheres = db.Column(db.Text)
    partner_type = db.Column(db.Text)
    financial_tip = db.Column(db.Text)
    business_potential = db.Column(db.Text)
    health_tips = db.Column(db.Text)
    mission = db.Column(db.Text)
    recommendations = db.Column(db.Text)


class ProfessionContent(db.Model):
    __tablename__ = 'profession_content'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10))
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    list_csv = db.Column(db.Text)


# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def get_group(d):
    """Определяет базовый архетип по дню (1-9)"""
    try:
        val = int(d)
        return str((val - 1) % 9 + 1)
    except:
        return "1"


def sum_digits(n):
    """Редукция числа до однозначного (1-9) для Дхармы"""
    res = sum(int(d) for d in str(n) if d.isdigit())
    return res if res <= 9 else sum_digits(res)


# --- РОУТЫ ---
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    dharma_data = None
    matrix_raw = None
    jobs = []

    if request.method == 'POST':
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')
        country = request.form.get('country', 'ua')

        # 1. Расчет Основного Архетипа (по дню)
        group_num = get_group(day)
        result = ArchetypeContent.query.filter_by(number=group_num).first()

        # 2. Расчет Дхармы (День + Месяц)
        try:
            d_val = int(day)
            m_val = int(month)
            dharma_num = str(sum_digits(d_val + m_val))
            # Загружаем контент Дхармы из записи с соответствующим номером
            dharma_data = ArchetypeContent.query.filter_by(number=dharma_num).first()
        except:
            dharma_data = None

        # 3. Матрица (визуальный ряд)
        s = f"{day}{month}{year}"
        matrix_raw = {f"c{i + 1}": s[i] if i < len(s) else "?" for i in range(9)}

        # 4. Вакансии (по основному архетипу)
        if result:
            jobs = CareerService.get_vacancies(result, country=country)

    return render_template('index.html',
                           result=result,
                           dharma_data=dharma_data,  # Передаем объект Дхармы
                           matrix_raw=matrix_raw,
                           jobs=jobs)


@app.route('/admin/get/<num>')
def admin_get(num):
    content = ArchetypeContent.query.filter_by(number=num).first()
    if content:
        cols = [c.name for c in ArchetypeContent.__table__.columns]
        return jsonify({'status': 'success', 'data': {c: getattr(content, c) for c in cols}})
    return jsonify({'status': 'error'})


@app.route('/admin/update', methods=['POST'])
def admin_update():
    data = request.json
    num = data.get('number')
    content = ArchetypeContent.query.filter_by(number=num).first()
    if not content:
        content = ArchetypeContent(number=num)
        db.session.add(content)

    for key, value in data.items():
        if hasattr(content, key):
            setattr(content, key, value)

    db.session.commit()
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)