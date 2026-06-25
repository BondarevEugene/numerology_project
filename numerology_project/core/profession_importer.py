import pandas as pd

from models import (
    Profession,
    db
)

from core.import_validator import (
    ImportValidator
)


class ProfessionImporter:
    @staticmethod
    def import_excel(path):
        df = pd.read_excel(path)
        imported = 0
        failed = 0
        for _, row in df.iterrows():
            data = row.to_dict()
            errors = (
                ImportValidator
                .validate_profession(
                    data
                )
            )
            if errors:
                failed += 1
                continue
            profession = Profession(

                title=title,
                title_ru=data.get(
                    "title_ru"
                ),
                title_ua=data.get(
                    "title_ua"
                ),
                description=data.get(
                    "description"
                ),
                category=data.get(
                    "category"
                ),
                subcategory=data.get(
                    "subcategory"
                ),
                keywords=data.get(
                    "keywords"
                ),
                category_group=data.get(
                    "category_group"
                ),
                source="excel",
                status="imported"
            )
            db.session.add(
                profession
            )
            imported += 1
        db.session.commit()
        return {
            "imported":
                imported,
            "failed":
                failed
        }