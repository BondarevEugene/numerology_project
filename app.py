import os
import re
import shutil
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
import io

try:
    from weasyprint import HTML

    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False
    print("⚠️ WeasyPrint не найден или не настроен (это нормально для Windows). PDF отключен локально.")

# --- ИНИЦИАЛИЗАЦИЯ ПРИЛОЖЕНИЯ ---
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'genesis_secret_key_0602')

# --- КОНФИГУРАЦИЯ БАЗЫ ДАННЫХ (NEON.TECH) ---
# Твоя прямая ссылка для подключения
NEON_DB_URL = "postgresql://neondb_owner:npg_cLG3oCesPw6A@ep-damp-math-al92xna7.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require"

# Приоритет переменной окружения (для Render), иначе используем Neon напрямую
db_url = os.environ.get('DATABASE_URL', NEON_DB_URL)

# Исправление протокола для SQLAlchemy 2.0
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- ДОБАВЬ ЭТИ ТРИ СТРОКИ НИЖЕ ---
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,  # Проверять живое ли соединение перед каждым запросом
    "pool_recycle": 300,  # Пересоздавать соединение каждые 5 минут
}

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- ПОЧТА ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'projectnumerology@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'ohkzqberuempfqhn')
mail = Mail(app)

# Импорт сервисов
try:
    from services import CareerService
except ImportError as e:
    CareerService = None
    print(f"⚠️ Ошибка импорта CareerService: {e}")


@app.after_request
def add_header(response):
    response.headers['Content-Security-Policy'] = "script-src 'self' 'unsafe-eval' 'unsafe-inline';"
    return response


# --- ВСТРОЕННЫЕ ДАННЫЕ (ПОЛНЫЕ) ---
NODES_INFO = {
    "1": {"name": "Характер и Воля",
          "low": "Склонность к сомнениям, потребность в поддержке, мягкость в принятии решений.",
          "mid": "Устойчивый характер, баланс эго и альтруизма, умение постоять за себя.",
          "high": "Сильная воля, лидерские качества, властность, мощная внутренняя опора."},
    "2": {"name": "Энергия Действия",
          "low": "Дефицит природной энергии, быстрая утомляемость, необходима подзарядка извне.",
          "mid": "Контактность, достаточный ресурс для общения и повседневных дел.",
          "high": "Избыток энергии, экстрасенсорные способности, высокая активность."},
    "3": {"name": "Познание и Наука",
          "low": "Гуманитарный склад, творческий хаос, интуитивное обучение.",
          "mid": "Интерес к наукам, технический склад ума, склонность к порядку.",
          "high": "Глубокие знания, педантичность, тяга к конструированию и сложным системам."},
    "4": {"name": "Здоровье и Тело",
          "low": "Слабый иммунитет от рождения, нужно внимательно следить за питанием и режимом.",
          "mid": "Среднее здоровье, важен регулярный спорт для поддержания тонуса.",
          "high": "Крепкое тело, высокая выносливость, мощный физический потенциал."},
    "5": {"name": "Логика и Интуиция",
          "low": "Интуитивное мышление, витание в облаках, принятие решений сердцем.",
          "mid": "Развитая логика, планирование, умение анализировать факты.",
          "high": "Стратегическое мышление, дар предвидения, сильный аналитический аппарат."},
    "6": {"name": "Труд и Мастерство",
          "low": "Творческий труд, нелюбовь к физической работе, поиск вдохновения.",
          "mid": "Мастер на все руки, склонность к созиданию, практичность.",
          "high": "Трудоголизм, власть через профессионализм, умение делать сложные вещи руками."},
    "7": {"name": "Удача и Судьба",
          "low": "Всего нужно добиваться своим трудом, жизнь как путь преодоления.",
          "mid": "Частичное везение, защита ангела-хранителя в критических ситуациях.",
          "high": "Баловень судьбы, огромный потенциал удачи, интуитивное попадание в поток."},
    "8": {"name": "Долг и Род",
          "low": "Свобода от жестких обязательств, поиск себя вне семейных сценариев.",
          "mid": "Развитое чувство ответственности перед близкими и социумом.",
          "high": "Жертвенность, служение обществу, глубокая связь с кармой рода."},
    "9": {"name": "Память и Мудрость",
          "low": "Рассеянность, нужно записывать идеи, акцент на текущем моменте.",
          "mid": "Хорошая память, высокая способность к обучению и анализу.",
          "high": "Блестящий ум, аналитический дар, мудрость, накопленная поколениями."}
}

