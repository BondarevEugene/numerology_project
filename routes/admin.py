from flask import Blueprint, render_template, request, jsonify
from models import db, ArchetypeContent

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_panel():
    return render_template('admin.html')

@admin_bp.route('/get/<number>')
def get_content(number):
    try:
        item = ArchetypeContent.query.filter_by(number=str(number)).first()
        if item:
            # Автоматически собираем все поля модели в словарь
            columns = [c.name for c in item.__table__.columns if c.name != 'id']
            data = {col: getattr(item, col) or "" for col in columns}
            return jsonify({"status": "success", "data": data})
        return jsonify({"status": "error", "message": "Аркан не найден"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/update', methods=['POST'])
def update_content():
    try:
        data = request.json
        number = str(data.get('number'))
        item = ArchetypeContent.query.filter_by(number=number).first()

        if not item:
            item = ArchetypeContent(number=number)
            db.session.add(item)

        # Список полей для маппинга (соответствует models.py и admin.html)
        fields = [
            'title', 'planet', 'element', 'tarot_arcane', 'action_power',
            'shadow_side', 'growth_point', 'realization', 'karmic_tasks',
            'development_cycle', 'mind_power', 'life_result', 'partner_type',
            'financial_tip', 'health_tips', 'exit_minus', 'search_queries'
        ]

        for field in fields:
            if field in data:
                setattr(item, field, data.get(field))

        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500