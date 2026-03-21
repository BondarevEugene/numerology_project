import os
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
from datetime import datetime

app = Flask(__name__)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Модель таблицы клиентов
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    birth_date = db.Column(db.String(20))
    report_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Создание БД при запуске
with app.app_context():
    db.create_all()


# --- АЛГОРИТМ РАСЧЕТА ---
def get_interpretation(day):
    # Пример для числа 1 (сюда вы добавите остальные числа из таблицы)
    content_map = {
        "1": {
            "title": "Число ума: 1",
            "body": "Вы - прирожденный лидер... (весь ваш текст для 1)",
            "karma": "Взять под контроль своё эго. Найти себя...",
            "compatibility": "Взаимодействие с 8-кой дает максимальную реализацию."
        }
    }
    return content_map.get(str(day), None)


# --- ГЕНЕРАЦИЯ PDF ---
def generate_pdf(name, data):
    pdf = FPDF()
    pdf.add_page()
    # Подключаем шрифт для корректного отображения русского языка
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)

    pdf.cell(200, 10, txt=f"Персональный расчет для {name}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('DejaVu', '', 11)

    # Текст из алгоритма
    full_text = f"{data['title']}\n\n{data['body']}\n\nКармические задачи:\n{data['karma']}\n\nСовместимость:\n{data['compatibility']}"
    pdf.multi_cell(0, 7, txt=full_text)

    file_path = f"report_{name}.pdf"
    pdf.output(file_path)
    return file_path


# --- ГЛАВНЫЙ МАРШРУТ САЙТА ---
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    pdf_file = None

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')

        # Запуск алгоритма
        analysis = get_interpretation(day)

        if analysis:
            # Сохраняем в базу данных
            new_client = Client(
                name=name,
                email=email,
                birth_date=f"{day}.{month}.{year}",
                report_text=analysis['body']
            )
            db.session.add(new_client)
            db.session.commit()

            # Генерируем PDF
            pdf_file = generate_pdf(name, analysis)
            result = analysis

    return render_template('index.html', result=result, pdf_file=pdf_file)


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)