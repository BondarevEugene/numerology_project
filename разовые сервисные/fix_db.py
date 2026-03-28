import sqlite3

conn = sqlite3.connect('genesis_v2.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE archetype_content ADD COLUMN dharma TEXT")
    print("Поле dharma успешно добавлено!")
except sqlite3.OperationalError:
    print("Поле dharma уже существует.")

conn.commit()
conn.close()

'''добавление разово колонки в БД Дхарма для расчета данного поля
Как проверить, что всё заработало:
Открой сайт.
Нажми на значок ✺ в углу.
Выбери любой Архетип в выпадающем списке.
В списке полей теперь обязательно появится Дхарма (Долг Души).
'''

