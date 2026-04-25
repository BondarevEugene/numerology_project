from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from models import db, User, ArchetypeContent, ProfessionContent, Course
from mind_logic import calculate_full_matrix_logic, sum_digits, SYNASTRY_TEXTS
from data import ARCHETYPE_EXTRAS
import math
import datetime  # <--- ОБЯЗАТЕЛЬНО ЭТА СТРОКА ИНАЧЕ ПАДАЕТ РЕГИСТРАЦИЯ
from datetime import date

profile_bp = Blueprint('profile', __name__)


def get_temporal_advice():
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return {"status": "ИНИЦИАЦИЯ", "msg": "Время установки векторов. Энергия на пике созидания.",
                "color": "#00ff88"}
    elif 11 <= hour < 17:
        return {"status": "ЭКСПАНСИЯ", "msg": "Активная фаза захвата ресурсов и реализации цепочек.",
                "color": "#d4af37"}
    elif 17 <= hour < 22:
        return {"status": "АНАЛИЗ", "msg": "Время подведения итогов и калибровки настроек.", "color": "#00d1ff"}
    else:
        return {"status": "СОН РАЗУМА", "msg": "Глубокая фаза обработки данных. Не принимайте решений.",
                "color": "#ff4444"}


@profile_bp.route('/profile')
def nexus_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = db.session.get(User, session['user_id'])
    # Генерируем динамические логи "на лету" (имитация работы Nexus)
    system_status = []
    if bio_data['phys'] < 30:
        system_status.append({"msg": "LOW_PHYSICAL_RESERVE: Рекомендуется минимизировать нагрузки", "type": "warn"})
    if int(matrix.get('1', '0').replace('-', '0')) > 111:
        system_status.append({"msg": "LEADERSHIP_OVERFLOW: Высокое давление на окружение", "type": "info"})
    # Nexus сам решит: считать биоритмы, луну или матрицу сегодня
    # Мы просто передаем 'user', а получаем 'render_context'
    context = nexus.execute_event('on_dashboard_load', {'user': user, 'stats': {}})
    system_status.append({"msg": f"SYNC_COMPLETED: Node_{user.id} stable", "type": "success"})

    return render_template('profile.html', **context)


@profile_bp.route('/profile')
def dashboard():
    # 1. Проверка авторизации
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # СНАЧАЛА получаем пользователя
    user = db.session.get(User, session['user_id'])

    if not user:
        return redirect(url_for('auth.login'))

    # ТЕПЕРЬ рассчитываем биоритмы, так как переменная 'user' уже существует
    bio_data = get_biorhythms(user.birth_date)

    # 2. Базовые расчеты даты
    d, m, y = user.birth_date.day, user.birth_date.month, user.birth_date.year

    # 3. Расчет Психоматрицы
    matrix, *_ = calculate_full_matrix_logic(d, m, y)

    # 4. Получение основного Архетипа (1-9) и контента из Neon
    arc_num = str(sum_digits(d))
    content = ArchetypeContent.query.filter_by(number=arc_num).first()

    # 5. Сбор дополнительных данных "из всех углов"
    # А) Астро-ключи из data.py
    extra = ARCHETYPE_EXTRAS.get(arc_num, {})

    # Б) Рекомендованные профессии из таблицы ProfessionContent
    professions = ProfessionContent.query.filter_by(number=arc_num).first()
    prof_list = professions.list_csv.split(',') if professions and professions.list_csv else []

    # В) Рекомендованные курсы/обучение
    courses = Course.query.filter_by(archetype_num=arc_num).all()

    # 6. Расчет динамических показателей (stats) для графиков
    # Считаем "мощность" каждого сектора матрицы
    def nexus_get_power(key):
        val = matrix.get(key, '')
        return len(val)

    stats = {
        "haracter": get_power('1'),
        "energy": get_power('2'),
        "interest": get_power('3'),
        "health": get_power('4'),
        "logic": get_power('5'),
        "trud": get_power('6'),
        "luck": get_power('7'),
        "duty": get_power('8'),
        "memory": get_power('9')
    }

    # 7. Расчет "Вибрационного Числа Года" (текущий прогноз)
    current_year = date.today().year
    year_vibe = sum_digits(d + m + current_year)

    system_status = []
    if bio_data['phys'] < 30:
        system_status.append({"msg": "LOW_PHYSICAL_RESERVE: Рекомендуется минимизировать нагрузки", "type": "warn"})
    if int(matrix.get('1', '0').replace('-', '0')) > 111:
        system_status.append({"msg": "LEADERSHIP_OVERFLOW: Высокое давление на окружение", "type": "info"})

    # Добавляем "шум" для атмосферы
    system_status.append({"msg": f"SYNC_COMPLETED: Node_{user.id} stable", "type": "success"})

    # 8. Формируем итоговый объект для шаблона
    return render_template('profile.html',
                           user=user,
                           matrix=matrix,
                           content=content,
                           stats=stats,  # ваши расчеты (haracter, energy и т.д.)
                           bio=bio_data,  # <--- ВОТ ЭТОГО НЕ ХВАТАЛО
                           extra=extra,
                           professions=prof_list,
                           courses=courses,
                           year_vibe=year_vibe,
                           spirit_level=min(100, (stats['haracter'] + stats['luck']) * 15),
                           today=datetime.date.today(),
                           current_year=datetime.date.today().year)


def get_moon_phase(dt):
    # Упрощенный расчет фазы Луны
    diff = dt - date(2000, 1, 6)
    days = diff.days % 29.53
    if days < 1.84:
        return "Новолуние 🌑"
    elif days < 9.22:
        return "Растущая Луна 🌓"
    elif days < 16.61:
        return "Полнолуние 🌕"
    else:
        return "Убывающая Луна 🌗"


