import os
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF, XPos, YPos  # Добавили новые константы для позиционирования
from datetime import datetime

app = Flask(__name__)

# БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///genesis_archive.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
    library = {
        "1": {
            "title": "Архетип I: Солнечный Трон",
            "html": """
                <div class="highlight-text">«Вы — лидер, рожденный с сознанием Царя.»</div>
                <p>Ваша воля — ваш главный инструмент. Избегайте стагнации.</p>
            """,
            "plain": "Архетип 1: Рожденный на Троне. Лидерская природа, железная воля."
        }
    }
    return library.get(str(day), {"title": "В разработке", "html": "Данные готовятся...", "plain": "Нет данных"})


import random


def create_pdf(name, data_plain):
    pdf = FPDF()
    pdf.add_page()

    # Подключаем шрифт (убедись, что arial.ttf в папке)
    font_path = os.path.join(os.getcwd(), 'arial.ttf')
    if os.path.exists(font_path):
        pdf.add_font('ArialCustom', '', font_path)
        pdf.set_font('ArialCustom', '', 12)
    else:
        pdf.set_font('helvetica', '', 12)

    # --- СТИЛИЗАЦИЯ ЗАГОЛОВКА ---
    pdf.set_text_color(176, 141, 87)  # Цвет меди (наш брендовый)
    pdf.set_font('ArialCustom', '', 18)
    pdf.cell(0, 15, text="GENESIS: АНАЛИТИЧЕСКИЙ ПРОФИЛЬ", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Тонкая линия-разделитель
    pdf.set_draw_color(176, 141, 87)
    pdf.line(20, 30, 190, 30)
    pdf.ln(10)

    # --- ЛИРИЧЕСКОЕ ВСТУПЛЕНИЕ (МАСКИ) ---
    greetings = [
        f"Уважаемый {name}, мы завершили глубокий анализ вашего архетипического кода.",
        f"Для нас большая честь представить результаты исследования системы Genesis для субъекта: {name}.",
        f"Ниже представлен детальный разбор ваших фундаментальных настроек, полученный на основе даты вашего воплощения."
    ]

    intro_text = [
        "Данный отчет подготовлен ведущим аналитиком отдела психотипологии. Мы рассматриваем личность не как набор цифр, а как сложную динамическую систему потенциалов.",
        "Ваш код указывает на уникальное сочетание волевых качеств и внутренних ресурсов, которые требуют осознанного управления."
    ]

    pdf.set_text_color(60, 60, 60)  # Темно-серый для основного текста
    pdf.set_font('ArialCustom', '', 11)
    pdf.multi_cell(0, 8, text=random.choice(greetings))
    pdf.ln(5)
    pdf.set_font('ArialCustom', '', 10)
    pdf.multi_cell(0, 7, text=random.choice(intro_text))
    pdf.ln(10)

    # --- ОСНОВНОЙ БЛОК АНАЛИЗА ---
    pdf.set_fill_color(245, 245, 245)  # Светло-серый фон для блока данных
    pdf.set_font('ArialCustom', '', 12)
    pdf.set_text_color(176, 141, 87)
    pdf.cell(0, 10, text="КЛЮЧЕВЫЕ ХАРАКТЕРИСТИКИ АРХЕТИПА", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    pdf.set_text_color(40, 40, 40)
    pdf.set_font('ArialCustom', '', 11)
    # Сюда вставляем основной текст анализа
    pdf.multi_cell(0, 9, text=data_plain)
    pdf.ln(15)

    # --- ЗАКЛЮЧЕНИЕ ПСИХОЛОГА ---
    pdf.set_draw_color(200, 200, 200)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(10)

    recommendations = [
        "Рекомендация: Интегрируйте полученные знания в повседневную практику. Помните, что осознание — это 50% трансформации.",
        "Совет эксперта: Ваша энергия требует дисциплины. Направьте вектор внимания на созидательные задачи.",
        "Заключение: Вы обладаете достаточным ресурсом для преодоления текущих вызовов. Опирайтесь на свою внутреннюю опору."
    ]

    pdf.set_font('ArialCustom', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 7, text=random.choice(recommendations))

    # Футер (подпись)
    pdf.set_y(-30)
    pdf.set_font('ArialCustom', '', 8)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 10, text="Genesis System | Отдел системного анализа | 2026", align='C')

    filename = f"Analysis_{name}.pdf"
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
            result_text=data['plain']
        )
        db.session.add(new_record)
        db.session.commit()

        # Генерация PDF
        pdf_file = create_pdf(name, data['plain'])
        result = data

    return render_template('index.html', result=result, pdf_file=pdf_file)


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)