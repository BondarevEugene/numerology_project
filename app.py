import os
import random
import re
from datetime import datetime
from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF
from markupsafe import Markup
from sqlalchemy import func

# 1. НАСТРОЙКА ПРИЛОЖЕНИЯ
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'genesis_archive.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 2. МОДЕЛИ ДАННЫХ (БАЗА)
class ArchetypeContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), unique=True, nullable=False)
    title = db.Column(db.String(200))
    full_text = db.Column(db.Text)


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


# 3. КОНСТАНТЫ (На случай, если база пуста)
PROFESSIONS_DEFAULT = {
    "1": ["Топ-менеджмент", "Госслужба", "Собственный бизнес", "Политика"],
    "2": ["Дипломатия", "Психология", "Аналитика", "Работа в партнерстве"],
    "3": ["Образование", "Финансы", "Юриспруденция", "Стратегическое планирование"],
    "4": ["IT-разработка", "Креатив", "Инженерия", "Инновационные стартапы"],
    "5": ["Торговля", "Маркетинг", "PR и коммуникации", "Международный бизнес"],
    "6": ["Дизайн", "Индустрия красоты", "Наставничество", "Инвестиции"],
    "7": ["Йога и спорт", "Криптовалюты", "Исследования", "Антикризис-менеджмент"],
    "8": ["Управление активами", "Недвижимость", "Производство", "Банковское дело"],
    "9": ["Медицина", "Военное дело", "Социальные проекты", "Спорт высоких достижений"]
}


# 4. СИНХРОНИЗАЦИЯ КОНТЕНТА
def sync_content_to_db():
    from content import ARCHETYPES  # Импортируем внутри, чтобы избежать циклов

    # Заполняем архетипы
    if not ArchetypeContent.query.first():
        for num, data in ARCHETYPES.items():
            db.session.add(ArchetypeContent(number=str(num), title=data['title'], full_text=data['full_text']))

    # Заполняем профессии
    if not ProfessionContent.query.first():
        for num, profs in PROFESSIONS_DEFAULT.items():
            db.session.add(ProfessionContent(number=str(num), list_csv=", ".join(profs)))

    db.session.commit()


# Инициализация БД
with app.app_context():
    db.create_all()
    sync_content_to_db()


# 5. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def get_interpretation(day):
    day_str = str(day)
    record = ArchetypeContent.query.filter_by(number=day_str).first()
    if not record:
        base_digit = sum(int(d) for d in day_str)
        if base_digit > 9: base_digit = sum(int(d) for d in str(base_digit))
        record = ArchetypeContent.query.filter_by(number=str(base_digit)).first()

    if record:
        return {"title": record.title, "full_text": record.full_text}
    return {"title": "Error", "full_text": "Content not found"}