SYNASTRY_TEXTS = {
    1: "Союз Лидеров. Вдохновляете друг друга, но избегайте борьбы за власть.",
    2: "Гармония Душ. Глубокое эмоциональное понимание и уют.",
    3: "Творческий Тандем. Союз полон идей, общения и общих проектов.",
    4: "Фундаментальная Опора. Крепкие отношения, построенные на стабильности.",
    5: "Ветер Перемен. Динамика, приключения и свобода в паре.",
    6: "Семейный Очаг. Забота, дом и глубокая привязанность.",
    7: "Духовное Единство. Глубокое связь на уровне интуиции и смыслов.",
    8: "Власть и Процветание. Идеальные партнеры для успеха и бизнеса.",
    9: "Кармическая Мудрость. Глубокий союз, завершающий важные жизненные уроки."
}

LINES_INFO = {
    "row1": {"name": "Целеустремленность (1-4-7)", "text": "Способность ставить цели и доводить их до конца."},
    "row2": {"name": "Семейность (2-5-8)", "text": "Стремление к созданию семьи и качество партнерских отношений."},
    "row3": {"name": "Стабильность (3-6-9)", "text": "Привычки, привязанность к быту и материальная устойчивость."},
    "col1": {"name": "Самооценка (1-2-3)", "text": "Внутренняя уверенность и выделение своего 'Я' из толпы."},
    "col2": {"name": "Зарабатывание (4-5-6)", "text": "Способность обеспечивать себя и семью материально."},
    "col3": {"name": "Талант (7-8-9)", "text": "Уровень божественной искры и реализации способностей."},
    "diag1": {"name": "Духовность (1-5-9)", "text": "Тяга к высшим смыслам, религии или философии."},
    "diag2": {"name": "Темперамент (3-5-7)", "text": "Сексуальная энергия и внешняя привлекательность."}
}


# --- МОДЕЛИ ДАННЫХ ---
class ArchetypeContent(db.Model):
    __tablename__ = 'archetype_content'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True)
    title = db.Column(db.String(200))
    planet = db.Column(db.String(100))
    element = db.Column(db.String(50))
    tarot_arcane = db.Column(db.Text)
    action_power = db.Column(db.Text)
    shadow_side = db.Column(db.Text)
    growth_point = db.Column(db.Text)
    realization = db.Column(db.Text)
    karmic_tasks = db.Column(db.Text)
    development_cycle = db.Column(db.Text)
    mind_power = db.Column(db.Text)
    life_result = db.Column(db.Text)
    partner_type = db.Column(db.Text)
    financial_tip = db.Column(db.Text)
    health_tips = db.Column(db.Text)
    exit_minus = db.Column(db.Text)
    search_queries = db.Column(db.Text)
    coach_tips = db.relationship('DailyCoachTip', backref='archetype', lazy=True)


