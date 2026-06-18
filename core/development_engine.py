class DevelopmentEngine:
    @staticmethod
    def build(advanced):
        recommendations = []
        focus_area = "Личностный рост"
        main_risk = "Не определен"
        main_strength = "Не определена"
        temperament = advanced.get(
            "temperament",
            ""
        )
        spirituality = advanced.get(
            "spirituality",
            {}
        )
        karma = advanced.get(
            "karma",
            []
        )
        imbalances = advanced.get(
            "imbalances",
            []
        )
        # ===== ТЕМПЕРАМЕНТ =====
        if "Приемник" in temperament:
            main_strength = (
                "Глубокое восприятие людей и ситуаций"
            )
            recommendations.extend([
                "Выделять время на восстановление энергии",
                "Избегать перегруженного окружения",
                "Ограничивать контакт с токсичными людьми"
            ])
        elif "Донор" in temperament:
            main_strength = (
                "Способность вдохновлять и вести других"
            )
            recommendations.extend([
                "Регулярная физическая активность",
                "Лидерские задачи",
                "Передача опыта другим людям"
            ])
        # ===== КАРМА =====
        for lesson in karma:
            if "Здоровья" in lesson:
                focus_area = "Физический ресурс"
                recommendations.append(
                    "Сформировать устойчивый режим сна и нагрузки"
                )
            elif "Логики" in lesson:
                focus_area = "Системность"
                recommendations.append(
                    "Планировать неделю заранее"
                )
            elif "Созидания" in lesson:
                focus_area = "Завершение проектов"
                recommendations.append(
                    "Доводить начатое до результата"
                )
            elif "Ответственности" in lesson:
                focus_area = "Личная зрелость"
                recommendations.append(
                    "Брать обязательства и выполнять их"
                )
        # ===== ПЕРЕКОСЫ =====
        if imbalances:
            imbalance = imbalances[0]
            main_risk = imbalance.get(
                "status",
                ""
            )
            recommendations.append(
                imbalance.get(
                    "recommendation",
                    ""
                )
            )
        return {
            "main_strength":
                main_strength,
            "main_risk":
                main_risk,
            "focus_area":
                focus_area,
            "recommendations":
                recommendations[:6]
        }