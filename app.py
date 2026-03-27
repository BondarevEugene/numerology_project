import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Используем твою новую базу v2
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'genesis_v2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- МОДЕЛЬ ДАННЫХ (ВСЕ ТВОИ ПОЛЯ) ---
class ArchetypeContent(db.Model):
    __tablename__ = 'archetype_content'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True)  # Группа (1-9)
    title = db.Column(db.String(200))
    planet = db.Column(db.String(100))
    mind_power = db.Column(db.Text)
    action_power = db.Column(db.Text)
    realization = db.Column(db.Text)
    life_result = db.Column(db.Text)
    power_vector = db.Column(db.Text)
    shadow_trap = db.Column(db.Text)
    growth_point = db.Column(db.Text)
    dharma = db.Column(db.Text)
    cycle = db.Column(db.Text)
    karmic_tasks = db.Column(db.Text)


# --- ЛОГИКА РАСЧЕТОВ ---
def get_group_leader(d_str):
    mapping = {
        "1": "1", "10": "1", "19": "1", "28": "1",
        "2": "2", "11": "2", "20": "2", "29": "2",
        "3": "3", "12": "3", "21": "3", "30": "3",
        "4": "4", "13": "4", "22": "4", "31": "4",
        "5": "5", "14": "5", "23": "5",
        "6": "6", "15": "6", "24": "6",
        "7": "7", "16": "7", "25": "7",
        "8": "8", "17": "8", "26": "8",
        "9": "9", "18": "9", "27": "9"
    }
    return mapping.get(str(d_str), "1")


def calculate_pythagoras(date_str):
    digits = [int(d) for d in date_str if d.isdigit()]
    if not digits: return {}
    n1 = sum(digits)
    n2 = sum(int(d) for d in str(n1))
    first = digits[0] if digits[0] != 0 else (digits[1] if len(digits) > 1 else 0)
    n3 = abs(n1 - (2 * first))
    n4 = sum(int(d) for d in str(n3))
    all_num = "".join(map(str, digits)) + str(n1) + str(n2) + str(n3) + str(n4)
    return {str(i): (str(i) * all_num.count(str(i))) if all_num.count(str(i)) > 0 else "---" for i in range(1, 10)}


def get_personal_day_number(d, m):
    today = datetime.now()
    total = int(d) + int(m) + today.day + today.month + today.year
    while total > 9: total = sum(int(digit) for digit in str(total))
    return total


# --- МАРШРУТЫ ---
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    matrix_raw = {}
    day_advice = None

    if request.method == 'POST':
        d = request.form.get('day')
        m = request.form.get('month')
        y = request.form.get('year')

        if d and m and y:
            leader = get_group_leader(d)
            content = ArchetypeContent.query.filter_by(number=leader).first()

            # Собираем данные для отображения
            if content:
                result = {
                    'number': leader,
                    'title': content.title or f"Архетип {leader}",
                    'planet': content.planet,
                    'mind_power': content.mind_power,
                    'action_power': content.action_power,
                    'realization': content.realization,
                    'life_result': content.life_result,
                    'power_vector': content.power_vector,
                    'shadow_trap': content.shadow_trap,
                    'growth_point': content.growth_point,
                    'dharma': content.dharma,
                    'cycle': content.cycle,
                    'karmic_tasks': content.karmic_tasks
                }
            else:
                # Если в базе нет данных, создаем пустой объект, чтобы не было ошибок в шаблоне
                result = {'number': leader, 'title': f"Архетип {leader} (Данные не заполнены)"}

            matrix_raw = calculate_pythagoras(f"{d}{m}{y}")

            # Совет дня
            day_num = get_personal_day_number(d, m)
            advices = {
                1: "День новых начинаний. Время заявить о себе.",
                2: "День дипломатии. Слушайте интуицию, избегайте конфликтов.",
                3: "День творчества. Самовыражение принесет плоды.",
                4: "День порядка. Займитесь рутиной и фундаментом дел.",
                5: "День перемен. Будьте готовы к неожиданным встречам.",
                6: "День гармонии. Уделите время близким и дому.",
                7: "День анализа. Уединение пойдет на пользу мудрости.",
                8: "День достижений. Время масштабировать свои планы.",
                9: "День завершения. Отпустите старое, чтобы вошло новое."
            }
            day_advice = {"number": day_num, "text": advices.get(day_num)}

    return render_template('index.html', result=result, matrix_raw=matrix_raw, day_advice=day_advice)


@app.route('/admin/get/<num>')
def admin_get(num):
    item = ArchetypeContent.query.filter_by(number=str(num)).first()
    if item:
        return jsonify({'status': 'success', 'data': {c.name: getattr(item, c.name) for c in item.__table__.columns}})
    return jsonify({'status': 'empty'})


@app.route('/admin/update', methods=['POST'])
def admin_update():
    data = request.json
    num_str = str(data.get('number'))
    item = ArchetypeContent.query.filter_by(number=num_str).first()
    if not item:
        item = ArchetypeContent(number=num_str)
        db.session.add(item)
    for k, v in data.items():
        if hasattr(item, k): setattr(item, k, v)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    # Заглушка PDF (нужна библиотека reportlab)
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, "Genesis Scroll Report")
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="genesis.pdf", mimetype='application/pdf')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)