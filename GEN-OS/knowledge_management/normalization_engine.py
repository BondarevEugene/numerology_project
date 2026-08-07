"""
═══════════════════════════════════════════════════════════════════════════════
GENESIS HR® // GEN-OS

Knowledge Management Core

FILE:
normalization_engine.py

BUILD:
0103

DESCRIPTION:

Нормализация импортируемых знаний.

Отвечает за:

• очистку строк
• нормализацию регистра
• удаление лишних пробелов
• унификацию значений
• поиск синонимов
• канонизацию сущностей

ВАЖНО

НЕ записывает данные в Registry.

НЕ строит Graph.

НЕ изменяет Import Session.

Только подготавливает знания.

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import re

import pandas as pd


class NormalizationEngine:

    """
    Унификация знаний.
    """

    def normalize_dataframe(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        df = dataframe.copy()

        for column in df.columns:

            if df[column].dtype == object:

                df[column] = (
                    df[column]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    .str.replace(r"\s+", " ", regex=True)
                )

        return df

    def normalize_text(self, value: str) -> str:

        if not value:
            return ""

        value = value.strip()

        value = re.sub(r"\s+", " ", value)

        return value

    def normalize_skill(self, value: str) -> str:

        value = self.normalize_text(value)

        synonyms = {

            "python3": "Python",

            "python 3": "Python",

            "py": "Python",

            "js": "JavaScript",

            "javascript": "JavaScript",

            "node js": "Node.js",

            "nodejs": "Node.js",

            "c sharp": "C#",

            "c-sharp": "C#"

        }

        key = value.lower()

        return synonyms.get(key, value)

    def normalize_profession(self, value: str) -> str:

        value = self.normalize_text(value)

        return value.title()

    def normalize_column(
        self,
        dataframe: pd.DataFrame,
        column_name: str
    ) -> pd.DataFrame:

        if column_name not in dataframe.columns:

            return dataframe

        dataframe[column_name] = dataframe[column_name].apply(

            self.normalize_text

        )

        return dataframe
