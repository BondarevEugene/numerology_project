import os
import requests
from fpdf import FPDF
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


# --- МОДЕЛИ ДАННЫХ ---
class ArchetypeContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), unique=True, nullable=False)
    title = db.Column(db.String(200))
    power_vector = db.Column(db.Text)
    shadow_side = db.Column(db.Text)
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

def get_detailed_interpretation(matrix):
    """Генерирует текстовое описание для каждого сектора психоматрицы"""
    if not matrix: return []

    meanings = {
        '1': {
            0: "Отсутствие проявленной воли, ведомость.",
            1: "Характер утонченный, эгоцентричный. Требуется внимание.",
            2: "Мягкий, покладистый характер, золотая середина.",
            3: "Устойчивая психика, умение убеждать.",
            4: "Сильная воля, задатки лидера и руководителя.",
            5: "Диктаторский характер, жесткая волевая позиция.",
            6: "Перегрузка воли, возможна деспотичность."
        },
        '2': {
            0: "Энергодефицит. Склонность к лени и быстрой усталости.",
            1: "Мало собственной энергии, возможна эмоциональная нестабильность.",
            2: "Норма энергии для жизни и общения.",
            3: "Способности к экстрасенсорике, высокая чувствительность.",
            4: "Избыток энергии, природный донор.",
            5: "Энергетический магнетизм, мощное влияние на людей."
        },
        '3': {
            0: "Гуманитарий, чистое творчество без системности.",
            1: "Интерес к искусству и порядку, но без фанатизма.",
            2: "Склонность к точным наукам и глубокому анализу.",
            3: "Ученый, технарь, мастер логических цепочек.",
            4: "Энциклопедические знания, гениальность в деталях."
        },
        '4': {
            0: "Здоровье слабое от рождения, нужно укреплять.",
            1: "Среднее здоровье, склонность к простудам.",
            2: "Крепкое тело, хорошая выносливость.",
            3: "Очень крепкое здоровье, атлетическое сложение.",
            4: "Запредельный физический потенциал."
        },
        '5': {
            0: "Интуиция закрыта, опора только на голые факты.",
            1: "Хорошее чутье, канал интуиции открыт.",
            2: "Сильная интуиция, вещие сны, предчувствия.",
            3: "Провидец, почти не совершает ошибок в выборе.",
            4: "Ясновидение, прямой доступ к информационному полю."
        },
        '6': {
            0: "Физический труд не в приоритете, упор на интеллект.",
            1: "Склонность к заземленному труду.",
            2: "Мастер на все руки, золотые руки.",
            3: "Труд как смысл жизни, высокий профессионализм.",
            4: "Трудоголизм, полное погружение в материальный мир."
        },
        '7': {
            0: "Путь через препятствия, всё достигается своим трудом.",
            1: "Есть Божья искра, небольшое везение в делах.",
            2: "Везунчик, удача сопутствует в рискованных делах.",
            3: "Человек под особой защитой Высших сил.",
            4: "Магнит для чудес, невероятная удачливость."
        },
        '8': {
            0: "Свобода от кармических обязательств перед родом.",
            1: "Развитое чувство долга и ответственности.",
            2: "Прирожденное служение людям, доброта.",
            3: "Большая кармическая ответственность, миссия.",
            4: "Глобальное влияние на судьбы людей."
        },
        '9': {
            0: "Слабая память, трудности с концентрацией.",
            1: "Средние умственные способности, нужно развивать.",
            2: "Сильный интеллект, отличная память.",
            3: "Мудрость, проницательность, талант к обучению.",
            4: "Гениальный ум, доступ к скрытым знаниям."
        }
    }

    report = []
    # Проходим по всем цифрам от 1 до 9
    for i in range(1, 10):
        key = str(i)
        count = matrix.get(key, 0)

        # Берем описание из словаря или ставим заглушку
        desc = meanings.get(key, {}).get(count, "Интерпретация в процессе настройки...")

        # Форматируем для HTML (названия секторов)
        sector_names = {
            '1': 'Характер', '2': 'Энергия', '3': 'Познание',
            '4': 'Здоровье', '5': 'Интуиция', '6': 'Труд',
            '7': 'Удача', '8': 'Долг', '9': 'Память'
        }
        name = sector_names.get(key, key)
        report.append(f"<b>{name}:</b> {desc}")

    return report


