# nexus_modules.py

def inject_matrix_data(context):
    """Пример ноды: обогащает контекст данными матрицы"""
    user = context['user']
    # Твоя существующая логика из mind_logic
    from mind_logic import calculate_full_matrix_logic
    matrix, *_ = calculate_full_matrix_logic(user.birth_date.day, user.birth_date.month, user.birth_date.year)

    context['stats']['matrix_power'] = len(matrix.get('1', ''))  # Сила характера
    context['display_matrix'] = True
    return context


def inject_daily_forecast(context):
    """Пример ноды: прогноз на день"""
    import random
    forecasts = ["День созидания", "Время тишины", "Импульс к действию"]
    context['daily_msg'] = random.choice(forecasts)
    return context

def get_current_focus():
    from datetime import datetime
    hour = datetime.now().hour
    # Упрощенная логика китайских двухчасовок или планетарных часов
    if 5 <= hour < 9: return "ЗОЛОТОЙ ЧАС: Время для манифестации воли."
    if 22 <= hour or hour < 5: return "ГЛУБОКАЯ ФАЗА: Время загрузки подсознания."
    return "АКТИВНЫЙ ЦИКЛ: Внедрение идей в материю."