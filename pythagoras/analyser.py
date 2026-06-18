# -*- coding: utf-8 -*-
"""
Модуль: analyser.py
Назначение: Глубокий экспертный анализ психоматрицы Пифагора.
Включает расчет векторов реализации, линий семейности, духовности и кармических задач.
"""


class PersonalityAdvancedAnalyser:
    def __init__(self, matrix):
        """
        Инициализация анализатора.
        :param matrix: Словарь данных матрицы, например {'1': '111', '2': '22', ...}
        """
        # Преобразуем строковые значения (цифры) в их количество
        self.counts = {str(i): len(matrix.get(str(i), "")) for i in range(1, 10)}
        self.raw_matrix = matrix

    def get_full_analysis(self):
        """
        Собирает все модули анализа в единый структурированный объект.
        """
        return {
            "imbalances": self._analyze_vectors(),
            "temperament": self._analyze_temperament(),
            "spirituality": self._analyze_diagonals(),
            "family_line": self._analyze_family_line(),
            "social_role": self._analyze_columns(),
            "karma": self._analyze_karma(),
            "chart_data": self.get_energy_chart_data()
        }

    def _analyze_vectors(self):
        """Анализ горизонтальных линий (Цели, Семья, Стабильность)."""
        reports = []

        # Строка 1 (1-4-7): Целеустремленность
        # Строка 3 (3-6-9): Стабильность / Быт
        goal_line = self.counts['1'] + self.counts['4'] + self.counts['7']
        stability_line = self.counts['3'] + self.counts['6'] + self.counts['9']

        if goal_line > stability_line + 2:
            reports.append({
                "aspect": "Вектор реализации",
                "status": "Перевес в сторону амбиций",
                "recommendation": "Вы склонны строить масштабные планы, но часто не имеете под ними твердой почвы. Чтобы идеи воплощались, начните с наведения порядка в финансах и повседневных делах. Дисциплина — ваш главный союзник."
            })
        elif stability_line > goal_line + 2:
            reports.append({
                "aspect": "Вектор реализации",
                "status": "Застой в стабильности",
                "recommendation": "У вас огромный потенциал для удержания достигнутого, но вы боитесь перемен. Жизнь требует от вас риска. Попробуйте поставить цель, которая выходит за рамки вашего привычного комфорта."
            })
        else:
            reports.append({
                "aspect": "Вектор реализации",
                "status": "Баланс планов и ресурсов",
                "recommendation": "Вы реально оцениваете свои силы. Продолжайте двигаться по выбранному пути, сохраняя текущий темп."
            })
        return reports

    def _analyze_columns(self):
        """Анализ вертикальных столбцов (Самооценка, Работоспособность, Талант)."""
        # Столбец 1 (1-2-3): Самооценка
        self_esteem = self.counts['1'] + self.counts['2'] + self.counts['3']

        if self_esteem > 6:
            return "Лидер-эксцентрик. Огромная уверенность в себе, важно не допускать подавления окружающих."
        if self_esteem < 3:
            return "Скрытый потенциал. Вы часто недооцениваете свои таланты. Пора перестать быть в тени."
        return "Уверенный профессионал."

    def _analyze_family_line(self):
        """Анализ линии 2-5-8 (Семья и отношения)."""
        score = self.counts['2'] + self.counts['5'] + self.counts['8']
        if score >= 5:
            return "Высокая значимость рода. Семья для вас — главный источник силы, но остерегайтесь гиперопеки."
        if score <= 1:
            return "Индивидуалист. Для вас важна личная свобода и независимость. Традиционные рамки могут казаться тесными."
        return "Гармония в партнерстве."

    def _analyze_temperament(self):
        """Энергетический тип личности (Двойки и Четверки)."""
        energy = self.counts['2']
        health = self.counts['4']

        if energy >= 3:
            return "Энергетический Донор. Вы способны заряжать других, но без физической нагрузки энергия может превращаться в агрессию."
        if energy <= 1:
            return "Энергетический Приемник. Ваш ресурс ограничен. Избегайте 'токсичных' людей и шума, восстанавливайтесь через тишину."
        return "Сбалансированный энергообмен."

    def _analyze_diagonals(self):
        """Диагонали: Духовность (1-5-9) и Чувственность (3-5-7)."""
        spirit = self.counts['1'] + self.counts['5'] + self.counts['9']
        flesh = self.counts['3'] + self.counts['5'] + self.counts['7']

        if spirit > flesh + 2:
            desc = "Духовный приоритет. Идеалы и смыслы для вас важнее материальных благ."
        elif flesh > spirit + 2:
            desc = "Материальный приоритет. Вы твердо стоите на ногах, цените комфорт и осязаемый результат."
        else:
            desc = "Золотая середина между духом и материей."

        return {"description": desc, "spirit_score": spirit, "flesh_score": flesh}

    def _analyze_karma(self):
        """Анализ отсутствующих качеств (кармические задачи)."""
        missing_lessons = []
        if self.counts['4'] == 0:
            missing_lessons.append(
                "Урок Здоровья: Вам необходимо осознанно заниматься своим телом, оно не прощает пренебрежения.")
        if self.counts['5'] == 0:
            missing_lessons.append("Урок Логики: Учитесь планировать и доверять не только интуиции, но и фактам.")
        if self.counts['6'] == 0:
            missing_lessons.append("Урок Созидания: Важно научиться завершать начатое и ценить физический труд.")
        if self.counts['8'] == 0:
            missing_lessons.append("Урок Ответственности: Развивайте чувство долга перед близкими и обществом.")

        return missing_lessons if missing_lessons else [
            "Все базовые качества проявлены. Сосредоточьтесь на их углублении."]

    def get_energy_chart_data(self):
        """Подготовка меток и значений для графиков."""
        return {
            "labels": [
                'Воля (1)', 'Энергия (2)', 'Интерес (3)',
                'Здоровье (4)', 'Логика (5)', 'Труд (6)',
                'Удача (7)', 'Долг (8)', 'Память (9)'
            ],
            "values": [self.counts[str(i)] for i in range(1, 10)]
        }