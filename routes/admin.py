import os
import re
from flask import Blueprint, render_template, request, jsonify, current_app
from models import db, ArchetypeContent
import inspect
from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for
from models import db, ArchetypeContent, User  # Добавь NexusNode в models.py если используешь
import importlib  # Добавьте в импорты в начале файла

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


def scan_blueprint_fields(filepath):
    """Анализирует .py файл и находит request.form.get('...')"""
    if not os.path.exists(filepath): return {"form": [], "args": []}
    form_fields = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # Ищем поля в формах и аргументах
        form_fields.update(re.findall(r"request\.form\.get\(['\"](\w+)['\"]", content))
        form_fields.update(re.findall(r"request\.args\.get\(['\"](\w+)['\"]", content))
    return sorted(list(form_fields))


# --- РАЗДЕЛ NEXUS: ОРКЕСТРАЦИЯ СИСТЕМЫ ---

@admin_bp.route('/nexus/execute', methods=['POST'])
def nexus_execute_command():
    """Безопасный запуск управленческих функций"""
    data = request.json
    blueprint_name = data.get('module', '').lower()
    command = data.get('command')

    try:
        # 1. Проверка прав (можно добавить проверку сессии админа)
        bp = current_app.blueprints.get(blueprint_name)
        if not bp:
            return jsonify({"status": "error", "message": f"Модуль {blueprint_name} не найден"}), 404

        # 2. Динамический поиск функции
        module = importlib.import_module(bp.import_name)
        func = getattr(module, command, None)

        if not func or not command.startswith('nexus_'):
            return jsonify({"status": "error", "message": "Команда недоступна или запрещена"}), 403

        # 3. Выполнение
        result = func()
        return jsonify({"status": "success", "data": str(result)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/nexus')
def nexus_hub_view():
    """Единственная точка входа для визуального интерфейса"""
    return render_template('nexus_hub.html')


@admin_bp.route('/nexus/nodes')
def nexus_nodes_unified():
    """Сбор данных для графа: Ядро, БД и Блюпринты"""
    nodes = []
    edges = []
    try:
        # Базовые узлы (Центр и Библиотека данных)
        nodes.append({"data": {"id": "ADMIN", "label": "IL_CENTRO", "type": "center"}})
        nodes.append({"data": {"id": "DATABASE", "label": "BIBLIOTECA", "type": "database"}})
        edges.append({"data": {"source": "ADMIN", "target": "DATABASE"}})

        for name, blueprint in current_app.blueprints.items():
            if name == 'admin': continue
            node_id = name.upper()

            nexus_actions = []
            path = "Unknown"
            try:
                # Динамический анализ модуля
                module = importlib.import_module(blueprint.import_name)
                nexus_actions = [n for n, f in inspect.getmembers(module, inspect.isfunction) if n.startswith('nexus_')]

                # Получение физического пути
                endpoint = next((ep for ep in current_app.view_functions if ep.startswith(name + ".")), None)
                if endpoint:
                    path = inspect.getfile(current_app.view_functions[endpoint]).replace('\\', '/')
            except:
                pass

            nodes.append({
                "data": {
                    "id": node_id,
                    "label": node_id,
                    "type": "module",
                    "actions": nexus_actions,
                    "full_path": path
                }
            })
            edges.append({"data": {"source": "ADMIN", "target": node_id}})

        return jsonify({"nodes": nodes, "edges": edges})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@admin_bp.route('/nexus/inspect')
def nexus_inspect_unified():
    """Инспектор структуры файла (вызывается при клике на узел)"""
    path = request.args.get('path')
    fields = scan_blueprint_fields(path)

    # HTML-ответ для HTMX в стиле Да Винчи
    html = '<div style="color:#ff9000; font-family:\'Cinzel Decorative\'; margin-bottom:10px; border-bottom:1px solid #333; padding-bottom:5px;">• АНАЛИЗ МАНУСКРИПТА •</div>'
    if not fields:
        return html + '<div style="color:#555; font-style:italic;">Синапсы не обнаружены.</div>'

    html += '<ul style="list-style:none; padding:0; font-family:\'JetBrains Mono\'; font-size:11px;">'
    for f in fields:
        # Выделяем nexus-функции оранжевым, а поля — серым
        color = "#ff9000" if f.startswith('nexus_') else "#aaa"
        icon = "⚙" if f.startswith('nexus_') else "⚡"
        html += f'<li style="margin-bottom:6px; color:{color}; border-left:1px solid {color}; padding-left:8px;">{icon} {f}</li>'
    return html + '</ul>'


def scan_blueprint_fields(filepath):
    """Глубокий поиск связей внутри файла"""
    if not filepath or not os.path.exists(filepath): return []
    found = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Поля ввода (формы и аргументы)
            found.update(re.findall(r"request\.(?:form|args)\.get\(['\"](\w+)['\"]", content))
            # Функции управления
            found.update(re.findall(r"def (nexus_\w+)", content))
    except:
        pass
    return sorted(list(found))


# --- МОДУЛЬ УПРАВЛЕНИЯ NEXUS ---

@admin_bp.route('/nexus/call', methods=['POST'])
def nexus_execute():
    """Запуск сакральной функции модуля через интерфейс"""
    data = request.json
    blueprint_name = data.get('module').lower()
    action_name = data.get('action')

    try:
        # Ищем блюпринт и импортируем его модуль
        blueprint = current_app.blueprints.get(blueprint_name)
        if not blueprint:
            return jsonify({"status": "error", "message": "Blueprint not found"}), 404

        module = importlib.import_module(blueprint.import_name)
        func = getattr(module, action_name)

        # Запускаем функцию (она должна возвращать строку или словарь)
        result = func()
        return jsonify({"status": "success", "result": str(result)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500