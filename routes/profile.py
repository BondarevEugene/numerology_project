"""
--------------------------------------------------------------------------------
MODULE: profile.py (Mobile Sync Extension)
PROJECT: Genesis HR® | Intelligence Systems
VERSION: 2.6.0 (Mobile Integration)
DATE: 2024-05-21
DESCRIPTION: API endpoint for mobile application synchronization.
             Implements intelligent advice logic based on Matrix sectors.
--------------------------------------------------------------------------------
"""

import math
from datetime import date, datetime
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from models import db, User, ArchetypeContent, ProfessionContent, Course, SessionArchive
from utils import calculate_full_matrix_logic, sum_digits, SYNASTRY_TEXTS
from data import ARCHETYPE_EXTRAS
from flask import jsonify
from content import ARCHETYPES
from data import ARCHETYPE_EXTRAS
from mind_logic import sum_digits # или  функция расчета аркана
from datetime import datetime
from flask import render_template, redirect, url_for
from flask_login import current_user
# Импортируем словари с данными и логику
from content import ARCHETYPES
from data import ARCHETYPE_EXTRAS
from utils import calculate_full_matrix_logic, sum_digits

from core.profile_service import ProfileService

profile_bp = Blueprint('profile', __name__)


# --- [ СЕКЦИЯ: ОСНОВНОЙ МАРШРУТ ПАНЕЛИ ] ---


@profile_bp.route('/')
def index():
    # 1. Логика пользователя (Auth или Guest)
    if current_user.is_authenticated:
        user = current_user
    else:
        class GuestUser:
            id = 777
            username = "GUEST_PROTOCOL"
            full_name = "Авторизация пропущена"
            birth_date = datetime(1990, 5, 20)
            email = "guest@genesis.ai"
        user = GuestUser()

    # 2. Расчеты
    d, m, y = user.birth_date.day, user.birth_date.month, user.birth_date.year
    matrix, *_ = calculate_full_matrix_logic(d, m, y)
    arcane_number = d if d <= 22 else sum_digits(d)
    arcane_key = str(arcane_number)

    # 3. Данные из баз (content.py и data.py)
    content_data = ARCHETYPES.get(arcane_key, {})
    extra_data = ARCHETYPE_EXTRAS.get(arcane_key, {})

    # 4. Биоритмы и сессии
    bio_data = _calculate_biorhythms_internal(user.birth_date)
    user_sessions = []
    try:
        user_sessions = SessionArchive.query.filter_by(user_id=user.id).order_by(SessionArchive.created_at.desc()).limit(8).all()
    except: pass

    return render_template('profile.html',
                           user=user, matrix=matrix, bio=bio_data,
                           content=content_data, extra=extra_data,
                           user_sessions=user_sessions, arcane_key=arcane_key)

"""
    # 5. Статистика для Радара
stats = {
        'haracter': len(str(matrix.get('1', '')).replace('-', '')),
        'energy': len(str(matrix.get('2', '')).replace('-', '')),
        'interest': len(str(matrix.get('3', '')).replace('-', '')),
        'health': len(str(matrix.get('4', '')).replace('-', '')),
        'logic': len(str(matrix.get('5', '')).replace('-', '')),
        'trud': len(str(matrix.get('6', '')).replace('-', ''))
    }
"""

# --- [ СЕКЦИЯ: ВНУТРЕННЯЯ ЛОГИКА (HELPER FUNCTIONS) ] ---

def _calculate_biorhythms_internal(birth_date):
    """Внутренний расчет биоритмов для формирования контекста шаблона"""
    if not birth_date:
        return {"phys": 0, "emot": 0, "intel": 0}
    b_date = birth_date.date() if isinstance(birth_date, datetime) else birth_date
    days = (date.today() - b_date).days
    calc = lambda p: round(math.sin(2 * math.pi * days / p) * 100)
    return {"phys": calc(23), "emot": calc(28), "intel": calc(33)}


def _calculate_moon_phase(dt):
    """Расчет фазы Луны на основе даты рождения или текущей даты"""
    d_obj = dt.date() if isinstance(dt, datetime) else dt
    diff = d_obj - date(2000, 1, 6)  # Дата известного новолуния
    days = diff.days % 29.53059
    if days < 1.84:
        return "Новолуние 🌑"
    elif days < 9.22:
        return "Растущая Луна 🌓"
    elif days < 16.61:
        return "Полнолуние 🌕"
    return "Убывающая Луна 🌗"


