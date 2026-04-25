from flask import Blueprint, render_template, request
from models import db, Article, ArchetypeContent, ProfessionContent, User
from mind_logic import sum_digits, calculate_full_matrix_logic

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    # Загрузка трендов
    try:
        trends = Article.query.filter_by(category='Trends').limit(3).all()
    except Exception as e:
        print(f"⚠️ Ошибка загрузки трендов: {e}")
        trends = []

    # Инициализация переменных для шаблона
    result = {}
    cells = {}
    jobs = []
    user_name = ""
    day = month = year = ""
    user_skills = {"labels": ["Лидерство", "Коммуникация", "Эмпатия", "Логика", "Agile"], "data": [40, 50, 60, 70, 80]}
    energy_data = [5] * 7

    if request.method == 'POST':
        user_name = request.form.get('user_name', 'Гость')
        day = request.form.get('day', '01')
        month = request.form.get('month', '01')
        year = request.form.get('year', '1990')
        email = request.form.get('email', '')

        # 1. Расчет матрицы (Распаковка 4-х значений)
        cells, user_skills_raw, all_digits, _ = calculate_full_matrix_logic(day, month, year)

        # 2. Расчет числа архетипа
        group_num = sum_digits(int(day))
        result['group_num'] = group_num
        result['cells'] = cells

        # 3. Получение данных из БД ArchetypeContent
        try:
            arc_db = ArchetypeContent.query.filter_by(number=str(group_num)).first()
            if arc_db:
                result['title'] = f"{user_name}: {arc_db.title}"
                result['action_power'] = arc_db.action_power or ""
                result['shadow_side'] = arc_db.shadow_side or ""
                result['karmic_tasks'] = arc_db.karmic_tasks or ""
                result['career_business'] = arc_db.realization or "Анализ карьеры..."
            else:
                result['title'] = f"Анализ для {user_name}"
        except Exception as e:
            print(f"⚠️ Ошибка БД Архетипов: {e}")

        # 4. Получение профессий из БД
        try:
            prof_data = ProfessionContent.query.filter_by(number=str(group_num)).first()
            if prof_data and prof_data.list_csv:
                jobs = [j.strip() for j in prof_data.list_csv.split(',')]
            else:
                jobs = ["Аналитик", "Консультант", "Менеджер"]
        except Exception as e:
            print(f"⚠️ Ошибка БД Профессий: {e}")
            jobs = ["Данные временно недоступны"]

        # 5. Сохранение записи пользователя
        try:
            new_rec = User(full_name=user_name, email=email, archetype_num=str(group_num))
            db.session.add(new_rec)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Ошибка записи: {e}")

    # Подготовка строк для вывода
    result['professions'] = ", ".join(jobs)

    return render_template('index.html',
                           result=result,
                           cells=cells,
                           user_skills=user_skills,
                           energy_data=energy_data,
                           jobs=jobs,
                           trends=trends,
                           name=user_name,
                           day=day,
                           month=month,
                           year=year)