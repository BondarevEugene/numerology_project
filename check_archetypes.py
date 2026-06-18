import sqlite3

conn = sqlite3.connect(
    r"instance\genesis_v2.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT *
FROM archetype_content
LIMIT 3
""")

rows = cursor.fetchall()

for row in rows:
    print()
    print("=" * 80)
    print(row)

conn.close()