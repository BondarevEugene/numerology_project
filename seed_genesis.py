import pandas as pd
import os
import chardet
from app import app, db, ArchetypeContent


def detect_encoding(file_path):
    """Определяет кодировку файла (UTF-8, CP1251 и т.д.)"""
    with open(file_path, 'rb') as f:
        rawdata = f.read(20000)
    return chardet.detect(rawdata)['encoding']


def clean_text(text):
    """Очистка текста от мусора Excel"""
    if pd.isna(text): return ""
    return str(text).replace("_x000D_", "").strip()


def seed_database():
    with app.app_context():
        print("🌀 Очистка базы данных...")
        db.drop_all()
        db.create_all()

        # Создаем хранилище для данных (числа от 1 до 22)
        vault = {str(i): {
            "mind": "", "action": "", "real": "", "result": "",
            "title": "", "strength": "", "shadow": "", "growth": ""
        } for i in range(1, 23)}

        files = {
            'mind': 'I. Число УМА.csv',
            'action': 'II. Число ДЕЙСТВИЯ.csv',
            'real': 'III. Число РЕАЛИЗАЦИИ.csv',
            'result': 'IV. Число ИТОГА ЖИЗНИ.csv',
            'arkani': 'Аркані.csv'
        }

        for key, filename in files.items():
            if not os.path.exists(filename):
                print(f"❌ Файл не найден: {filename}")
                continue

            enc = detect_encoding(filename)
            print(f"📖 Читаю {filename} (кодировка: {enc})...")

            # Читаем CSV с автоматическим определением разделителя (, или ;)
            df = pd.read_csv(filename, header=None, encoding=enc, sep=None, engine='python')

            current_num = None
            for _, row in df.iterrows():
                first_val = str(row[0]).strip().split('.')[0]  # Чистим "1.0" -> "1"

                if first_val.isdigit():
                    current_num = first_val

                if current_num in vault:
                    if key == 'arkani':
                        # Структура: 0-№, 1-Название, 2-Сила, 3-Тень, 4-Рост
                        vault[current_num]['title'] = clean_text(row[1])
                        vault[current_num]['strength'] = clean_text(row[2])
                        vault[current_num]['shadow'] = clean_text(row[3])
                        vault[current_num]['growth'] = clean_text(row[4])
                    else:
                        # Склеиваем весь текст в строке после номера
                        row_content = " ".join([clean_text(c) for c in row[1:] if clean_text(c)])
                        vault[current_num][key] += row_content + " "

        print("💾 Сохранение в базу данных...")
        planets_map = {
            "1": "Солнце", "2": "Луна", "3": "Юпитер", "4": "Раху", "5": "Меркурий",
            "6": "Венера", "7": "Кету", "8": "Сатурн", "9": "Марс"
        }

        for num, data in vault.items():
            if not data['title'] and not data['mind']: continue

            # Настройка соответствия полей модели
            arc = ArchetypeContent(
                number=num,
                title=data['title'] or f"Архетип {num}",
                mind_power=data['mind'].strip(),
                action_power=data['action'].strip(),
                realization=data['real'].strip(),
                life_result=data['result'].strip(),
                # Добавляем планеты и векторы силы, которые пропали
                power_vector=data['strength'],
                shadow_side=data['shadow'],
                growth_point=data['growth']
            )
            db.session.add(arc)

        db.session.commit()
        print("✅ База Genesis готова. Текст теперь читаем!")


if __name__ == "__main__":
    seed_database()