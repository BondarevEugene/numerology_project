"""
====================================================
Genesis Import Engine
Universal Import Pipeline
====================================================
"""

from pathlib import Path

from .registry import IMPORT_SOURCES
from .validator import ImportValidator
from .mapper import COLUMN_MAPPING
from .preview import ImportPreview
from .processor import ProfessionProcessor

from .excel import ExcelImporter
from .csv import CsvImporter

from models import db


class ImportEngine:

    READERS = {
        ".xlsx": ExcelImporter,
        ".xls": ExcelImporter,
        ".csv": CsvImporter
    }
    @classmethod
    def run(cls, path):
        extension = Path(path).suffix.lower()
        if extension not in cls.READERS:
            raise Exception(
                f"Unsupported format {extension}"
            )
        reader = cls.READERS[extension]
        rows = reader.read(path)
        preview = ImportPreview.build(rows)
        imported = 0
        failed = 0

        for row in rows:

            mapped = {}
            for key, value in row.items():
                mapped_key = COLUMN_MAPPING.get(
                    key,
                    key
                )
                mapped[mapped_key] = value
            errors = ImportValidator.validate_columns_from_dict(
                mapped
            )
            if errors:
                failed += 1
                continue
            profession = ProfessionProcessor.create(
                mapped
            )
            db.session.add(
                profession
            )
            imported += 1
        db.session.commit()
        return {
            "preview":preview,
            "imported":imported,
            "failed":failed
        }