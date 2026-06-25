"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Excel Mapper
BUILD:0072
DESCRIPTION
Сопоставление колонок
Excel
с Entity.

═══════════════════════════════════════════════════════════════════════
"""


class ExcelMapper:
    DEFAULT_MAPPING = {
        "title":
            "title",
        "category":
            "category",
        "description":
            "description",
        "code":
            "code"
    }

    @classmethod
    def mapping(cls):
        return cls.DEFAULT_MAPPING
