from sqlalchemy import create_engine
from sqlalchemy import inspect

DATABASE_URL = "postgresql://neondb_owner:npg_EFN09eZPMqai@ep-damp-math-al92xna7-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)

inspector = inspect(engine)

print("\nТАБЛИЦЫ:\n")

for table in inspector.get_table_names():

    print(f"\n{'=' * 60}")
    print(table)
    print('=' * 60)

    columns = inspector.get_columns(table)

    for column in columns:

        print(
            f"{column['name']} | {column['type']}"
        )