class DailyCoachTip(db.Model):
    __tablename__ = 'daily_coach_tips'
    id = db.Column(db.Integer, primary_key=True)
    archetype_id = db.Column(db.Integer, db.ForeignKey('archetype_content.id'))
    day_type = db.Column(db.String(20))
    phys_content = db.Column(db.Text)
    ment_content = db.Column(db.Text)
    harm_content = db.Column(db.Text)


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    title = db.Column(db.String(200))
    platform = db.Column(db.String(100))
    link = db.Column(db.String(500))
    archetype_num = db.Column(db.String(10))


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


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
    s_leadership = db.Column(db.Integer, default=50)
    s_comm = db.Column(db.Integer, default=50)
    s_empathy = db.Column(db.Integer, default=50)
    s_logic = db.Column(db.Integer, default=50)
    s_agile = db.Column(db.Integer, default=50)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def sum_digits(n):
    if not n or str(n) == '0': return 0
    clean_n = "".join(filter(str.isdigit, str(n)))
    if not clean_n: return 0
    s = sum(int(d) for d in clean_n)
    while s > 9:
        s = sum(int(d) for d in str(s))
    return s


def calculate_full_matrix_logic(day, month, year):
    d_s, m_s, y_s = day.zfill(2), month.zfill(2), str(year)
    s_base = f"{d_s}{m_s}{y_s}"

    n1 = sum(int(c) for c in s_base if c.isdigit())
    n2 = sum(int(c) for c in str(n1))
    first_digit = int(d_s[0] if d_s[0] != '0' else d_s[1])
    n3 = abs(n1 - (first_digit * 2))
    n4 = sum(int(c) for c in str(n3))

    all_digits = s_base + str(n1) + str(n2) + str(n3) + str(n4)

    # 1. Матрица для точек
    matrix = {str(i): (str(i) * all_digits.count(str(i)) if all_digits.count(str(i)) > 0 else "-") for i in
              range(1, 10)}

    # 2. Навыки для Радара
    def get_score(chars, weight=20):
        count = sum(all_digits.count(c) for c in chars)
        return min(20 + (count * weight), 100)

    skills = {
        "labels": ["Лидерство", "Энергия", "Логика", "Гибкость", "Эмпатия"],
        "data": [get_score('1', 15), get_score('2', 25), get_score('5', 35), get_score('36', 15), get_score('84', 20)]
    }

    # 3. Линии матрицы
    def get_l(keys):
        return sum(len(matrix[k]) if matrix[k] != "-" else 0 for k in keys)

    matrix_lines = {
        "row1": {"name": "Целеустремленность", "score": get_l(['1', '4', '7'])},
        "row2": {"name": "Семейность", "score": get_l(['2', '5', '8'])},
        "row3": {"name": "Стабильность", "score": get_l(['3', '6', '9'])},
        "col1": {"name": "Самооценка", "score": get_l(['1', '2', '3'])},
        "col2": {"name": "Зарабатывание", "score": get_l(['4', '5', '6'])},
        "col3": {"name": "Талант", "score": get_l(['7', '8', '9'])},
        "diag1": {"name": "Духовность", "score": get_l(['1', '5', '9'])},
        "diag2": {"name": "Темперамент", "score": get_l(['3', '5', '7'])}
    }
    for k in matrix_lines:
        sc = matrix_lines[k]['score']
        matrix_lines[k]['status'] = "Мощная" if sc > 5 else "Средняя" if sc >= 3 else "Слабая"
        matrix_lines[k]['theory'] = LINES_INFO[k]['text'] if k in LINES_INFO else ""

    return matrix, skills, all_digits, matrix_lines


# --- API ---
@app.route('/api/v1/coach/<arch_num>/<day_type>')
def api_get_coach(arch_num, day_type):
    arch = ArchetypeContent.query.filter_by(number=str(arch_num)).first()
    if not arch: return jsonify({"error": "Arch not found"}), 404
    tip = DailyCoachTip.query.filter_by(archetype_id=arch.id, day_type=day_type).first()
    if not tip: return jsonify({"error": "Tip not found"}), 404
    return jsonify({"body": tip.phys_content, "mind": tip.ment_content, "spirit": tip.harm_content})


