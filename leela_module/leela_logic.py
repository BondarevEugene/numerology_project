from flask import Blueprint, render_template
from .leela_data import DESCRIPTIONS
from flask import Blueprint, render_template
# ОБЯЗАТЕЛЬНО импортируем все три переменные здесь:
from .leela_data import DESCRIPTIONS, SNAKES, ARROWS

# Создаем блюпринт
leela_bp = Blueprint('leela', __name__,
                     template_folder='templates',
                     static_folder='static',
                     static_url_path='/leela_static')


@leela_bp.route('/play')
def play():
    return render_template('leela.html',
                           cells_info=DESCRIPTIONS,
                           snakes=SNAKES,
                           arrows=ARROWS)
