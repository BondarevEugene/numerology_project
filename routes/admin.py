"""
--------------------------------------------------------------------------------
MODULE: admin.py
PROJECT: Genesis HR® | Intelligence Systems
VERSION: 2.2.1 (Stability Fix)
DATE: 2024-05-21
DESCRIPTION: Administrative Console & Nexus Orchestrator Logic.
--------------------------------------------------------------------------------
"""

import os
import re
import importlib
import inspect
from flask import Blueprint, render_template, request, jsonify, current_app
from models import db, ArchetypeContent
from flask_login import login_required, current_user # Добавьте login_required здесь

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# --- [ СЕКЦИЯ: ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ] ---

def scan_blueprint_fields(filepath):
    """[ SYNAPSE: CODE SCANNER ]"""
    if not filepath or not os.path.exists(filepath): return []
    found = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            found.update(re.findall(r"request\.(?:form|args)\.get\(['\"](\w+)['\"]", content))
            found.update(re.findall(r"def (nexus_\w+)", content))
    except: pass
    return sorted(list(found))

# --- [ СЕКЦИЯ: УПРАВЛЕНИЕ КОНТЕНТОМ ] ---

@admin_bp.route('/')
def admin_panel():
    return render_template('admin.html')

@admin_bp.route('/get/<number>')
def get_content(number):
    try:
        item = ArchetypeContent.query.filter_by(number=str(number)).first()
        if item:
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

        fields = ['title', 'planet', 'element', 'tarot_arcane', 'action_power', 'shadow_side',
                  'growth_point', 'realization', 'karmic_tasks', 'development_cycle',
                  'mind_power', 'life_result', 'partner_type', 'financial_tip',
                  'health_tips', 'exit_minus', 'search_queries']
        for field in fields:
            if field in data: setattr(item, field, data.get(field))
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# --- [ СЕКЦИЯ: NEXUS ORCHESTRATION ] ---

@admin_bp.route('/get_menu_structure')
def get_menu_structure():
    """[ SYNAPSE: MENU GENERATOR ]"""
    structure = {
        "GENESIS": [
            {"id": "main", "label": "Core Kernel", "url": "/"},
            {"id": "admin", "label": "Control Panel", "url": "/admin/"}
        ],
        "HR_INTELLIGENCE": [
            {"id": "profile", "label": "User Profiles", "url": "/profile/"},
            {"id": "auth", "label": "Access Vault", "url": "/auth/login"}
        ],
        "LEELA_PATH": []
    }
    for name, bp in current_app.blueprints.items():
        if name not in ['admin', 'main', 'auth', 'profile', 'static']:
            structure["LEELA_PATH"].append({
                "id": name, "label": name.upper().replace('_', ' '), "url": f"/{name}/"
            })
    return jsonify(structure)

@admin_bp.route('/nexus/nodes')
def nexus_nodes():
    nodes = []
    edges = []
    try:
        nodes.append({"data": {"id": "ADMIN", "label": "IL_CENTRO", "type": "center"}})
        nodes.append({"data": {"id": "DATABASE", "label": "BIBLIOTECA", "type": "database"}})
        edges.append({"data": {"source": "ADMIN", "target": "DATABASE"}})
        for name, bp in current_app.blueprints.items():
            if name == 'admin': continue
            nodes.append({"data": {"id": name.upper(), "label": name.upper(), "type": "module"}})
            edges.append({"data": {"source": "ADMIN", "target": name.upper()}})
        return jsonify({"nodes": nodes, "edges": edges})
    except Exception as e: return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/nexus/forge', methods=['POST'])
def nexus_forge():
    """[ PROTOCOL: THE FORGE ]"""
    try:
        data = request.json
        raw_name = data.get('name', '').strip()
        if not raw_name: return jsonify({"status": "error", "message": "Empty name"}), 400
        module_id = re.sub(r'[^a-zA-Z0-9_]', '', raw_name).lower()
        filename = f"blueprint_{module_id}.py"
        filepath = os.path.join(current_app.root_path, filename)

        if os.path.exists(filepath): return jsonify({"status": "error", "message": "Exists"}), 400

        template = f"from flask import Blueprint\n{module_id}_bp = Blueprint('{module_id}', __name__)\n"
        with open(filepath, 'w', encoding='utf-8') as f: f.write(template)
        return jsonify({"status": "success", "message": f"Module {filename} forged."})
    except Exception as e: return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/sync')
def admin_sync():
    """[ OPERATION: DATA REFLECTION ]"""
    try:
        from services import sync_data_to_local
        if sync_data_to_local(): return "✅ Synced", 200
        return "❌ Sync Error", 500
    except Exception as e: return f"❌ Error: {str(e)}", 500


@admin_bp.route('/evolution/manage', methods=['GET', 'POST'])
@login_required
# Здесь должен быть декоратор проверки прав админа (например, current_user.is_admin)
def manage_evolution():
    if request.method == 'POST':
        # Логика добавления нового протокола
        new_p = EvolutionProtocol(
            category=request.form.get('category'),
            sector_trigger=request.form.get('sector'),
            condition=request.form.get('condition'),
            title=request.form.get('title'),
            content=request.form.get('content'),
            xp_reward=int(request.form.get('xp', 50))
        )
        db.session.add(new_p)
        db.session.commit()

    protocols = EvolutionProtocol.query.all()
    return render_template('admin/evolution.html', protocols=protocols)

@admin_bp.route('/archetypes')
@login_required
def manage_archetypes():
    # Проверка на админа (если у вас есть поле is_admin)
    # if not current_user.is_admin: return "Access Denied", 403
    all_content = ArchetypeContent.query.order_by(ArchetypeContent.number).all()
    return render_template('admin/archetypes.html', content=all_content)

@admin_bp.route('/archetypes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_archetype(id):
    item = ArchetypeContent.query.get_or_404(id)
    if request.method == 'POST':
        item.title = request.form.get('title')
        item.content = request.form.get('content')
        item.shadow = request.form.get('shadow')
        item.advice = request.form.get('advice')
        db.session.commit()
        return redirect(url_for('admin.manage_archetypes'))
    return render_template('admin/edit_archetype.html', item=item)