@app.route('/api/v1/skills/<int:user_id>')
def api_get_skills(user_id):
    u = UserRecord.query.get(user_id)
    if not u: return jsonify({"error": "User not found"}), 404
    return jsonify({
        "labels": ["Лидерство", "Коммуникация", "Эмпатия", "Логика", "Agile"],
        "data": [u.s_leadership, u.s_comm, u.s_empathy, u.s_logic, u.s_agile],
        "user_name": u.name
    })


# --- РОУТЫ АДМИНКИ ---

@app.route('/admin-auth', methods=['POST'])
def admin_auth():
    if request.json.get('password') == '0602':
        session['admin_logged_in'] = True
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 401


@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return "Доступ запрещен. Зайдите через главную (пароль 0602)", 403
    archetypes = ArchetypeContent.query.order_by(ArchetypeContent.number.cast(db.Integer)).all()
    records = UserRecord.query.order_by(UserRecord.created_at.desc()).all()
    articles = Article.query.all()
    stats = {}
    for r in records:
        stats[r.archetype] = stats.get(r.archetype, 0) + 1
    return render_template('admin.html', archetypes=archetypes, records=records, stats=stats, articles=articles)


@app.route('/admin/get/<num>')
def admin_get(num):
    content = ArchetypeContent.query.filter_by(number=str(num)).first()
    if content:
        fields = ['title', 'planet', 'element', 'action_power', 'shadow_side',
                  'growth_point', 'realization', 'karmic_tasks', 'development_cycle',
                  'mind_power', 'life_result', 'partner_type', 'financial_tip',
                  'health_tips', 'exit_minus', 'search_queries']
        data = {f: getattr(content, f) for f in fields}
        return jsonify({'status': 'success', 'data': data})
    return jsonify({'status': 'error', 'message': 'Not found'})


@app.route('/admin/update', methods=['POST'])
def admin_update():
    #if not session.get('admin_logged_in'): return jsonify({'status': 'error'}), 403 временная заглушка для наполнения базы
    data = request.json
    num = data.get('number')
    content = ArchetypeContent.query.filter_by(number=str(num)).first()
    if not content:
        content = ArchetypeContent(number=str(num))
        db.session.add(content)

    for key, value in data.items():
        if hasattr(content, key) and key not in ['id', 'number']:
            setattr(content, key, value)

    try:
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {e}")  # Видеть ошибку в консоли полезно
        return jsonify({'status': 'error', 'message': str(e)}), 500  #поправление додавления


