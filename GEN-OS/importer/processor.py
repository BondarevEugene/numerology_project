"""
Processor
Создает объекты Profession
после нормализации данных.
"""


from models import Profession


class ProfessionProcessor:

    @staticmethod
    def create(data):
        profession = Profession(
            title=data.get("title"),
            title_ru=data.get("title_ru"),
            title_ua=data.get("title_ua"),
            description=data.get("description"),
            category=data.get("category"),
            source=data.get(
                "source",
                "excel"
            ),
            status="imported"
        )

        return profession
