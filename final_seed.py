import pandas as pd
import os
import chardet
from app import app, db, ArchetypeContent


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read(20000)
    return chardet.detect(rawdata)['encoding'] or 'utf-8'


def clean_text(text):
    if pd.isna(text): return ""
    return str(text).replace("_x000D_", "").strip()


def seed_database():
    with app.app_context():
        print("🌀 Полная очистка и пересоздание базы...")
        db.drop_all()
        db.create_all()

        # Создаем структуру для всех 22 чисел
        vault = {str(i): {
            "mind": "", "action": "", "real": "", "result": "",
            "title": "", "shadow": "", "growth": "", "planet": "",
            "cycle": "", "karmic": "", "exit": ""
        } for i in range(1, 23)}

        # Имена файлов (проверь, чтобы они совпадали с твоими!)
        files = {
            'mind': 'I. Число УМА.csv',
            'action': 'II. Число ДЕЙСТВИЯ.csv',
            'real': 'III. Число РЕАЛИЗАЦИИ.csv',
            'result': 'IV. Число ИТОГА ЖИЗНИ.csv',
            'arkani': 'Аркані.csv'
        }

        for key, filename in files.items():
            if not os.path.exists(filename):
                print(f"⚠️ Пропуск: файл {filename} не найден.")
                continue

            enc = detect_encoding(filename)
            print(f"📖 Читаю {filename}...")

            # Читаем CSV
            df = pd.read_csv(filename, header=None, encoding=enc, sep=None, engine='python')

            current_num = None
            for _, row in df.iterrows():
                # Проверяем первую колонку на наличие номера (1, 2, 3...)
                first_val = str(row[0]).strip().split('.')[0]

                if first_val.isdigit():
                    current_num = first_val

                if current_num in vault:
                    if key == 'arkani':
                        # Для Арканов распределяем колонки (проверь порядок в своем CSV!)
                        vault[current_num]['title'] = clean_text(row[1])
                        # Если в твоем файле "Аркани" есть больше колонок - добавь их тут
                    else:
                        # Накапливаем текст для основных блоков
                        row_content = " ".join([clean_text(c) for c in row[1:] if clean_text(c)])
                        vault[current_num][key] += row_content + "\n"

        print("💾 Интеграция данных в модель Genesis...")

        # Карта планет для Чисел Судьбы (1-9)
        planets_map = {
            "1": "Солнце", "2": "Луна", "3": "Юпитер", "4": "Раху", "5": "Меркурий",
            "6": "Венера", "7": "Кету", "8": "Сатурн", "9": "Марс"
        }

        for num, data in vault.items():
            # Если данных нет совсем - создаем пустую запись, чтобы потом через админку наполнить
            arc = ArchetypeContent(
                number=num,
                title=data['title'] or f"Архетип {num}",
                mind_power=data['mind'].strip(),
                action_power=data['action'].strip(),
                realization=data['real'].strip(),
                life_result=data['result'].strip(),
                shadow_side=data['shadow'],
                growth_point=data['growth'],
                planet=planets_map.get(num, ""),
                cycle="",  # Эти поля пока пустые, их наполнишь через админку
                karmic_tasks="",
                exit_minus=""
            )
            db.session.add(arc)

        db.session.commit()
        print("✅ БАЗА ОБНОВЛЕНА. Теперь можно заходить в админку и вставлять 'Циклы' и 'Задачи'.")


if __name__ == "__main__":
    seed_database()