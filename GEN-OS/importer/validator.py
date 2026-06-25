"""
====================================================
Genesis HR® Intelligence Platform
IMPORT REGISTRY
Version : 1.0
====================================================

Регистрирует все поддерживаемые источники данных.
Любой новый источник подключается
без изменения Import Engine.

====================================================
"""

IMPORT_SOURCES = {

    "excel": {
        "title": "Microsoft Excel",
        "extensions": [
            ".xlsx",
            ".xls"
        ],
        "enabled": True
    },

    "csv": {
        "title": "CSV",
        "extensions": [
            ".csv"
        ],
        "enabled": True
    },

    "esco": {
        "title": "ESCO API",
        "enabled": False
    },

    "onet": {
        "title": "O*NET API",
        "enabled": False
    }

}


############### Это новый метод. Он остается на уровне со старым #########
@classmethod
def validate_columns_from_dict(cls, row):
    errors = []
    for field in cls.REQUIRED_COLUMNS:

        if not row.get(field):
            errors.append(field)

    return errors
