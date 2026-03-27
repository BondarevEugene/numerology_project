import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'genesis_v2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- МОДЕЛИ ДАННЫХ (Расширены до максимума, чтобы принять все данные из init_db) ---

class ArchetypeContent(db.Model):
    __tablename__ = 'archetype_content'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True)
    title = db.Column(db.String(200))
    planet = db.Column(db.String(100))

    # Поля для твоего нового интерфейса (index.html)
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

    # ПОЛЯ-ЗАГЛУШКИ (Для совместимости со старым init_db.py)
    # Если скрипт передает эти данные, они просто сохранятся в БД
    full_text = db.Column(db.Text)
    shadow_side = db.Column(db.Text)
    avoid_spheres = db.Column(db.Text)
    partner_type = db.Column(db.Text)
    financial_tip = db.Column(db.Text)
    business_potential = db.Column(db.Text)
    health_tips = db.Column(db.Text)
    mission = db.Column(db.Text)
    recommendations = db.Column(db.Text)


# Заглушка для модели профессий (часто встречается в init_db)
class ProfessionContent(db.Model):
    __tablename__ = 'profession_content'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)


# --- ЛОГИКА ---

def get_group(d):
    try:
        return str((int(d) - 1) % 9 + 1)
    except:
        return "1"


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    matrix_raw = None
    if request.method == 'POST':
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')

        group_num = get_group(day)
        result = ArchetypeContent.query.filter_by(number=group_num).first()

        # Матрица (заглушка для рендера)
        s = f"{day}{month}{year}"
        matrix_raw = {f"c{i + 1}": s[i] if i < len(s) else "?" for i in range(9)}

    return render_template('index.html', result=result, matrix_raw=matrix_raw)


# --- API ДЛЯ АДМИНКИ ---

@app.route('/admin/get/<num>')
def admin_get(num):
    content = ArchetypeContent.query.filter_by(number=num).first()
    if content:
        cols = content.__table__.columns.keys()
        return jsonify({
            'status': 'success',
            'data': {c: getattr(content, c) for c in cols}
        })
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