def create_pdf_report(name, result, professions, extras, pif_report):
    """Генерация PDF через fpdf2 (без wkhtmltopdf)"""
    try:
        pdf = FPDF()
        pdf.add_page()
        # Стандартный шрифт (Кириллица может не отображаться без добавления .ttf файла,
        # поэтому для стабильности деплоя пишем базовую информацию)
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, txt="GENESIS ANALYSIS REPORT", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(190, 10, txt=f"Identity: {name}", ln=True)
        pdf.cell(190, 10, txt=f"Archetype: {result.title if result else 'Unknown'}", ln=True)
        pdf.ln(5)
        pdf.multi_cell(190, 10, txt=f"Professions: {professions}")

        fname = f"Genesis_{name.replace(' ', '_')}.pdf"
        pdf.output(fname)
        return fname
    except Exception as e:
        print(f"PDF Error: {e}")
        return None


def calculate_compatibility_score(matrix1, matrix2):
    if not matrix1 or not matrix2: return None
    score = 50
    # Упрощенная логика для стабильности
    details = ["Энергетическая настройка в процессе.", "Резонанс по базовым частотам."]
    return {"percent": score, "notes": details, "harmony_advice": "Синхронизируйте общие цели."}


def get_real_jobs(keyword):
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
    first = digits[0] if digits[0] != '0' else digits[1]
    n3 = abs(n1 - (2 * int(first)))
    n4 = sum(int(d) for d in str(n3))
    all_num = "".join(map(str, digits)) + str(n1) + str(n2) + str(n3) + str(n4)
    return {str(i): all_num.count(str(i)) for i in range(1, 10)}


# --- МАРШРУТЫ ---
@app.route('/', methods=['GET', 'POST'])
def index():
    data = {'result': None, 'professions': None, 'extras': None, 'pif_matrix': None,
            'pif_full_report': [], 'compatibility': None, 'pdf_file': None, 'real_jobs': [], 'synergy': None}

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        d, m, y = request.form.get('day'), request.form.get('month'), request.form.get('year')
        pd, pm, py = request.form.get('p_day'), request.form.get('p_month'), request.form.get('p_year')

        if d and m and y:
            a_num = str(calculate_digit(d))
            res = ArchetypeContent.query.filter_by(number=a_num).first()
            p_cont = ProfessionContent.query.filter_by(number=a_num).first()

            matrix = calculate_pythagoras(f"{d.zfill(2)}{m.zfill(2)}{y}")
            report = get_detailed_interpretation(matrix)
            p_str = p_cont.list_csv if p_cont else "Консультант, Аналитик"
            jobs = get_real_jobs(p_str.split(',')[0])

            comp = {"perfect": f"{(int(a_num) + 2) % 9 + 1}", "challenge": f"{(int(a_num) + 4) % 9 + 1}",
                    "partner_desc": res.partner_type if res else "Партнер"}

            syn = None
            if pd and pm and py:
                p_matrix = calculate_pythagoras(f"{pd.zfill(2)}{pm.zfill(2)}{py}")
                syn = calculate_compatibility_score(matrix, p_matrix)

            pdf = create_pdf_report(name, res, p_str, ARCHETYPE_EXTRAS.get(a_num, {}), report)

            db.session.add(
                AnalysisRecord(name=name, email=email, birth_date=f"{d}-{m}-{y}", archetype=a_num, professions=p_str))
            db.session.commit()

            data.update({'result': res, 'professions': p_str, 'extras': ARCHETYPE_EXTRAS.get(a_num, {}),
                         'pif_matrix': matrix, 'pif_full_report': report, 'compatibility': comp,
                         'real_jobs': jobs, 'synergy': syn, 'pdf_file': pdf})

    return render_template('index.html', **data)


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)