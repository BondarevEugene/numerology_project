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

    # Шрифты
    font_path = os.path.join(os.getcwd(), 'arial.ttf')
    font_bold_path = os.path.join(os.getcwd(), 'arialbd.ttf')

    if os.path.exists(font_path):
        pdf.add_font('ArialCustom', '', font_path)
        if os.path.exists(font_bold_path):
            pdf.add_font('ArialCustom', 'B', font_bold_path)
        pdf.set_font('ArialCustom', '', 12)
    else:
        pdf.set_font('helvetica', '', 12)

    # Шапка
    pdf.set_text_color(176, 141, 87)
    pdf.set_font('ArialCustom', 'B' if os.path.exists(font_bold_path) else '', 16)
    pdf.cell(0, 15, text="GENESIS: ПЕРСОНАЛЬНЫЙ ШИФР", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(176, 141, 87)
    pdf.line(20, 30, 190, 30)
    pdf.ln(10)

    # Приветствие
    pdf.set_text_color(60, 60, 60)
    pdf.set_font('ArialCustom', '', 10)
    pdf.multi_cell(0, 6, text=random.choice(GREETINGS).format(name=name))
    pdf.ln(5)

    # Парсинг контента
    raw_text = data['full_text']
    lines = raw_text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(2)
            continue

        # Заголовки разделов
        if line.startswith('###'):
            pdf.ln(3)
            pdf.set_font('ArialCustom', 'B' if os.path.exists(font_bold_path) else '', 11)
            pdf.set_text_color(176, 141, 87)
            pdf.multi_cell(0, 8, text=line.replace('###', '').strip().upper())
            pdf.ln(1)

        # Эзотерические списки (наши новые значки)
        elif any(mark in line for mark in ['◈', '☯', '⚜']):
            pdf.set_font('ArialCustom', '', 10)
            pdf.set_text_color(40, 40, 40)
            pdf.set_x(25)  # Отступ для красоты
            # Убираем жирность Markdown (**), так как FPDF её не понимает внутри строки
            clean_line = line.replace('**', '')
            pdf.multi_cell(0, 7, text=clean_line)

        # Обычный текст
        else:
            pdf.set_font('ArialCustom', '', 10)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 7, text=line.replace('**', ''))

    # Подпись
    pdf.set_y(-20)
    pdf.set_font('ArialCustom', '', 8)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 10, text=f"Система Genesis | Анализ для {name} | 2026", align='C')

    filename = f"Genesis_Analysis_{data_key}.pdf"
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