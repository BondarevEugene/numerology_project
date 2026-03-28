import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # 1. Импорт здесь
from services import CareerService # импорт сервиса карьеры из основного файла. пока так.

app = Flask(__name__) # 2. Сначала создаем app

# Настройки базы данных
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'genesis_v2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # 3. Потом создаем db
migrate = Migrate(app, db) # 4. И только ТЕПЕРЬ создаем migrate

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
    dharma = db.Column(db.Text)
    life_result = db.Column(db.Text)
    # Поля для умного поиска и совместимости
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
    list_csv = db.Column(db.Text)  # <--- Добавляем это поле для скрипта


def get_group(d):
    try:
        return str((int(d) - 1) % 9 + 1)
    except:
        return "1"


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    matrix_raw = None
    jobs = []
    country = request.form.get('country', 'ua') # 'ua' теперь значение по умолчанию, если вдруг придет пустой запрос

    if request.method == 'POST':
        # Собираем все пришедшие данные
        user_name = request.form.get('user_name')
        user_email = request.form.get('user_email')
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')
        partner_date = request.form.get('partner_date')

        # Основная логика поиска архетипа
        group_num = get_group(day)
        result = ArchetypeContent.query.filter_by(number=group_num).first()

        # Матрица
        s = f"{day}{month}{year}"
        matrix_raw = {f"c{i + 1}": s[i] if i < len(s) else "?" for i in range(9)}

        if result:
            jobs = CareerService.get_vacancies(result, country=country)

    return render_template('index.html',
                           result=result,
                           matrix_raw=matrix_raw,
                           jobs=jobs)


@app.route('/admin/get/<num>')
def admin_get(num):
    content = ArchetypeContent.query.filter_by(number=num).first()
    if content:
        cols = content.__table__.columns.keys()
        return jsonify({'status': 'success', 'data': {c: getattr(content, c) for c in cols}})
    return jsonify({'status': 'error'})


@app.route('/admin/update', methods=['POST'])
def admin_update():
    data = request.json
    content = ArchetypeContent.query.filter_by(number=data.get('number')).first()
    if not content:
        content = ArchetypeContent(number=data.get('number'))
        db.session.add(content)
    for key, value in data.items():
        if hasattr(content, key): setattr(content, key, value)
    db.session.commit()
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)