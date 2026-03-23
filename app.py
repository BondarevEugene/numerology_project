import os
import random
import re
from datetime import datetime
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF
from markupsafe import Markup

# ИМПОРТ НАШИХ ТЕКСТОВ
from content import ARCHETYPES, GREETINGS, INTRO_TEXTS, RECOMMENDATIONS

app = Flask(__name__)

# Настройка БД
# Настройка путей
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'genesis_archive.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ПРИНУДИТЕЛЬНОЕ СОЗДАНИЕ ПРИ ЗАПУСКЕ
with app.app_context():
    try:
        db.create_all()
        print(f"--- DATABASE INITIALIZED AT: {db_path} ---")
    except Exception as e:
        print(f"--- DATABASE ERROR: {e} ---")

PROFESSIONS = {
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


@app.route('/compatibility', methods=['GET', 'POST'])
def compatibility():
    comp_result = None
    if request.method == 'POST':
        d1 = request.form.get('day1')
        d2 = request.form.get('day2')

        # Логика: сумма арканов
        def get_digit(n):
            s = sum(int(d) for d in str(n))
            return s if s <= 9 else get_digit(s)

        score = get_digit(get_digit(d1) + get_digit(d2))

        # Краткие трактовки
        meanings = {
            "1": "Лидерство и соревнование. Учитесь уступать.",
            "2": "Идеальный союз, глубокое понимание.",
            "3": "Творчество и развитие. Сильное потомство.",
            "4": "Стабильность и порядок. Крепкий фундамент.",
            "5": "Страсть и перемены. Не соскучитесь.",
            "6": "Любовь и гармония. Самый теплый союз.",
            "7": "Интеллектуальная связь. Общие тайны.",
            "8": "Материальный успех. Работа на общий результат.",
            "9": "Духовный путь. Служение общим идеалам."
        }
        comp_result = {"score": score, "text": meanings.get(str(score))}

    return render_template('compatibility.html', result=comp_result)

# Обновленная модель БД
class AnalysisRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    birth_date = db.Column(db.String(20))
    archetype = db.Column(db.String(10))
    professions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


def get_interpretation(day):
    day_str = str(day)
    # Пытаемся найти прямое вхождение (для 10, 15, 28 и т.д. из sync_archetypes)
    data = ARCHETYPES.get(day_str)

    # Если не нашли, схлопываем до базового числа (например, 12 -> 3)
    if not data:
        base_digit = sum(int(d) for d in day_str)
        if base_digit > 9: base_digit = sum(int(d) for d in str(base_digit))
        data = ARCHETYPES.get(str(base_digit))

    if not data:
        return {
            "title": "Архетип в процессе калибровки",
            "full_text": "Данные этого кода временно недоступны."
        }
    return data


# Добавляем 4-й аргумент compatibility_msg
def create_pdf(name, data_key, professions_list, compatibility_msg=None): #(v2.7.x style)
    try:
        data = get_interpretation(data_key)
        # Используем современный конструктор
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, 'arial.ttf')

        # РЕГИСТРАЦИЯ ШРИФТА (Безопасная)
        try:
            pdf.add_font('GenesisFont', '', font_path)
            font_main = 'GenesisFont'
        except:
            print("!!! ШРИФТ НЕ НАЙДЕН ИЛИ ПОВРЕЖДЕН, ИСПОЛЬЗУЮ СТАНДАРТНЫЙ !!!")
            font_main = 'Helvetica'  # Но кириллица тут может не сработать

        pdf.set_font(font_main, size=12)

        # ТЕМНЫЙ ФОН
        pdf.set_fill_color(6, 7, 9)
        pdf.rect(0, 0, 210, 297, 'F')

        # ШАПКА (Медь)
        pdf.set_text_color(176, 141, 87)
        pdf.set_font(font_main, size=18)
        pdf.cell(0, 20, text="GENESIS SYSTEM: SACRED ARCHIVE", align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)

        # ОЧИСТКА ТЕКСТА (Убираем ВСЁ лишнее)
        raw_text = data.get('full_text', '')
        clean_text = raw_text.replace('**', '').replace('###', '').replace('✥', '').replace('◈', '-').replace('☯',
                                                                                                              '(*)').replace(
            '⚜', '>')

        # ОСНОВНОЙ ТЕКСТ
        pdf.set_text_color(210, 210, 210)
        pdf.set_font(font_main, size=11)
        pdf.multi_cell(0, 8, text=clean_text, align='L')
        pdf.ln(10)

        # СОВМЕСТИМОСТЬ
        if compatibility_msg:
            pdf.set_draw_color(212, 175, 55)
            pdf.set_fill_color(15, 18, 24)
            pdf.set_text_color(212, 175, 55)
            pdf.set_font(font_main, size=12)
            pdf.cell(0, 12, text=f" {compatibility_msg}", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(10)

        # ПРОФЕССИИ
        pdf.set_text_color(176, 141, 87)
        pdf.set_font(font_main, size=13)
        pdf.cell(0, 10, text="СФЕРЫ РЕАЛИЗАЦИИ:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(font_main, size=11)
        pdf.multi_cell(0, 8, text=", ".join(professions_list))

        # ФУТЕР
        pdf.set_y(-20)
        pdf.set_font(font_main, size=9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 10, text=f"Genesis Protocol 2026 | Subject: {name}", align='C')

        filename = f"Genesis_Report_{name.replace(' ', '_')}.pdf"
        pdf.output(filename)
        print(f"--- PDF SUCCESS: {filename} ---")
        return filename

    except Exception as e:
        print(f"!!! КРИТИЧЕСКАЯ ОШИБКА PDF: {e} !!!")
        import traceback
        traceback.print_exc()  # Это покажет нам ТОЧНУЮ строку ошибки
        return None

@app.template_filter('genesis_style')
def genesis_style_filter(text):
    if not text: return ""
    lines = [line.strip() for line in text.split('\n')]
    formatted_html = []

    for line in lines:
        if not line: continue
        # Заголовки
        if line.startswith('###'):
            title = line.replace('###', '').replace('✥', '').strip()
            formatted_html.append(f'<div class="mystic-header"><span>{title}</span></div>')
        # Списки/Значки
        elif any(mark in line for mark in ['◈', '☯', '⚜', '✥']):
            line_content = re.sub(r'\*\*(.*?)\*\*', r'<b class="gold-accent">\1</b>', line)
            # Берем первый символ как иконку
            icon = line_content[0]
            content = line_content[1:].strip()
            formatted_html.append(
                f'<div class="task-row"><span class="icon">{icon}</span><span class="text">{content}</span></div>')
        # Обычный текст
        else:
            line = re.sub(r'\*\*(.*?)\*\*', r'<b class="gold-accent">\1</b>', line)
            formatted_html.append(f'<p class="paragrapth">{line}</p>')

    return Markup('\n'.join(formatted_html))


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    pdf_file = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        day = request.form.get('day')

        # Данные для совместимости (если заполнены)
        partner_day = request.form.get('partner_day')

        data = get_interpretation(day)

        # Расчет базового числа (архетипа)
        def calculate_digit(n):
            s = sum(int(d) for d in str(n))
            return s if s <= 9 else calculate_digit(s)

        base_key = str(calculate_digit(day))
        profs = PROFESSIONS.get(base_key, ["Универсальный путь"])

        # Если есть партнер — считаем совместимость
        compatibility_msg = ""
        if partner_day:
            pair_score = calculate_digit(int(day) + int(partner_day))
            meanings = {
                1: "Союз лидеров. Важно не бороться за власть.",
                2: "Гармония и понимание. Сильная эмоциональная связь.",
                3: "Творческий союз. Вместе вы создадите нечто великое.",
                4: "Стабильность. Крепкий дом и общие цели.",
                5: "Приключения и страсть. Скучно точно не будет.",
                6: "Любовь и уют. Идеальная семья.",
                7: "Духовный поиск. Вы понимаете друг друга без слов.",
                8: "Деловой союз. Вместе вы заработаете капитал.",
                9: "Служение миру. Глубокий кармический союз."
            }
            compatibility_msg = f"СОВМЕСТИМОСТЬ: Код {pair_score} — {meanings.get(pair_score)}"

        # Сохранение в БД
        new_record = AnalysisRecord(
            name=name, email=email, birth_date=day,
            archetype=base_key, professions=", ".join(profs)
        )
        db.session.add(new_record)
        db.session.commit()

        # Генерация PDF (передаем и совместимость тоже)
        pdf_file = create_pdf(name, day, profs, compatibility_msg)
        result = data
        if compatibility_msg:
            result['compatibility'] = compatibility_msg

    return render_template('index.html', result=result, pdf_file=pdf_file)


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


@app.route('/genesis-admin')
def admin_panel():
    # Заменяем order_range на order_by
    records = AnalysisRecord.query.order_by(AnalysisRecord.created_at.desc()).all()
    return render_template('admin.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)