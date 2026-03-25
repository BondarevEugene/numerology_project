import os
import csv
import io
import pdfkit
from datetime import datetime
from flask import Flask, render_template, request, send_file, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from data import ARCHETYPE_EXTRAS

# 1. НАСТРОЙКА ПРИЛОЖЕНИЯ
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'genesis_v2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Настройка путей для PDF
if os.name == 'nt':  # Windows
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
else:  # Linux (Render)
    path_wkhtmltopdf = '/usr/bin/wkhtmltopdf'

try:
    PDF_CONFIG = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
except:
    PDF_CONFIG = None


# 2. МОДЕЛИ ДАННЫХ
class ArchetypeContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), unique=True, nullable=False)
    title = db.Column(db.String(200))
    full_text = db.Column(db.Text)
    # Новые социальные поля
    shadow_side = db.Column(db.Text)
    growth_point = db.Column(db.Text)
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


# 3. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def calculate_digit(n):
    try:
        s = sum(int(d) for d in str(n) if d.isdigit())
        return s if s <= 9 else calculate_digit(s)
    except:
        return 1


def create_pdf_report(name, result, professions, extras, compatibility):
    prof_list = professions.split(',') if professions else []

    # Генерируем HTML для PDF с логотипом VVV
    styled_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ background-color: #060709; color: #a0a0a0; font-family: 'Helvetica', 'Arial', sans-serif; padding: 50px; line-height: 1.5; }}

            /* ЛОГОТИП VVV */
            .logo-container {{ text-align: center; margin-bottom: 20px; }}
            .vvv-logo {{
                display: inline-block;
                font-family: 'Georgia', serif;
                font-size: 40px;
                color: #d4af37;
                letter-spacing: -12px; /* Сближаем буквы для эффекта сплетения */
                font-weight: bold;
                opacity: 0.9;
                border-bottom: 1px solid #b08d57;
                padding-bottom: 5px;
            }}

            .header {{ text-align: center; margin-bottom: 40px; }}
            .system-label {{ color: #b08d57; letter-spacing: 8px; font-size: 10px; text-transform: uppercase; margin-bottom: 10px; }}
            .title {{ color: #d4af37; font-size: 32px; letter-spacing: 4px; text-transform: uppercase; margin: 15px 0; }}

            .meta-grid {{ display: table; width: 100%; margin-bottom: 40px; border-top: 1px solid rgba(176,141,87,0.2); border-bottom: 1px solid rgba(176,141,87,0.2); padding: 15px 0; }}
            .meta-item {{ display: table-cell; text-align: center; color: #d4af37; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }}

            h3 {{ color: #b08d57; border-bottom: 1px solid rgba(176,141,87,0.2); padding-bottom: 8px; font-size: 18px; text-transform: uppercase; }}
            .main-text {{ text-align: justify; font-size: 14px; margin-bottom: 40px; color: #d1d1d1; }}

            .grid-box {{ display: table; width: 100%; border-spacing: 20px 0; margin: 20px -20px; }}
            .box-item {{ display: table-cell; width: 50%; padding: 20px; border-radius: 8px; vertical-align: top; }}
            .shadow {{ background: rgba(255, 68, 68, 0.08); border-left: 4px solid #ff4444; }}
            .growth {{ background: rgba(0, 200, 81, 0.08); border-left: 4px solid #00c851; }}

            .warning-box {{ background: rgba(255, 68, 68, 0.03); border: 1px solid rgba(255, 68, 68, 0.3); padding: 20px; margin-top: 30px; }}
            .gold-box {{ border: 1px solid #d4af37; padding: 25px; margin-top: 30px; background: rgba(212, 175, 55, 0.02); }}

            .footer {{ text-align: center; font-size: 9px; margin-top: 60px; opacity: 0.4; letter-spacing: 2px; }}
        </style>
    </head>
    <body>
        <div class="logo-container">
            <div class="vvv-logo">V V V</div>
        </div>

        <div class="header">
            <div class="system-label">Sacred Geometry & Frequency</div>
            <div class="title">{result.title}</div>
            <p style="font-style: italic; font-size: 14px;">Индивидуальный энергетический оттиск: <b>{name}</b></p>
        </div>

        <div class="meta-grid">
            <div class="meta-item">АРКАН: {extras['arcane'] if extras else '---'}</div>
            <div class="meta-item">ПЛАНЕТА: {extras['planet'] if extras else '---'}</div>
            <div class="meta-item">СТИХИЯ: {extras['element'] if extras else '---'}</div>
        </div>

        <div class="main-text">
            {result.full_text}
        </div>

        <div class="grid-box">
            <div class="box-item shadow">
                <b style="color:#ff4444; font-size: 12px; text-transform: uppercase;">Теневая сторона:</b><br>
                <p style="font-size:13px; margin-top: 10px;">{result.shadow_side}</p>
            </div>
            <div class="box-item growth">
                <b style="color:#00c851; font-size: 12px; text-transform: uppercase;">Точка роста:</b><br>
                <p style="font-size:13px; margin-top: 10px;">{result.growth_point}</p>
            </div>
        </div>

        <h3>Резонирующие сферы (Профессии):</h3>
        <p style="color: #fff; font-size: 14px; margin-bottom: 30px;">{", ".join(prof_list)}</p>

        <div class="warning-box">
            <b style="color:#ff4444; font-size: 12px; text-transform: uppercase;">⚠️ Внимание: Зоны энергетического спада</b><br>
            <p style="font-size:13px; font-style: italic; margin-top: 10px;">Не рекомендуется: {result.avoid_spheres}</p>
        </div>

        <div class="gold-box">
            <div style="text-align: center; color: #d4af37; font-size: 14px; letter-spacing: 3px; margin-bottom: 15px;">СВЯЩЕННЫЕ РЕЗОНАНСЫ</div>
            <table style="width: 100%; font-size: 13px;">
                <tr>
                    <td style="color: #d4af37;"><b>Числа Силы:</b></td>
                    <td>{compatibility['perfect']}</td>
                </tr>
                <tr>
                    <td style="color: #ff4444;"><b>Точка Трения:</b></td>
                    <td>{compatibility['challenge']}</td>
                </tr>
                <tr>
                    <td><b>Идеальный партнер:</b></td>
                    <td>{compatibility['partner_desc']}</td>
                </tr>
            </table>
        </div>

        <div class="footer">
            GENESIS SYSTEM PROTOCOL v3.0 | SECURED ARCHIVE | {datetime.now().strftime('%Y')}
        </div>
    </body>
    </html>
    """

    filename = f"Genesis_Report_{name.replace(' ', '_')}.pdf"
    try:
        options = {
            'encoding': "UTF-8",
            'page-size': 'A4',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'no-outline': None,
            'quiet': ''
        }
        pdfkit.from_string(styled_html, filename, configuration=PDF_CONFIG, options=options)
        return filename
    except Exception as e:
        print(f"Ошибка генерации PDF: {e}")
        return None


# 4. МАРШРУТЫ
@app.route('/', methods=['GET', 'POST'])
def index():
    # Инициализируем переменные, чтобы страница не падала при обычном открытии (GET)
    result, pdf_file, professions, compatibility, extras = None, None, None, None, None

    if request.method == 'POST':
        # 1. Извлекаем данные из формы
        name = request.form.get('name')
        email = request.form.get('email')
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')

        if day and month and year:
            # Складываем всё в одну строку, чтобы посчитать общую сумму цифр
            full_date_str = f"{day}{month}{year}"
            arch_number = str(calculate_digit(full_date_str))

            # Для отладки: выведи в консоль, что посчиталось
            print(f"--- DEBUG: Full Date: {full_date_str} | Archetype: {arch_number} ---")

        # Проверяем, что day не пустой, прежде чем считать
        if day:
            arch_number = str(calculate_digit(day))

            # 2. Ищем данные в БД
            result = ArchetypeContent.query.filter_by(number=arch_number).first()
            prof_data = ProfessionContent.query.filter_by(number=arch_number).first()

            if result:
                professions = prof_data.list_csv if prof_data else ""

                # 3. Считаем совместимость
                num = int(arch_number)
                compatibility = {
                    "perfect": f"{(num + 2) % 9 + 1}, {(num + 5) % 9 + 1}",
                    "challenge": str((num + 3) % 9 + 1),
                    "partner_desc": result.partner_type
                }

                # 4. Доп. метаданные из твоего словаря в data.py
                extras = ARCHETYPE_EXTRAS.get(arch_number)

                # 5. Сохраняем запись в историю
                db.session.add(AnalysisRecord(
                    name=name,
                    email=email,
                    birth_date=day,
                    archetype=arch_number,
                    professions=professions
                ))
                db.session.commit()

                # 6. Генерируем PDF
                pdf_file = create_pdf_report(name, result, professions, extras, compatibility)

    # Возвращаем все переменные в шаблон
    return render_template('index.html',
                           result=result,
                           pdf_file=pdf_file,
                           professions=professions,
                           compatibility=compatibility,
                           extras=extras)

@app.route('/genesis-admin')
def admin_dashboard():
    records = AnalysisRecord.query.order_by(AnalysisRecord.created_at.desc()).all()
    archetypes = ArchetypeContent.query.order_by(ArchetypeContent.number).all()
    profs = ProfessionContent.query.order_by(ProfessionContent.number).all()
    stats_raw = db.session.query(AnalysisRecord.archetype, func.count(AnalysisRecord.archetype)).group_by(
        AnalysisRecord.archetype).all()
    return render_template('admin.html', records=records, archetypes=archetypes, profs=profs,
                           stats={str(k): v for k, v in stats_raw})


@app.route('/admin/edit/<type>/<int:id>', methods=['POST'])
def quick_edit(type, id):
    if type == 'arch':
        item = db.session.get(ArchetypeContent, id)
        if item:
            item.title = request.form.get('title')
            item.full_text = request.form.get('full_text_html')
            item.shadow_side = request.form.get('shadow_side')  # Поддержка новых полей
            item.growth_point = request.form.get('growth_point')
            item.partner_type = request.form.get('partner_type')
    elif type == 'prof':
        item = db.session.get(ProfessionContent, id)
        if item: item.list_csv = request.form.get('list_csv')
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


@app.route('/admin/export-csv')
def export_csv():
    records = AnalysisRecord.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Имя', 'Email', 'Архетип'])
    for r in records: writer.writerow([r.name, r.email, r.archetype])
    return Response(output.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=export.csv"})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)