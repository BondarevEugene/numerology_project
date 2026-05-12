# leela_module/leela_logic.py
from flask import Blueprint, render_template, request
from .leela_data import DESCRIPTIONS, SNAKES, ARROWS

# Создаем блюпринт (один раз)
leela_bp = Blueprint('leela', __name__,
                     template_folder='templates',
                     static_folder='static',
                     static_url_path='/leela_static')


@leela_bp.route('/play')
def play():
    """
    Основной роут игры. 
    Получает архетип пользователя из параметров запроса (arch),
    чтобы подсветить персональные клетки силы на 3D-доске.
    """
    # Получаем архетип (например, /lila/play?arch=5)
    # Если его нет, по умолчанию будет '0'
    user_archetype = request.args.get('arch', '0')

    # Рендерим 3D-шаблон, передавая все необходимые данные
    return render_template('leela.html',
                           cells_info=DESCRIPTIONS,
                           snakes=SNAKES,
                           arrows=ARROWS,
                           user_archetype=user_archetype)

# Место для будущих функций (например, API для сохранения инсайтов)