def create_pdf(name, data_key, professions_list, compatibility_msg=None):
    try:
        data = get_interpretation(data_key)
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, 'arial.ttf')

        try:
            pdf.add_font('GenesisFont', '', font_path)
            font_main = 'GenesisFont'
        except:
            font_main = 'Helvetica'

        pdf.set_font(font_main, size=12)
        pdf.set_fill_color(6, 7, 9)
        pdf.rect(0, 0, 210, 297, 'F')

        pdf.set_text_color(176, 141, 87)
        pdf.set_font(font_main, size=18)
        pdf.cell(0, 20, text="GENESIS SYSTEM: SACRED ARCHIVE", align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)

        raw_text = data.get('full_text', '')
        clean_text = raw_text.replace('**', '').replace('###', '').replace('✥', '').replace('◈', '-').replace('☯',
                                                                                                              '(*)').replace(
            '⚜', '>')

        pdf.set_text_color(210, 210, 210)
        pdf.set_font(font_main, size=11)
        pdf.multi_cell(0, 8, text=clean_text, align='L')
        pdf.ln(10)

        if compatibility_msg:
            pdf.set_draw_color(212, 175, 55)
            pdf.set_fill_color(15, 18, 24)
            pdf.set_text_color(212, 175, 55)
            pdf.set_font(font_main, size=12)
            pdf.cell(0, 12, text=f" {compatibility_msg}", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(10)

        pdf.set_text_color(176, 141, 87)
        pdf.set_font(font_main, size=13)
        pdf.cell(0, 10, text="СФЕРЫ РЕАЛИЗАЦИИ:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(font_main, size=11)
        pdf.multi_cell(0, 8, text=", ".join(professions_list))

        pdf.set_y(-20)
        pdf.set_font(font_main, size=9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 10, text=f"Genesis Protocol 2026 | Subject: {name}", align='C')

        filename = f"Genesis_Report_{name.replace(' ', '_')}.pdf"
        pdf.output(filename)
        return filename
    except Exception as e:
        print(f"PDF Error: {e}")
        return None


# 6. ФИЛЬТРЫ И МАРШРУТЫ
@app.template_filter('genesis_style')
def genesis_style_filter(text):
    if not text: return ""
    lines = [line.strip() for line in text.split('\n')]
    formatted_html = []
    for line in lines:
        if not line: continue
        if line.startswith('###'):
            title = line.replace('###', '').replace('✥', '').strip()
            formatted_html.append(f'<div class="mystic-header"><span>{title}</span></div>')
        elif any(mark in line for mark in ['◈', '☯', '⚜', '✥']):
            line_content = re.sub(r'\*\*(.*?)\*\*', r'<b class="gold-accent">\1</b>', line)
            icon = line_content[0]
            content = line_content[1:].strip()
            formatted_html.append(
                f'<div class="task-row"><span class="icon">{icon}</span><span class="text">{content}</span></div>')
        else:
            line = re.sub(r'\*\*(.*?)\*\*', r'<b class="gold-accent">\1</b>', line)
            formatted_html.append(f'<p class="paragrapth">{line}</p>')
    return Markup('\n'.join(formatted_html))


@app.route('/', methods=['GET', 'POST'])
def admin_dashboard():
    # 1. Последние 20 записей
    records = AnalysisRecord.query.order_by(AnalysisRecord.created_at.desc()).limit(20).all()

    # 2. Архетипы и Профессии из базы
    archetypes = ArchetypeContent.query.order_by(ArchetypeContent.number.cast(db.Integer)).all()
    profs = ProfessionContent.query.order_by(ProfessionContent.number.cast(db.Integer)).all()

    # 3. СТАТИСТИКА: Считаем сколько раз встречается каждый архетип
    # Результат будет в виде списка кортежей: [('1', 5), ('3', 12), ...]
    stats_raw = db.session.query(
        AnalysisRecord.archetype,
        func.count(AnalysisRecord.archetype)
    ).group_by(AnalysisRecord.archetype).all()

    stats = {str(k): v for k, v in stats_raw}  # Превращаем в удобный словарь для HTML

    return render_template('admin.html',
                           records=records,
                           archetypes=archetypes,
                           profs=profs,
                           stats=stats)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        result, pdf_file = None, None

        # ЛОГИКА ПРОГНОЗА ДНЯ (берем текущую дату)
        now = datetime.now()
        day_sum = sum(int(d) for d in str(now.day))
        month_sum = sum(int(d) for d in str(now.month))
        year_sum = sum(int(d) for d in str(now.year))
        daily_code = str(day_sum + month_sum + year_sum)
        if int(daily_code) > 9: daily_code = str(sum(int(d) for d in daily_code))

        daily_data = get_interpretation(daily_code)
        daily_forecast = {"code": daily_code, "title": daily_data['title']}

        if request.method == 'POST':
            # ... твой существующий код обработки формы (name, email, и т.д.) ...
            # (Оставь его без изменений, просто добавь daily_forecast в return ниже)
            pass

        return render_template('index.html', result=result, pdf_file=pdf_file, daily_forecast=daily_forecast)

    # --- ОБНОВЛЕННАЯ АДМИНКА ---
    @app.route('/genesis-admin')
    def admin_dashboard():
        records = AnalysisRecord.query.order_by(AnalysisRecord.created_at.desc()).limit(20).all()
        archetypes = ArchetypeContent.query.order_by(ArchetypeContent.number.cast(db.Integer)).all()
        profs = ProfessionContent.query.order_by(ProfessionContent.number.cast(db.Integer)).all()

        # Сбор статистики для графиков
        stats_raw = db.session.query(AnalysisRecord.archetype, func.count(AnalysisRecord.archetype)).group_by(
            AnalysisRecord.archetype).all()
        stats = {str(k): v for k, v in stats_raw}

        return render_template('admin.html', records=records, archetypes=archetypes, profs=profs, stats=stats)

def index():
    result, pdf_file = None, None
    if request.method == 'POST':
        name, email, day = request.form.get('name'), request.form.get('email'), request.form.get('day')
        partner_day = request.form.get('partner_day')

        data = get_interpretation(day)

        def calculate_digit(n):
            s = sum(int(d) for d in str(n))
            return s if s <= 9 else calculate_digit(s)

        base_key = str(calculate_digit(day))

        # Берем профессии из базы
        prof_record = ProfessionContent.query.filter_by(number=base_key).first()
        profs = prof_record.list_csv.split(", ") if prof_record else ["Универсальный путь"]

        compatibility_msg = ""
        if partner_day:
            pair_score = calculate_digit(int(day) + int(partner_day))
            meanings = {1: "Лидерство", 2: "Гармония", 3: "Творчество", 4: "Стабильность", 5: "Страсть", 6: "Уют",
                        7: "Духовность", 8: "Бизнес", 9: "Служение"}
            compatibility_msg = f"СОВМЕСТИМОСТЬ: Код {pair_score} — {meanings.get(pair_score, 'Союз')}"

        db.session.add(
            AnalysisRecord(name=name, email=email, birth_date=day, archetype=base_key, professions=", ".join(profs)))
        db.session.commit()

        pdf_file = create_pdf(name, day, profs, compatibility_msg)
        result = data
        if compatibility_msg: result['compatibility'] = compatibility_msg

    return render_template('index.html', result=result, pdf_file=pdf_file)


# 7. АДМИН-ПАНЕЛЬ
@app.route('/genesis-admin')
def admin_dashboard():
    records = AnalysisRecord.query.order_by(AnalysisRecord.created_at.desc()).limit(20).all()
    archetypes = ArchetypeContent.query.order_by(ArchetypeContent.number.cast(db.Integer)).all()
    profs = ProfessionContent.query.order_by(ProfessionContent.number.cast(db.Integer)).all()
    return render_template('admin.html', records=records, archetypes=archetypes, profs=profs)


@app.route('/admin/edit/<type>/<int:id>', methods=['POST'])
def quick_edit(type, id):
    if type == 'arch':
        item = ArchetypeContent.query.get(id)
        item.title = request.form.get('title')
        item.full_text = request.form.get('full_text')
    elif type == 'prof':
        item = ProfessionContent.query.get(id)
        item.list_csv = request.form.get('list_csv')
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete-record/<int:id>', methods=['POST'])
def delete_record(id):
    record = AnalysisRecord.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
