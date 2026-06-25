"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Excel Validator
BUILD:0073
DESCRIPTION
Проверка структуры Excel.
═══════════════════════════════════════════════════════════════════════
"""


class ExcelValidator:
    REQUIRED = [
        "title"
    ]

    @classmethod
    def validate(
        cls,
        dataframe
    ):
        errors = []
        for field in cls.REQUIRED:
            if field not in dataframe.columns:
                errors.append(field)
        return errors
