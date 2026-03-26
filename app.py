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

# --- НАСТРОЙКА PDF ---
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
    power_vector = db.Column(db.Text)
    shadow_side = db.Column(db.Text)  # Это и есть "Теневая сторона"
    growth_point = db.Column(db.Text)
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
def calculate_compatibility_score(matrix1, matrix2):
    """Расчет Synergy Resonance"""
    if not matrix1 or not matrix2: return None
    score, details = 0, []

    # Упрощенная логика для примера
    e1 = matrix1.get('2', 0) + matrix1.get('5', 0) + matrix1.get('8', 0)
    e2 = matrix2.get('2', 0) + matrix2.get('5', 0) + matrix2.get('8', 0)

    if abs(e1 - e2) <= 1:
        score += 40
        details.append("Высокий энергетический резонанс.")
    else:
        score += 20
        details.append("Требуется подстройка темпов жизни.")

    final_score = min(score + 30, 100)  # Базовый уровень + расчет
    return {"percent": final_score, "notes": details, "harmony_advice": "Синхронизируйте общие цели."}


def get_real_jobs(keyword):
    """HH.ru Live интеграция"""
    try:
        url = f"https://api.hh.ru/vacancies?text={keyword}&per_page=3"
        r = requests.get(url, headers={'User-Agent': 'Genesis'}, timeout=5)
        if r.status_code == 200:
            return [{'title': i['name'], 'url': i['alternate_url'], 'employer': i['employer']['name']} for i in
                    r.json().get('items', [])]
    except:
        pass
    return []


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


# --- МАРШРУТЫ ---
@app.route('/', methods=['GET', 'POST'])
def index():
    # Полный список ключей, которые ожидает твой HTML
    data = {
        'result': None,
        'professions': None,
        'extras': None,
        'pif_matrix': None,
        'pif_full_report': [], # Добавил это
        'compatibility': None,  # Добавил это
        'pdf_file': None,
        'real_jobs': [],
        'synergy': None
    }

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        d, m, y = request.form.get('day'), request.form.get('month'), request.form.get('year')
        pd, pm, py = request.form.get('p_day'), request.form.get('p_month'), request.form.get('p_year')

        if d and m and y:
            a_num = str(calculate_digit(d))
            res = ArchetypeContent.query.filter_by(number=a_num).first()
            p_cont = ProfessionContent.query.filter_by(number=a_num).first()

            # 1. Матрица и ПОЛНЫЙ отчет (интерпретация)
            u_date = f"{d.zfill(2)}{m.zfill(2)}{y}"
            matrix = calculate_pythagoras(u_date)
            report = get_detailed_interpretation(matrix) # Вот это было пропущено

            # 2. Профессии и Вакансии
            p_str = p_cont.list_csv if p_cont else "Консультант, Аналитик, Специалист"
            jobs = get_real_jobs(p_str.split(',')[0])

            # 3. Расчет классической совместимости (Числа силы)
            num = int(a_num)
            comp = {
                "perfect": f"{(num + 2) % 9 + 1}, {(num + 5) % 9 + 1}",
                "challenge": str((num + 3) % 9 + 1),
                "partner_desc": res.partner_type if res else "Гармоничный партнер"
            }

            # 4. Расчет Синергии (если введена дата партнера)
            syn = None
            if pd and pm and py:
                p_matrix = calculate_pythagoras(f"{pd.zfill(2)}{pm.zfill(2)}{py}")
                syn = calculate_compatibility_score(matrix, p_matrix)

            # 5. Генерация PDF (передаем все накопленные данные)
            # Убедись, что твоя функция create_pdf_report принимает эти аргументы
            pdf = create_pdf_report(name, res, p_str, ARCHETYPE_EXTRAS.get(a_num, {}), report)

            # 6. Сохранение в БД
            db.session.add(AnalysisRecord(
                name=name,
                email=email,
                birth_date=f"{d}-{m}-{y}",
                archetype=a_num,
                professions=p_str
            ))
            db.session.commit()

            # ОБНОВЛЯЕМ ДАННЫЕ ДЛЯ СТРАНИЦЫ
            data.update({
                'result': res,
                'professions': p_str,
                'extras': ARCHETYPE_EXTRAS.get(a_num, {}),
                'pif_matrix': matrix,
                'pif_full_report': report, # Теперь отчет попадет в HTML
                'compatibility': comp,     # Теперь Числа Силы появятся
                'real_jobs': jobs,
                'synergy': syn,
                'pdf_file': pdf
            })

    return render_template('index.html', **data)


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)