def _get_temporal_advice():
    """Система временных советов Genesis на основе текущего часа"""
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return {"status": "ИНИЦИАЦИЯ", "msg": "Время установки векторов. Энергия на пике созидания.",
                "color": "#00ff88"}
    elif 11 <= hour < 17:
        return {"status": "ЭКСПАНСИЯ", "msg": "Активная фаза захвата ресурсов и реализации цепочек.",
                "color": "#d4af37"}
    elif 17 <= hour < 22:
        return {"status": "АНАЛИЗ", "msg": "Время подведения итогов и калибровки настроек.", "color": "#00d1ff"}
    return {"status": "СОН РАЗУМА", "msg": "Глубокая фаза обработки данных. Не принимайте решений.", "color": "#ff4444"}


# --- [ СЕКЦИЯ: API ЭНДПОИНТЫ (NEXUS OPERATIONS) ] ---

@profile_bp.route('/nexus/save_session', methods=['POST'])
@login_required
def save_current_session():
    """[ OPERATION: STATE ANCHOR ] Фиксация состояния в Chrono-Vault"""
    data = request.json
    try:
        new_session = SessionArchive(
            user_id=current_user.id,
            arcane_number=data.get('arcane'),
            state_tag=data.get('tag', 'Standard'),
            bio_physical=data.get('bio_p'),
            bio_emotional=data.get('bio_e'),
            bio_intellectual=data.get('bio_i'),
            notes=data.get('notes')
        )
        db.session.add(new_session)
        db.session.commit()
        return jsonify({"status": "anchored", "session_id": new_session.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@profile_bp.route('/nexus/archive')
@login_required
def get_archive_vault():
    """[ OPERATION: CHRONO-VAULT ACCESS ] Получение истории сессий"""
    sessions = SessionArchive.query.filter_by(user_id=current_user.id).order_by(SessionArchive.timestamp.desc()).all()
    return jsonify({
        "status": "accessed",
        "vault": [s.to_dict() for s in sessions]
    })


@profile_bp.route('/nexus/biorhythms')
@login_required
def get_biorhythms_api():
    """[ SYNAPSE: BIORHYTHM ENGINE ] API для динамического обновления биоритмов"""
    if not current_user.birth_date:
        return jsonify({"status": "warning", "message": "Birth date not set in core"}), 200

    data = _calculate_biorhythms_internal(current_user.birth_date)
    return jsonify({
        "status": "synchronized",
        "data": data
    })


@profile_bp.route('/compatibility', methods=['POST'])
@login_required
def nexus_compatibility():
    """[ OPERATION: SYNASTRY ] Расчет совместимости арканов"""
    partner_date_str = request.form.get('partner_date')
    try:
        p_date = datetime.strptime(partner_date_str, '%Y-%m-%d').date()

        def to_22(day):
            return day if day <= 22 else day - 22

        a1 = to_22(current_user.birth_date.day)
        a2 = to_22(p_date.day)

        pair_num = a1 + a2
        if pair_num > 22: pair_num -= 22

        description = SYNASTRY_TEXTS.get(pair_num, "Ваш союз — это уникальный кармический узел.")
        return jsonify({"status": "success", "pair_num": pair_num, "description": description})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# --- [ СЕКЦИЯ: ГЛАВНЫЙ ДАШБОРД ] ---

@profile_bp.route('/')
@login_required
def profile_home():
    """[ SYNAPSE: MAIN DASHBOARD ] Сборка всех данных для профиля пользователя"""
    user = current_user
    if not user.birth_date:
        return "Критический сбой: Дата рождения не найдена в профиле.", 400

    # 1. Расчеты Психоматрицы и Аркана
    d, m, y = user.birth_date.day, user.birth_date.month, user.birth_date.year
    matrix, *_ = calculate_full_matrix_logic(d, m, y)
    arc_num = str(sum_digits(d))

    # 2. Получение контента из базы данных
    content = ArchetypeContent.query.filter_by(number=arc_num).first()
    extra = ARCHETYPE_EXTRAS.get(arc_num, {})
    professions = ProfessionContent.query.filter_by(number=arc_num).first()
    prof_list = professions.list_csv.split(',') if professions and professions.list_csv else []
    courses = Course.query.filter_by(archetype_num=arc_num).all()

    # 3. Динамические показатели (Биоритмы и Луна)
    bio_data = _calculate_biorhythms_internal(user.birth_date)
    moon_phase = _calculate_moon_phase(user.birth_date)
    advice = _get_temporal_advice()

    # 4. Аналитика сил (Stats) для графиков
    def get_power(key):
        val = matrix.get(key, '')
        return 0 if val == '-' else len(str(val))

    stats = {k: get_power(v) for k, v in {
        "haracter": "1", "energy": "2", "interest": "3",
        "health": "4", "logic": "5", "trud": "6",
        "luck": "7", "duty": "8", "memory": "9"
    }.items()}

    # 5. Прогнозы и статусы системы
    current_year = date.today().year
    year_vibe = sum_digits(d + m + current_year)

    system_status = []
    if bio_data['phys'] < 30:
        system_status.append({"msg": "LOW_PHYSICAL_RESERVE: Требуется калибровка отдыха", "type": "warn"})
    if get_power('1') > 3:
        system_status.append({"msg": "LEADERSHIP_OVERFLOW: Высокое давление воли", "type": "info"})
    system_status.append({"msg": f"SYNC_COMPLETED: Node_{user.id} stable", "type": "success"})

    return render_template('profile.html',
                           user=user,
                           matrix=matrix,
                           content=content,
                           stats=stats,
                           bio=bio_data,
                           moon=moon_phase,
                           extra=extra,
                           professions=prof_list,
                           courses=courses,
                           year_vibe=year_vibe,
                           today=date.today(),
                           advice=advice,
                           system_status=system_status)


@profile_bp.route('/api/v1/mobile_sync')
@login_required
def mobile_sync_api():
    """
    Интеллектуальный эндпоинт: объединяет расчеты матрицы, биоритмов и
    генерирует контекстные рекомендации по спорту, питанию и рискам.
    """
    user = current_user

    # Расчет базовых структур Genesis
    d, m, y = user.birth_date.day, user.birth_date.month, user.birth_date.year
    matrix, *_ = calculate_full_matrix_logic(d, m, y)
    bio_data = _calculate_biorhythms_internal(user.birth_date)

    # Инициализация контейнера рекомендаций
    recommendations = {
        "food": "Сбалансированное питание. Поддержание энергетического плато.",
        "sport": "Стандартная активность согласно текущему биоритму.",
        "mind": "Анализ текущих задач и когнитивная настройка.",
        "risk": "Система стабильна. Критических резонансов не обнаружено."
    }

    # --- ЛОГИКА ИНТЕРПРЕТАЦИИ МАТРИЦЫ ---

    # Анализ Сектора 1 (Характер / Воля)
    h_val = str(matrix.get('1', '')).replace('-', '')
    if len(h_val) > 3:
        recommendations["risk"] = "LEADERSHIP_OVERFLOW: Избыточное давление воли. Риск деструктивного доминирования."
        recommendations["mind"] = "Практика 'Тихого Наблюдателя'. Снизьте ментальный контроль над окружением."

    # Анализ Сектора 4 (Здоровье / Физический ресурс)
    if matrix.get('4') == '-':
        recommendations[
            "sport"] = "HEALTH_LOW_RESERVE: Сектор здоровья не активен. Требуется принудительная активация тела (йога, плавание)."
        recommendations["food"] = "Genesis Diet: Исключить стимуляторы и тяжелые жиры. Фокус на гидратации."

    # Интеграция архетипического контента
    arcane_num = sum_digits(d)
    content = ArchetypeContent.query.filter_by(number=arcane_num).first()
    if content:
        recommendations["mind"] = f"Архетип {arcane_num}: {content.description[:150]}..."

    return jsonify({
        "status": "success",
        "node_id": f"GEN_MOBILE_{user.id}",
        "username": user.username,
        "matrix": matrix,
        "bio": bio_data,
        "rec": recommendations,
        "sync_time": datetime.now().isoformat()
    })


@profile_bp.route('/api/v1/evolution_sync')
@login_required
def evolution_sync():
    user = current_user
    d, m, y = user.birth_date.day, user.birth_date.month, user.birth_date.year
    matrix, *_ = calculate_full_matrix_logic(d, m, y)

    # Логіка вибору квестів із бази
    active_quests = []

    # Приклад: Реакція на пустий сектор 4 (Здоров'я)
    if matrix.get('4') == '-':
        quest = EvolutionProtocol.query.filter_by(sector_trigger=4, condition='empty').first()
        if quest:
            active_quests.append({"id": quest.id, "title": quest.title, "xp": quest.xp_reward})

    # Приклад: Реакція на перевантажений сектор 1 (Воля)
    if len(str(matrix.get('1', '')).replace('-', '')) > 3:
        quest = EvolutionProtocol.query.filter_by(sector_trigger=1, condition='overflow').first()
        if quest:
            active_quests.append({"id": quest.id, "title": quest.title, "xp": quest.xp_reward})

    return jsonify({
        "status": "active",
        "rank": "NEOPHYTE",  # Можна розрахувати на основі UserProgress
        "xp_progress": 0.45,
        "matrix": matrix,
        "daily_quests": active_quests,
        "detailed_analysis": ARCHETYPE_EXTRAS.get(sum_digits(d), {})
    })

@profile_bp.route("/cabinet")
@login_required
def cabinet():

    profile_data = ProfileService.build(
        current_user
    )

    return render_template(
        "templates_v3/profile/profile_v3.html",
        profile=profile_data
    )

