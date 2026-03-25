import os
import requests
import pdfkit
from datetime import datetime
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# Импорт дополнительных данных
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

# Настройка путей для PDF
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
    full_text = db.Column(db.Text)
    shadow_side = db.Column(db.Text)
    growth_point = db.Column(db.Text)
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
def calculate_compatibility_score(matrix1, matrix2):
    if not matrix1 or not matrix2: return None
    score = 0
    details = []
    # Энергия (2-5-8)
    e1 = matrix1['2'] + matrix1['5'] + matrix1['8']
    e2 = matrix2['2'] + matrix2['5'] + matrix2['8']
    if abs(e1 - e2) <= 1:
        score += 35
        details.append("Высокий энергетический резонанс.")
    else:
        score += 15
        details.append("Разный темп жизни: требуется подстройка.")
    # Быт (3-6-9)
    s1 = matrix1['3'] + matrix1['6'] + matrix1['9']
    s2 = matrix2['3'] + matrix2['6'] + matrix2['9']
    if (s1 + s2) >= 6:
        score += 35
        details.append("Сильный материальный фундамент.")
    else:
        score += 20
        details.append("Союз на почве идей, а не быта.")
    # Дух (1-4-7)
    sp1 = matrix1['1'] + matrix1['4'] + matrix1['7']
    sp2 = matrix2['1'] + matrix2['4'] + matrix2['7']
    if abs(sp1 - sp2) <= 2:
        score += 30
        details.append("Единство жизненных целей.")
    return {"percent": min(score, 100), "notes": details}


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
    report = []
    for num in '123456789':
        count = matrix.get(num, 0)
        if count in meanings[num]:
            report.append(f"<b>{num}:</b> {meanings[num][count]}")
    return report


def get_real_jobs(keyword):
    try:
        url = f"https://api.hh.ru/vacancies?text={keyword}&per_page=3"
        response = requests.get(url, headers={'User-Agent': 'Genesis'}, timeout=5)
        if response.status_code == 200:
            return [{'title': i['name'], 'salary': 'По договоренности', 'url': i['alternate_url'],
                     'employer': i['employer']['name']} for i in response.json().get('items', [])]
    except:
        pass
    return []


def create_pdf_report(name, result, professions, extras, compatibility, pif_report):
    # Упрощенная версия для примера
    styled_html = f"<html><body><h1>{result.title}</h1><p>Клиент: {name}</p></body></html>"
    filename = f"Genesis_{name}.pdf"
    try:
        pdfkit.from_string(styled_html, filename, configuration=PDF_CONFIG)
        return filename
    except:
        return None


# --- МАРШРУТЫ ---
@app.route('/', methods=['GET', 'POST'])
def index():
    data = {
        'result': None, 'professions': None, 'extras': None,
        'compatibility': None, 'pif_matrix': None, 'real_jobs': [],
        'pdf_file': None, 'email': None, 'pif_full_report': [],
        'synergy': None
    }

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        day, month, year = request.form.get('day'), request.form.get('month'), request.form.get('year')
        p_day, p_month, p_year = request.form.get('p_day'), request.form.get('p_month'), request.form.get('p_year')

        if day and month and year:
            arch_num = str(calculate_digit(day))
            result = ArchetypeContent.query.filter_by(number=arch_num).first()
            prof_data = ProfessionContent.query.filter_by(number=arch_num).first()

            # Матрица пользователя
            u_date = f"{day.zfill(2)}{month.zfill(2)}{year}"
            pif_matrix = calculate_pythagoras(u_date)
            pif_report = get_detailed_interpretation(pif_matrix)

            # Совместимость
            synergy_data = None
            if p_day and p_month and p_year:
                p_date = f"{p_day.zfill(2)}{p_month.zfill(2)}{p_year}"
                p_matrix = calculate_pythagoras(p_date)
                synergy_data = calculate_compatibility_score(pif_matrix, p_matrix)

            num = int(arch_num)
            comp = {
                "perfect": f"{(num + 2) % 9 + 1}, {(num + 5) % 9 + 1}",
                "challenge": str((num + 3) % 9 + 1),
                "partner_desc": result.partner_type if result else "Не определен"
            }

            prof_str = prof_data.list_csv if prof_data else "Специалист"
            jobs = get_real_jobs(prof_str.split(',')[0])

            # Сохранение в БД
            record = AnalysisRecord(name=name, email=email, birth_date=f"{day}-{month}-{year}", archetype=arch_num,
                                    professions=prof_str)
            db.session.add(record)
            db.session.commit()

            pdf_file = create_pdf_report(name, result, prof_str, ARCHETYPE_EXTRAS.get(arch_num, {}), comp, pif_report)

            data.update({
                'result': result, 'professions': prof_str, 'extras': ARCHETYPE_EXTRAS.get(arch_num, {}),
                'compatibility': comp, 'pif_matrix': pif_matrix, 'real_jobs': jobs,
                'pdf_file': pdf_file, 'email': email, 'pif_full_report': pif_report, 'synergy': synergy_data
            })

    return render_template('index.html', **data)


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)