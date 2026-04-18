from flask import Blueprint, render_template, request, jsonify
from models import db, ArchetypeContent, Article, UserRecord

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# Страница входа/панели
@admin_bp.route('/')
def admin_panel():
    articles = Article.query.all()
    records = UserRecord.query.order_by(UserRecord.created_at.desc()).all()
    stats = {str(i): UserRecord.query.filter_by(archetype=str(i)).count() for i in range(1, 10)}
    return render_template('admin.html', articles=articles, records=records, stats=stats)


# Получение данных архетипа (для JS fetch)
@admin_bp.route('/get/<int:number>')
def get_archetype(number):
    arc = ArchetypeContent.query.filter_by(number=str(number)).first()
    if not arc:
        return jsonify({'data': {}})

    # Список всех полей из твоей модели ArchetypeContent
    fields = [
        'title', 'planet', 'element', 'search_queries', 'action_power',
        'shadow_side', 'exit_minus', 'growth_point', 'realization',
        'karmic_tasks', 'development_cycle', 'life_result', 'mind_power',
        'partner_type', 'financial_tip', 'health_tips'
    ]
    data = {f: getattr(arc, f) for f in fields}
    return jsonify({'data': data})


# Обновление данных
@admin_bp.route('/update', methods=['POST'])
def update_archetype():
    data = request.json
    num = str(data.get('number'))
    arc = ArchetypeContent.query.filter_by(number=num).first()

    if not arc:
        arc = ArchetypeContent(number=num)
        db.session.add(arc)

    for key, value in data.items():
        if hasattr(arc, key) and key != 'number':
            setattr(arc, key, value)

    db.session.commit()
    return jsonify({'status': 'ok'})


# Удаление записи пользователя
@admin_bp.route('/delete-record/<int:id>', methods=['POST'])
def delete_record(id):
    rec = UserRecord.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return render_template('admin.html')  # Или редирект