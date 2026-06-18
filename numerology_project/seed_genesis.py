import os
from app import app, db, ArchetypeContent, ProfessionContent
# Проверь, что в этих файлах есть нужные ключи, иначе подставятся дефолтные значения
from content import ARCHETYPES
from data import ARCHETYPE_EXTRAS


def seed_database():
    with app.app_context():
        print("🌀 Перезагрузка Матрицы Genesis...")
        # Опасно, но эффективно для полной синхронизации структуры
        db.drop_all()
        db.create_all()

        for i in range(1, 10):
            num = str(i)
            # Извлекаем данные из твоих словарей
            core = ARCHETYPES.get(num, {})
            extra = ARCHETYPE_EXTRAS.get(num, {})

            # Создаем запись Архетипа
            # Мы пытаемся вытянуть специфические поля, если их нет — ставим заглушку
            arc = ArchetypeContent(
                number=num,
                title=core.get('title', f"Архетип {num}").replace('᚛ ', '').replace(' ᚜', ''),
                planet=extra.get('planet', 'Солнце' if num == '1' else 'Луна' if num == '2' else 'Неизвестно'),

                # Текстовые блоки
                action_power=core.get('full_text', core.get('description', "Энергия действия в процессе анализа...")),
                shadow_side=extra.get('shadow', "Теневые аспекты требуют осознания и трансформации."),
                growth_point=extra.get('growth', "Точка роста лежит в балансе между личным и общественным."),
                realization=extra.get('realization', "Максимальная реализация через служение своей цели."),
                karmic_tasks=extra.get('karma', "Отработка уроков ответственности и лидерства."),

                # Новые поля
                development_cycle=extra.get('cycle', "1 — 4 — 7"),
                mind_power=extra.get('mind', "Высокий потенциал стратегического мышления."),
                life_result=extra.get('result', "Достижение внутренней гармонии и признания."),
                partner_type=extra.get('partner', "Партнер, уважающий личное пространство."),
                financial_tip=extra.get('finance', "Финансовый поток открывается через системный подход."),
                health_tips=extra.get('health', "Рекомендуется регулярная медитация и водный баланс.")
            )
            db.session.add(arc)

            # Профессии (можно задать списком для каждого номера)
            default_profs = {
                "1": "Руководитель, Индивидуальный предприниматель, Изобретатель",
                "2": "Дипломат, Психолог, Аналитик, Консультант",
                "3": "Преподаватель, Творческий деятель, Маркетолог",
                "4": "Администратор, Финансист, Инженер, Строитель",
                "5": "Оратор, Юрист, Путешественник, Переводчик",
                "6": "Дизайнер, Врач, Искусствовед, Социальный работник",
                "7": "Исследователь, Философ, IT-специалист, Мистик",
                "8": "Банкир, Судья, Крупный управленец, Ревизор",
                "9": "Меценат, Психотерапевт, Гуманитарный деятель"
            }

            prof = ProfessionContent(
                number=num,
                list_csv=default_profs.get(num, "Консультант, Менеджер")
            )
            db.session.add(prof)

        try:
            db.session.commit()
            print(f"✅ Успешно импортировано 9 архетипов и списки профессий!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Ошибка при наполнении базы: {e}")


if __name__ == "__main__":
    seed_database()