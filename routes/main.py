from flask import Blueprint, render_template, request, current_app, redirect, url_for
from models import db, Article, ArchetypeContent, ProfessionContent, UserRecord
import os

# Импортируем расчеты и тексты из mind_logic
from mind_logic import NODES_INFO, SYNASTRY_TEXTS, sum_digits, calculate_full_matrix_logic
# Импортируем сервис карьеры из utils
from utils import CareerService

# Создаем блюпринт
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    # --- 1. ЗАГРУЗКА ТРЕНДОВ ИЗ БАЗЫ ---
    # Теперь, когда ты заполнил таблицу пробными данными, они появятся на главной
    try:
        trends = Article.query.filter_by(category='Trends').limit(3).all()
    except Exception as e:
        print(f"⚠️ Ошибка загрузки трендов: {e}")
        trends = []

    # Инициализация переменных
    result = {}
    matrix_desc = {}
    matrix_lines = {}
    cells = {}
    jobs = []
    user_id = None
    synastry_result = None
    user_name = ""
    day = month = year = ""

    # Заглушки для графиков
    user_skills = {"labels": ["Лидерство", "Коммуникация", "Эмпатия", "Логика", "Agile"], "data": [40, 50, 60, 70, 80]}
    energy_data = [5, 5, 5, 5, 5, 5, 5]

    if request.method == 'POST':
        user_name = request.form.get('user_name', 'Гость')
        day = request.form.get('day', '01')
        month = request.form.get('month', '01')
        year = request.form.get('year', '1990')
        email = request.form.get('email', '')

        # Основной расчет матрицы (логика в mind_logic)
        raw_result = calculate_full_matrix_logic(day, month, year)
        result = raw_result[0] if isinstance(raw_result, tuple) else raw_result

        if result:
            matrix_desc = result.get('matrix_desc', {})
            matrix_lines = result.get('matrix_lines', {})
            energy_data = result.get('energy_data', [10] * 7)
            cells = result.get('matrix') or result.get('cells') or {}
            group_num = result.get('group_num', 1)

            # --- БЛОК 1: ПОЛУЧЕНИЕ ОПИСАНИЯ АРХЕТИПА ИЗ БД ---
            try:
                arc_db = ArchetypeContent.query.filter_by(number=str(group_num)).first()
                if arc_db:
                    result['archetype_title'] = arc_db.title
                    result['planet'] = arc_db.planet
                    result['element'] = arc_db.element
                    result['arcane'] = arc_db.tarot_arcane
                    result['shadow_side'] = arc_db.shadow_side
                    result['growth_point'] = arc_db.growth_point
                else:
                    result['archetype_title'] = f"Архетип №{group_num}"
            except Exception as e:
                print(f"⚠️ Ошибка ArchetypeContent: {e}")
                result['archetype_title'] = f"Архетип №{group_num} (БД Offline)"

            # --- БЛОК 2: ПОЛУЧЕНИЕ ПРОФЕССИЙ ИЗ БД ---
            try:
                prof_data = ProfessionContent.query.filter_by(number=str(group_num)).first()
                if prof_data and prof_data.list_csv:
                    # Разделяем строку из базы (CSV) в список
                    jobs = [j.strip() for j in prof_data.list_csv.split(',')]
                else:
                    jobs = ["Аналитик", "Консультант", "Менеджер"]
            except Exception as e:
                print(f"⚠️ Ошибка ProfessionContent: {e}")
                jobs = ["Данные профессий временно недоступны"]

            # --- БЛОК 3: РАСЧЕТ СКИЛЛОВ ДЛЯ ГРАФИКА ---
            s_data = [
                len(cells.get('1', '')) * 20,
                len(cells.get('8', '')) * 25,
                len(cells.get('5', '')) * 30,
                len(cells.get('3', '')) * 25,
                len(cells.get('9', '')) * 20
            ]
            user_skills['data'] = [max(20, min(100, x)) for x in s_data]

            # --- БЛОК 4: СОХРАНЕНИЕ ЗАПРОСА ПОЛЬЗОВАТЕЛЯ ---
            try:
                new_rec = UserRecord(
                    name=user_name,
                    email=email,
                    archetype=str(group_num)
                )
                db.session.add(new_rec)
                db.session.commit()
                user_id = new_rec.id
                print(f"✅ Успех: Пользователь {user_name} записан в базу.")
            except Exception as e:
                db.session.rollback()
                print(f"⚠️ Ошибка записи UserRecord: {e}")

    # Форматируем описания для вывода (приводим ключи к строкам)
    formatted_desc = {str(k): v for k, v in matrix_desc.items()} if matrix_desc else {}

    return render_template('index.html',
                           result=result,
                           matrix_desc=formatted_desc,
                           interpretations=formatted_desc,
                           cells=cells,
                           user_skills=user_skills,
                           energy_data=energy_data,
                           matrix_lines=matrix_lines,
                           jobs=jobs,
                           trends=trends,
                           user_id=user_id,
                           synastry_result=synastry_result,
                           name=user_name,
                           day=day,
                           month=month,
                           year=year)

@main_bp.route('/lila')
def lila_game():
    return render_template('lila.html')