@app.route('/admin/articles/add', methods=['POST'])
def admin_add_article():
    if not session.get('admin_logged_in'): return jsonify({'status': 'error'}), 403
    data = request.json
    try:
        new_art = Article(title=data.get('title'), category=data.get('category'), content=data.get('content'))
        db.session.add(new_art)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


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
    trends = Article.query.filter_by(category='Trends').limit(3).all()
    result = None
    matrix_desc = {}
    matrix_lines = {}
    jobs = []
    user_id = None
    synastry_result = None
    user_skills = {"labels": ["Лидерство", "Коммуникация", "Эмпатия", "Логика", "Agile"], "data": [0, 0, 0, 0, 0]}
    energy_data = [0, 0, 0, 0, 0, 0, 0]

    if request.method == 'POST':
        user_name = request.form.get('user_name', 'Искатель')
        email = request.form.get('user_email')
        day = request.form.get('day', '').strip()
        month = request.form.get('month', '').strip()
        year = request.form.get('year', '').strip()
        country = request.form.get('country', 'ua')
        p_day = request.form.get('partner_day', '').strip()

        if day and month and year:
            # 1. Расчет Архетипа
            group_num = str(sum_digits(day))
            result = ArchetypeContent.query.filter_by(number=group_num).first()

            # 2. Психоматрица
            matrix_dict, user_skills_calc, all_digits, m_lines = calculate_full_matrix_logic(day, month, year)
            user_skills = user_skills_calc
            matrix_lines = m_lines

            for n_id, info in NODES_INFO.items():
                cnt = all_digits.count(n_id)
                lvl = "low" if cnt == 0 else "mid" if cnt <= 2 else "high"
                matrix_desc[n_id] = {"name": info["name"], "text": info[lvl], "count": cnt, "visual": matrix_dict[n_id]}

            # 3. График Энергии
            try:
                calc_val = int(day) * int(month) * int(year)
                s_val = str(calc_val).ljust(7, '0')[:7]
                energy_data = [int(d) for d in s_val]
            except Exception as e:
                print(f"Ошибка энергии: {e}")

            # 4. Синастрия
            if p_day:
                try:
                    p_group = sum_digits(p_day)
                    union_num = sum_digits(int(group_num) + int(p_group))
                    synastry_result = {
                        "union_number": union_num,
                        "partner_archetype": p_group,
                        "description": SYNASTRY_TEXTS.get(union_num, "Сложный союз.")
                    }
                except:
                    pass

            # 5. Карьера
            if result and CareerService:
                try:
                    prof_entry = ProfessionContent.query.filter_by(number=str(result.number)).first()
                    kw = result.search_queries or (prof_entry.list_csv if prof_entry else None)
                    jobs = CareerService.get_vacancies(result.number, country=country, custom_keywords=kw)
                except Exception as e:
                    print(f"Ошибка CareerService: {e}")
                    jobs = []

            # 6. Сохранение в БД Neon
            try:
                new_rec = UserRecord(
                    name=user_name, email=email, archetype=group_num,
                    s_leadership=user_skills['data'][0],
                    s_comm=user_skills['data'][1],
                    s_empathy=user_skills['data'][4]
                )
                db.session.add(new_rec)
                db.session.commit()
                user_id = new_rec.id
            except Exception as e:
                db.session.rollback()
                print(f"⚠️ Ошибка БД: {e}")

    return render_template('index.html',
                           result=result,
                           matrix_desc=matrix_desc,
                           user_skills=user_skills,
                           energy_data=energy_data,
                           matrix_lines=matrix_lines,
                           jobs=jobs,
                           trends=trends,
                           user_id=user_id,
                           synastry_result=synastry_result
                           )


# --- ЭКСПОРТ PDF ---
@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    if not WEASYPRINT_AVAILABLE:
        return "PDF недоступен локально (WeasyPrint не найден).", 503

    try:
        user_name = request.form.get('user_name', 'Искатель')
        day, month, year = request.form.get('day', '').strip(), request.form.get('month', '').strip(), request.form.get(
            'year', '').strip()

        if not (day and month and year): return "Ошибка данных", 400

        group_num = str(sum_digits(day))
        result = ArchetypeContent.query.filter_by(number=group_num).first()
        matrix_dict, skills_info, all_digits, m_lines = calculate_full_matrix_logic(day, month, year)

        calc_val = int(day) * int(month) * int(year)
        energy_data = [int(d) for d in str(calc_val).ljust(7, '0')[:7]]

        rendered_html = render_template('pdf_template.html', result=result, matrix=matrix_dict, user_skills=skills_info,
                                        energy_data=energy_data, user_name=user_name, day=day, month=month, year=year)
        pdf = HTML(string=rendered_html).write_pdf()

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="Genesis_{user_name}.pdf"'
        return response
    except Exception as e:
        return f"Ошибка: {str(e)}", 500


@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        recipient = request.form.get('email')
        msg = Message("Ваш профиль | Genesis", sender=app.config['MAIL_USERNAME'], recipients=[recipient])
        msg.html = f"<html><body style='background:#050505; color:#b8b8b8; padding:20px;'>{request.form.get('html_content')}</body></html>"
        mail.send(msg)
        return "OK", 200
    except Exception as e:
        return str(e), 500


# --- ЗАПУСК ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Авто-заполнение базы при первом запуске
        if not ArchetypeContent.query.first():
            for i in range(1, 10):
                db.session.add(ArchetypeContent(number=str(i), title=f"Архетип {i}"))
            db.session.commit()
    app.run(debug=True)
