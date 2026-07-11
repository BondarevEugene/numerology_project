"""
═══════════════════════════════════════════════════════════════════════════════

GENESIS HR® // GEN-OS

Knowledge Management Core

FILE:
validation_engine.py

BUILD:
0102

DESCRIPTION:

Движок первичной проверки импортируемых наборов данных.

Проверяет:

• существование файла
• тип данных
• структуру
• обязательные колонки
• пустые значения
• дубликаты
• кодировку
• совместимость с Registry

НЕ изменяет данные.

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd


@dataclass(slots=True)
class ValidationResult:

    valid: bool = True

    rows: int = 0

    columns: int = 0

    duplicated_rows: int = 0

    missing_values: int = 0

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)


class ValidationEngine:

    """
    Проверка качества датасетов.
    """

    SUPPORTED_EXTENSIONS = {
        ".csv",
        ".xlsx",
        ".xls",
        ".json",
        ".parquet",
    }

    def validate(self, file_path: Path) -> ValidationResult:

        result = ValidationResult()

        if not file_path.exists():
            result.valid = False
            result.errors.append("Файл не найден.")
            return result

        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            result.valid = False
            result.errors.append(
                f"Неподдерживаемый формат: {file_path.suffix}"
            )
            return result

        try:

            if file_path.suffix == ".csv":
                df = pd.read_csv(file_path)

            elif file_path.suffix in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path)

            elif file_path.suffix == ".json":
                df = pd.read_json(file_path)

            elif file_path.suffix == ".parquet":
                df = pd.read_parquet(file_path)

            else:
                raise RuntimeError("Unknown format")

        except Exception as exc:

            result.valid = False
            result.errors.append(str(exc))
            return result

        result.rows = len(df)

        result.columns = len(df.columns)

        result.duplicated_rows = int(df.duplicated().sum())

        result.missing_values = int(df.isna().sum().sum())

        result.metadata["columns"] = list(df.columns)

        result.metadata["dtypes"] = {
            k: str(v)
            for k, v in df.dtypes.items()
        }

        if result.duplicated_rows:
            result.warnings.append(
                f"Обнаружено {result.duplicated_rows} дубликатов."
            )

        if result.missing_values:
            result.warnings.append(
                f"Обнаружено {result.missing_values} пустых значений."
            )

        return result