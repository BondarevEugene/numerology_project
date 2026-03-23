import os
import random
from datetime import datetime
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF, XPos, YPos

# ИМПОРТ НАШИХ ТЕКСТОВ
from content import ARCHETYPES, GREETINGS, INTRO_TEXTS, RECOMMENDATIONS

app = Flask(__name__)

# Настройка путей для БД (чтобы файл лежал в корне)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'genesis_archive.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Модель БД
class AnalysisRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    birth_date = db.Column(db.String(20))
    result_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


def get_interpretation(day):
    # Приводим к строке, так как ключи в словаре — строки "1", "2" и т.д.
    data = ARCHETYPES.get(str(day))

    if not data:
        return {
            "title": f"Архетип Числа {day}",
            "short_desc": "Анализ в очереди на обработку.",
            "full_text": "Детальные данные для этого числа будут доступны в ближайшем обновлении системы.",
            "html_display": "<p>Система Genesis калибрует данные для этого временного отрезка...</p>"
        }

    # Если в твоем файле нет поля html_display, создаем его на лету из текста
    if "html_display" not in data:
        data[
            "html_display"] = f"<div class='highlight-text'>{data.get('short_desc', '')}</div><p>{data['full_text'][:300].replace('\n', '<br>')}...</p>"

    return data


def create_pdf(name, data_key):
    data = get_interpretation(data_key)
    pdf = FPDF()
    pdf.add_page()

    # Инициализация шрифтов (Обычный и Жирный)
    # Убедись, что в папке есть arial.ttf и arialbd.ttf (жирный)
    font_path = os.path.join(os.getcwd(), 'arial.ttf')
    font_bold_path = os.path.join(os.getcwd(), 'arialbd.ttf')  # Желательно иметь и жирный шрифт

    if os.path.exists(font_path):
        pdf.add_font('ArialCustom', '', font_path)
        if os.path.exists(font_bold_path):
            pdf.add_font('ArialCustom', 'B', font_bold_path)
        pdf.set_font('ArialCustom', '', 12)
    else:
        pdf.set_font('helvetica', '', 12)

    # --- ЗАГОЛОВОК ДОКУМЕНТА ---
    pdf.set_text_color(176, 141, 87)  # Медь
    pdf.set_font('ArialCustom', 'B' if os.path.exists(font_bold_path) else '', 16)
    pdf.cell(0, 15, text="GENESIS: АНАЛИТИЧЕСКИЙ ПРОФИЛЬ", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(176, 141, 87)
    pdf.line(20, 30, 190, 30)
    pdf.ln(10)

    # --- ВВОДНАЯ ЧАСТЬ ---
    pdf.set_text_color(80, 80, 80)
    pdf.set_font('ArialCustom', '', 10)
    greeting = random.choice(GREETINGS).format(name=name)
    pdf.multi_cell(0, 6, text=greeting)
    pdf.ln(5)

    # --- ОБРАБОТКА ОСНОВНОГО ТЕКСТА (УМНОЕ ФОРМАТИРОВАНИЕ) ---
    raw_text = data['full_text']
    lines = raw_text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(2)
            continue

        # Обработка заголовков (###)
        if line.startswith('###'):
            clean_title = line.replace('###', '').strip().upper()
            pdf.ln(4)
            pdf.set_font('ArialCustom', 'B' if os.path.exists(font_bold_path) else '', 11)
            pdf.set_text_color(176, 141, 87)
            pdf.cell(0, 8, text=clean_title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(1)

        # Обработка списков (* или -)
        elif line.startswith('*') or line.startswith('-'):
            clean_item = line.replace('*', '').replace('**', '').strip()
            pdf.set_font('ArialCustom', '', 10)
            pdf.set_text_color(40, 40, 40)
            # Рисуем буллит (маленький квадратик или тире)
            pdf.set_x(25)
            pdf.cell(5, 7, text="-", border=0)
            pdf.multi_cell(0, 7, text=clean_item)

        # Обычный текст
        else:
            # Чистим жирный шрифт из Markdown (**текст**)
            clean_text = line.replace('**', '')
            pdf.set_font('ArialCustom', '', 10)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 7, text=clean_text)

    # --- ФУТЕР ---
    pdf.set_y(-25)
    pdf.set_font('ArialCustom', '', 8)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 10, text=f"Genesis System | Субъект: {name} | 2026", align='C')

    filename = f"Analysis_{name.replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    pdf_file = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        day = request.form.get('day')

        data = get_interpretation(day)

        # Сохранение в БД
        new_record = AnalysisRecord(
            name=name,
            email=email,
            birth_date=day,
            result_text=data['full_text']
        )
        db.session.add(new_record)
        db.session.commit()

        # Генерация PDF (передаем имя и номер дня)
        pdf_file = create_pdf(name, day)
        result = data

    return render_template('index.html', result=result, pdf_file=pdf_file)


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)