@profile_bp.route('/profile/compatibility', methods=['POST'])
# moon = get_moon_phase(user.birth_date)
# bio = get_biorhythms(user.birth_date)
# return render_template(..., moon=moon, bio=bio)
def nexus_compatibility():
    """Максимально точный расчет совместимости"""
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    user = db.session.get(User, session['user_id'])
    partner_date_str = request.form.get('partner_date')

    try:
        p_date = datetime.date.today().strptime(partner_date_str, '%Y-%m-%d')

        # Логика Арканов (до 22)
        def to_22(day):
            return day if day <= 22 else day - 22

        a1 = to_22(user.birth_date.day)
        a2 = to_22(p_date.day)

        pair_num = a1 + a2
        if pair_num > 22: pair_num -= 22

        description = SYNASTRY_TEXTS.get(pair_num, "Ваш союз — это уникальный кармический узел.")

        return jsonify({
            "status": "success",
            "pair_num": pair_num,
            "description": description
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@profile_bp.route('/profile')
@login_required
def dashboard():
    user = current_user
    d, m, y = user.birth_date.day, user.birth_date.month, user.birth_date.year

    # 1. Психоматрица и Скиллы (из твоей mind_logic)
    matrix, extra_nums, user_skills = calculate_full_matrix_logic(d, m, y)

    # 2. Архетип и доп. данные из data.py
    arc_num = str(sum_digits(d))
    extras = ARCHETYPE_EXTRAS.get(arc_num, {})

    # 3. Биоритмы и Луна
    bio_data = get_biorhythms(user.birth_date)
    moon_phase = get_moon_phase(date.today())

    # 4. Временной совет (Инициация/Экспансия и т.д.)
    temp_advice = get_temporal_advice()

    # 5. График энергии (7 чакр/дней)
    # Здесь можно вставить реальную логику или оставить как в index.html
    energy_data = [5, 7, 8, 4, 6, 9, 5]

    return render_template('profile.html',
                           user=user,
                           matrix=matrix,
                           extra_nums=extra_nums,
                           user_skills=user_skills,
                           arc_num=arc_num,
                           extras=extras,
                           bio_data=bio_data,
                           moon_phase=moon_phase,
                           temp_advice=temp_advice,
                           energy_data=energy_data)

def get_moon_phase(date):
    """Примерный расчет фазы Луны (0 - новолуние, 14 - полнолуние)"""
    diff = date - datetime.date.today()(2000, 1, 6)  # Дата известного новолуния
    days = diff.days
    phase = (days % 29.53059)
    if phase < 1.84:
        return "Новолуние 🌑"
    elif phase < 5.53:
        return "Молодая луна 🌒"
    elif phase < 9.22:
        return "Первая четверть 🌓"
    elif phase < 12.91:
        return "Растущая луна 🌔"
    elif phase < 16.61:
        return "Полнолуние 🌕"
    elif phase < 20.30:
        return "Убывающая луна 🌖"
    elif phase < 23.99:
        return "Последняя четверть 🌗"
    else:
        return "Старая луна 🌘"


def get_biorhythms(birth_date):
    """Расчет биоритмов на сегодня (в процентах)"""
    today = datetime.date.today()
    days = (today - birth_date).days
    # Циклы: Физический (23 дня), Эмоциональный (28), Интеллектуальный (33)
    p = math.sin(2 * math.pi * days / 23) * 100
    e = math.sin(2 * math.pi * days / 28) * 100
    i = math.sin(2 * math.pi * days / 33) * 100
    return {"phys": round(p), "emot": round(e), "intel": round(i)}


# Внутри @profile_bp.route('/profile') добавь:
# moon = get_moon_phase(user.birth_date)
# bio = get_biorhythms(user.birth_date)
# return render_template(..., moon=moon, bio=bio)

# ==========================================
# 2. NEXUS WRAPPERS (Обертки для админки)
# ==========================================
def nexus_get_biorhythms_data(user):
    """Эта функция теперь видна в NEXUS-админке"""
    return get_biorhythms(user.birth_date)


def nexus_calculate_moon_logic(user):
    """И эта тоже"""
    return get_moon_phase(user.birth_date)


def nexus_biorhythms_check(context):
    """[NODE] Проверка биоритмов пользователя для системы логов"""
    # Вызываем твою основную функцию
    user_birth = context['user'].birth_date
    results = get_biorhythms(user_birth)
    return results


def nexus_moon_phase_info(context):
    """[NODE] Получение фазы луны для дашборда"""
    today = datetime.date.today()
    return get_moon_phase(today)


def nexus_matrix_power(context):
    """[NODE] Анализ силы матрицы (111+)"""
    matrix = context.get('matrix', {})
    # Логика анализа...
    return "High Energy" if len(matrix.get('1', '')) > 2 else "Stable"


def get_temporal_advice():
    from datetime import datetime
    hour = datetime.now().hour

    if 5 <= hour < 11:
        return {"status": "Инициация", "msg": "Время для установки векторов дня. Энергия на пике созидания."}
    elif 11 <= hour < 17:
        return {"status": "Экспансия", "msg": "Активная фаза захвата ресурсов и реализации логических цепочек."}
    elif 17 <= hour < 22:
        return {"status": "Анализ", "msg": "Время подведения итогов и калибровки внутренних настроек."}
    else:
        return {"status": "Сон разума", "msg": "Глубокая фаза обработки данных подсознанием. Не принимать решений."}
