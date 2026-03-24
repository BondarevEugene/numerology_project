import os
import csv
import io
import re
import pdfkit
from datetime import datetime
from flask import Flask, render_template, request, send_file, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup
from sqlalchemy import func

# 1. НАСТРОЙКА ПРИЛОЖЕНИЯ
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Лимит 16 Мегабайт
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'genesis_archive.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# НАСТРОЙКА PDF (Укажи свой путь к wkhtmltopdf.exe)
PDF_CONFIG = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')


# 2. МОДЕЛИ ДАННЫХ
class ArchetypeContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), unique=True, nullable=False)
    title = db.Column(db.String(200))
    full_text = db.Column(db.Text)  # Здесь теперь хранится чистый HTML из редактора # В SQLite этого обычно достаточно для картинки


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


# 3. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def calculate_digit(n):
    try:
        s = sum(int(d) for d in str(n) if d.isdigit())
        return s if s <= 9 else calculate_digit(s)
    except:
        return 1


def get_interpretation(day):
    base_digit = str(calculate_digit(day))
    record = ArchetypeContent.query.filter_by(number=base_digit).first()
    return record if record else None


def create_rich_pdf(name, html_content, professions_list, compatibility=""):
    # Стилизация PDF (премиальный темный дизайн)
    styled_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap');
            body {{ background-color: #060709; color: #d1d1d1; font-family: 'Segoe UI', Arial, sans-serif; padding: 40px; }}
            .header {{ text-align: center; border-bottom: 2px solid #b08d57; padding-bottom: 20px; margin-bottom: 30px; }}
            .header h1 {{ font-family: 'Cinzel', serif; color: #b08d57; letter-spacing: 5px; margin: 0; font-size: 32px; }}
            .subject-info {{ color: #d4af37; font-size: 18px; margin-bottom: 20px; text-transform: uppercase; }}
            .main-content {{ line-height: 1.8; font-size: 15px; }}
            .main-content img {{ max-width: 100%; border: 1px solid #b08d57; margin: 20px 0; border-radius: 5px; }}
            .prof-box {{ background: rgba(176, 141, 87, 0.1); border: 1px solid #b08d57; padding: 20px; margin-top: 30px; }}
            .compatibility {{ color: #d4af37; font-weight: bold; border: 1px left solid #d4af37; padding-left: 15px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 50px; color: #444; font-size: 10px; letter-spacing: 2px; }}
            h1, h2, h3 {{ color: #d4af37; font-family: 'Cinzel', serif; }}
        </style>
    </head>
    <body>
        <div class="header"><h1>GENESIS ARCHIVE</h1></div>
        <div class="subject-info">Subject: {name}</div>

        {f'<div class="compatibility">{compatibility}</div>' if compatibility else ''}

        <div class="main-content">{html_content}</div>

        <div class="prof-box">
            <h3 style="margin-top:0">СФЕРЫ РЕАЛИЗАЦИИ</h3>
            <p>{", ".join(professions_list)}</p>
        </div>

        <div class="footer">GENESIS PROTOCOL © 2026 | SECURED REPORT</div>
    </body>
    </html>
    """

    filename = f"Genesis_Report_{name.replace(' ', '_')}.pdf"
    options = {
        'encoding': "UTF-8",
        'enable-local-file-access': None,
        'quiet': '',
        'page-size': 'A4',
        'margin-top': '0in', 'margin-right': '0in', 'margin-bottom': '0in', 'margin-left': '0in'
    }

    pdfkit.from_string(styled_html, filename, configuration=PDF_CONFIG, options=options)
    return filename


# 4. МАРШРУТЫ
@app.route('/', methods=['GET', 'POST'])
def index():
    result, pdf_file = None, None
    now = datetime.now()
    daily_code = str(calculate_digit(now.day + now.month + now.year))
    daily_data = get_interpretation(daily_code)
    daily_forecast = {"code": daily_code, "title": daily_data.title if daily_data else "Vibration"}

    if request.method == 'POST':
        name, email, day = request.form.get('name'), request.form.get('email'), request.form.get('day')
        partner_day = request.form.get('partner_day')

        base_key = str(calculate_digit(day))
        record = get_interpretation(day)

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

        # Генерация "сложного" PDF
        pdf_file = create_rich_pdf(name, record.full_text, profs, compatibility_msg)
        result = {"title": record.title, "full_text": Markup(record.full_text)}
        if compatibility_msg: result['compatibility'] = compatibility_msg

    return render_template('index.html', result=result, pdf_file=pdf_file, daily_forecast=daily_forecast)


@app.route('/genesis-admin')
def admin_dashboard():
    records = AnalysisRecord.query.order_by(AnalysisRecord.created_at.desc()).limit(20).all()
    archetypes = ArchetypeContent.query.order_by(ArchetypeContent.number.cast(db.Integer)).all()
    profs = ProfessionContent.query.order_by(ProfessionContent.number.cast(db.Integer)).all()
    stats_raw = db.session.query(AnalysisRecord.archetype, func.count(AnalysisRecord.archetype)).group_by(
        AnalysisRecord.archetype).all()
    stats = {str(k): v for k, v in stats_raw}
    return render_template('admin.html', records=records, archetypes=archetypes, profs=profs, stats=stats)


@app.route('/admin/export-csv')
def export_csv():
    records = AnalysisRecord.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Email', 'Day', 'Archetype', 'Date'])
    for r in records: writer.writerow([r.id, r.name, r.email, r.birth_date, r.archetype, r.created_at])
    return Response(output.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=genesis_data.csv"})


@app.route('/admin/edit/<type>/<int:id>', methods=['POST'])
def quick_edit(type, id):
    if type == 'arch':
        # Используем современный Session.get()
        item = db.session.get(ArchetypeContent, id)
        if item:
            item.title = request.form.get('title')
            item.full_text = request.form.get('full_text_html')  # Важно: берем HTML
    else:
        item = db.session.get(ProfessionContent, id)
        if item:
            item.list_csv = request.form.get('list_csv')

    db.session.commit()
    return "OK", 200


@app.route('/admin/delete-record/<int:id>', methods=['POST'])
def delete_record(id):
    db.session.delete(AnalysisRecord.query.get_or_404(id));
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)