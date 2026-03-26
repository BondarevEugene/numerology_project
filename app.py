import os
import requests
import pdfkit
from datetime import datetime
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy

# --- ИМПОРТ ДОПОЛНИТЕЛЬНЫХ ДАННЫХ ---
try:
    from data import ARCHETYPE_EXTRAS
except ImportError:
    ARCHETYPE_EXTRAS = {}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'genesis_v2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- НАСТРОЙКА PDF (wkhtmltopdf) ---
if os.name == 'nt':
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
else:
    path_wkhtmltopdf = '/usr/bin/wkhtmltopdf'

try:
    PDF_CONFIG = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
except:
    PDF_CONFIG = None


# --- МОДЕЛИ ДАННЫХ ---
class ArchetypeContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), unique=True, nullable=False)
    title = db.Column(db.String(200))
    # ДОБАВЛЕННЫЕ ПОЛЯ:
    power_vector = db.Column(db.Text)
    shadow_side = db.Column(db.Text)
    growth_point = db.Column(db.Text)
    # ОСТАЛЬНЫЕ ПОЛЯ:
    full_text = db.Column(db.Text)
    partner_type = db.Column(db.String(255))
    avoid_spheres = db.Column(db.Text)


class ProfessionContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), unique=True, nullable=False)
    list_csv = db.Column(db.Text)


class AnalysisRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    birth_date = db.Column(db.String(20))
    archetype = db.Column(db.String(10))
    professions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def calculate_digit(n):
    try:
        s = sum(int(d) for d in str(n) if d.isdigit())
        return s if s <= 9 else calculate_digit(s)
    except:
        return 1


def calculate_pythagoras(date_str):
    digits = [int(d) for d in str(date_str) if d.isdigit()]
    if not digits: return None
    n1 = sum(digits)
    n2 = sum(int(d) for d in str(n1))
    first = digits[0] if digits[0] != 0 else digits[1]
    n3 = abs(n1 - (2 * first))
    n4 = sum(int(d) for d in str(n3))
    all_num = "".join(map(str, digits)) + str(n1) + str(n2) + str(n3) + str(n4)
    return {str(i): all_num.count(str(i)) for i in range(1, 10)}


def get_detailed_interpretation(matrix):
    if not matrix: return []
    meanings = {
        '1': {1: "Эгоцентрик.", 2: "Мягкий характер.", 3: "Золотая середина.", 4: "Лидер.", 5: "Диктатор."},
        '2': {0: "Дефицит энергии.", 1: "Мало сил.", 2: "Норма.", 3: "Экстрасенс.", 4: "Донор."},
        '3': {0: "Гуманитарий.", 1: "Творчество.", 2: "Технарь.", 3: "Ученый."},
        '4': {0: "Здоровье слабое.", 1: "Среднее.", 2: "Крепкое.", 3: "Атлет."},
        '5': {0: "Логика слабая.", 1: "Интуит.", 2: "Провидец.", 3: "Стратег."},
        '6': {0: "Духовный поиск.", 1: "Ручной труд.", 2: "Мастер.", 3: "Трудоголик."},
        '7': {0: "Все сам.", 1: "Удача есть.", 2: "Везунчик.", 3: "Знак Ангела."},
        '8': {0: "Без долгов.", 1: "Ответственный.", 2: "Служение.", 3: "Карма семьи."},
        '9': {1: "Память средняя.", 2: "Умный.", 3: "Мудрец."}
    }
    return [f"<b>{n}:</b> {meanings[n][c]}" for n, c in matrix.items() if c in meanings[n]]


# --- PDF GENERATOR ---
def create_pdf_report(name, result, professions, extras, pif_report):
    pif_html = f"<h3>Психоматрица</h3><ul>{''.join([f'<li>{l}</li>' for l in pif_report])}</ul>" if pif_report else ""

    html = f"""
    <html><head><meta charset="UTF-8"><style>
        body {{ background: #060709; color: #a0a0a0; font-family: 'DejaVu Sans', sans-serif; padding: 40px; }}
        .title {{ color: #d4af37; font-size: 28px; text-align: center; text-transform: uppercase; }}
        .box {{ padding: 15px; border-radius: 5px; margin: 15px 0; background: #0c0e12; border-left: 4px solid #d4af37; }}
        .gold {{ color: #d4af37; font-weight: bold; }}
    </style></head><body>
        <div class="title">{result.title if result else "Genesis Report"}</div>
        <p style="text-align:center;">Identity: {name}</p>
        <div class="box">
            <span class="gold">Power Vector:</span> {result.power_vector if result else "-"}<br>
            <span class="gold">Shadow Side:</span> {result.shadow_side if result else "-"}<br>
            <span class="gold">Growth Point:</span> {result.growth_point if result else "-"}
        </div>
        <div class="box">Аркан: {extras.get('arcane', '-')} | Стихия: {extras.get('element', '-')}</div>
        <div>{result.full_text if result else ""}</div>
        {pif_html}
        <p><b>Рекомендуемые сферы:</b> {professions}</p>
    </body></html>
    """
    fname = f"Genesis_{name.replace(' ', '_')}.pdf"
    opts = {'encoding': "UTF-8", 'quiet': ''}
    try:
        pdfkit.from_string(html, fname, configuration=PDF_CONFIG, options=opts)
        return fname
    except Exception as e:
        print(f"PDF Error: {e}")
        return None


# --- МАРШРУТЫ ---
@app.route('/', methods=['GET', 'POST'])
def index():
    data = {'result': None, 'professions': None, 'extras': None, 'pif_matrix': None, 'pdf_file': None,
            'pif_full_report': []}

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        d, m, y = request.form.get('day'), request.form.get('month'), request.form.get('year')

        if d and m and y:
            a_num = str(calculate_digit(d))
            res = ArchetypeContent.query.filter_by(number=a_num).first()
            p_cont = ProfessionContent.query.filter_by(number=a_num).first()

            u_date = f"{d.zfill(2)}{m.zfill(2)}{y}"
            matrix = calculate_pythagoras(u_date)
            report = get_detailed_interpretation(matrix)
            p_str = p_cont.list_csv if p_cont else "Специалист"

            pdf = create_pdf_report(name, res, p_str, ARCHETYPE_EXTRAS.get(a_num, {}), report)

            db.session.add(
                AnalysisRecord(name=name, email=email, birth_date=f"{d}-{m}-{y}", archetype=a_num, professions=p_str))
            db.session.commit()

            data.update(
                {'result': res, 'professions': p_str, 'extras': ARCHETYPE_EXTRAS.get(a_num, {}), 'pif_matrix': matrix,
                 'pdf_file': pdf, 'pif_full_report': report})

    return render_template('index.html', **data)


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)