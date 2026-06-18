import sqlite3

db_path = r"instance\genesis_v2.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\nТАБЛИЦЫ:\n")

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

tables = cursor.fetchall()

for table in tables:
    print(table[0])

print("\n------------------\n")

for table in tables:

    table_name = table[0]

    try:
        cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        )

        count = cursor.fetchone()[0]

        print(
            f"{table_name}: {count} записей"
        )

    except Exception as e:
        print(
            f"{table_name}: ERROR {e}"
        )

conn.close()