import os
import re
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from services import CareerService
import pdfkit
from leela_module.leela_logic import leela_bp # импорт лилы

app = Flask(__name__)

app.register_blueprint(leela_bp, url_prefix='/leela')

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
    dharma = db.Column(db.Text)
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
def sum_digits(n):
    """Редукция любого числа до однозначного (1-9)"""
    if not n or str(n) == '0': return 0
    s = sum(int(d) for d in str(n) if d.isdigit())
    while s > 9:
        s = sum(int(d) for d in str(s))
    return s

def get_group(d):
    """Определяет базовый архетип дня (1-9)"""
    return str(sum_digits(d))


# --- РОУТЫ ---

@app.route('/admin/get_profs/<num>')
def admin_get_profs(num):
    """Получение списка профессий для админки"""
    prof = ProfessionContent.query.filter_by(number=str(num)).first()
    if prof:
        return jsonify({'status': 'success', 'list_csv': prof.list_csv})
    return jsonify({'status': 'success', 'list_csv': ''})


@app.route('/admin/update_profs', methods=['POST'])
def admin_update_profs():
    """Сохранение списка профессий из админки"""
    data = request.json
    num = data.get('number')
    list_csv = data.get('list_csv', '')

    if not num:
        return jsonify({'status': 'error', 'message': 'No number'})

    prof = ProfessionContent.query.filter_by(number=str(num)).first()
    if not prof:
        prof = ProfessionContent(number=str(num))
        db.session.add(prof)

    prof.list_csv = list_csv
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    dharma_data = None
    matrix_raw = None
    compatibility_result = None
    jobs = []

    if request.method == 'POST':
        # Данные пользователя
        day = request.form.get('day', '').strip()
        month = request.form.get('month', '').strip()
        year = request.form.get('year', '').strip()

        # Данные партнера
        p_day = request.form.get('p_day', '').strip()
        p_month = request.form.get('p_month', '').strip()

        country = request.form.get('country', 'ua')

        if day and month:
            # 1. Основной Архетип дня
            group_num = get_group(day)
            result = ArchetypeContent.query.filter_by(number=str(group_num)).first()

            # 2. Дхарма (День + Месяц)
            try:
                d_num = sum_digits(int(day) + int(month))
                dharma_data = ArchetypeContent.query.filter_by(number=str(d_num)).first()
            except:
                dharma_data = None
                #"расчет Дхармы для Согласно логике твоей функции sum_digits(int(day) + int(month)):День: "
                 #"17Месяц: 07Сумма: $17 + 7 = 24$Редукция (сведение к цифре): $2 + 4 = \mathbf{6}$"

            # 3. Матрица для "человечка"
            full_date_str = f"{day}{month}{year}"
            matrix_raw = {f"c{i + 1}": full_date_str[i] if i < len(full_date_str) else "0" for i in range(7)}

            # 4. Расчет совместимости (только если партнер введен)
            if p_day and p_month:
                try:
                    user_arch = sum_digits(day)
                    partner_arch = sum_digits(p_day)
                    pair_num = sum_digits(user_arch + partner_arch)
                    compatibility_result = ArchetypeContent.query.filter_by(number=str(pair_num)).first()
                except Exception as e:
                    print(f"Compatibility Error: {e}")

            # 5. ВАКАНСИИ (ТЕПЕРЬ НА ПРАВИЛЬНОМ УРОВНЕ)
            if result:
                try:
                    # Сначала сами берем слова из базы
                    prof_entry = ProfessionContent.query.filter_by(number=str(result.number)).first()
                    admin_keywords = prof_entry.list_csv if prof_entry else None

                    print(f"DEBUG: [→] Ключевые слова из базы для группы {result.number}: {admin_keywords}")

                    # Вызываем сервис
                    jobs = CareerService.get_vacancies(result, country=country, custom_keywords=admin_keywords)
                    print(f"DEBUG: [!!!] В шаблон передано вакансий: {len(jobs)}")
                except Exception as e:
                    print(f"DEBUG: [❌] Ошибка вызова сервиса: {e}")

    # Финальный возврат шаблона (на уровне метода POST)
    return render_template('index.html',
                           result=result,
                           dharma_data=dharma_data,
                           matrix_raw=matrix_raw,
                           compatibility_result=compatibility_result,
                           jobs=jobs)


@app.route('/admin/get/<num>')
def admin_get(num):
    content = ArchetypeContent.query.filter_by(number=num).first()
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
    if not num:
        return jsonify({'status': 'error', 'message': 'No number provided'})

    content = ArchetypeContent.query.filter_by(number=num).first()
    if not content:
        content = ArchetypeContent(number=num)
        db.session.add(content)

    for key, value in data.items():
        if hasattr(content, key) and key != 'id':
            if key == 'title':
                # Очистка заголовка от HTML
                clean_title = re.sub('<[^<]+?>', '', value)
                setattr(content, key, clean_title.strip())
            else:
                setattr(content, key, value)

    db.session.commit()
    return jsonify({'status': 'success'})


# Укажи путь к установленному wkhtmltopdf.exe
# ВНИМАНИЕ: Проверь этот путь на своем диске!
PATH_WKHTML = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'


@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    # Получаем скомпилированный HTML из скрытого поля формы
    html_content = request.form.get('html_to_pdf')

    if not html_content:
        return "Ошибка: данные для PDF не получены", 400

    # Настройки PDF (шрифты, отступы)
    options = {
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,  # Важно для подгрузки стилей и КЛЮЧЕВОЙ ПАРАМЕТР ДЛЯ ЛОКАЛЬНЫХ КАРТИНОК
        'disable-javascript': None,  # <--- ДОБАВЬ ЭТО: запрещаем JS внутри ПДФ, чтобы не вис
        'quiet': ''
    }

    try:
        config = pdfkit.configuration(wkhtmltopdf=PATH_WKHTML)
        # Генерируем PDF в память
        pdf = pdfkit.from_string(html_content, False, configuration=config, options=options)

        # Отправляем файл пользователю
        return (pdf, 200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename="Genesis_Chronics.pdf"'
        })
    except Exception as e:
        print(f"DEBUG: [❌] Ошибка генерации PDF: {e}")
        return f"Ошибка генерации PDF: {e}", 500



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)