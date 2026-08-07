"""
===============================================================

GEN-OS

Dataset Loader

Universal loader for:

    CSV
    XLSX
    JSON
    XML
    SQL
    ZIP

===============================================================
"""

from __future__ import annotations

import csv
import json
import sqlite3
import zipfile
from pathlib import Path
from typing import Any
from typing import Iterable

import pandas as pd


class DatasetLoader:

    """
    Universal dataset loader.
    """

    # ---------------------------------------------------------

    def exists(
        self,
        path: str | Path
    ) -> bool:

        return Path(path).exists()

    # ---------------------------------------------------------

    def extension(
        self,
        path: str | Path
    ) -> str:

        return Path(path).suffix.lower()

    # ---------------------------------------------------------

    def load_csv(
        self,
        path: str | Path
    ) -> list[dict]:

        with open(
            path,
            encoding="utf-8",
            newline=""
        ) as fp:

            return list(

                csv.DictReader(fp)

            )

    # ---------------------------------------------------------

    def load_json(
        self,
        path: str | Path
    ) -> Any:

        with open(

            path,

            encoding="utf-8"

        ) as fp:

            return json.load(fp)

    # ---------------------------------------------------------

    def load_excel(
        self,
        path: str | Path
    ) -> list[dict]:

        frame = pd.read_excel(path)

        return frame.to_dict(
            orient="records"
        )

    # ---------------------------------------------------------

    def load_sql(
        self,
        database: str | Path,
        query: str
    ) -> list[dict]:

        connection = sqlite3.connect(
            database
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.execute(
            query
        )

        rows = [

            dict(row)

            for row in cursor.fetchall()

        ]

        connection.close()

        return rows
    # ---------------------------------------------------------

    def load_xml(
        self,
        path: str | Path
    ):
        """
        Parse XML document.

        Returns ElementTree root.
        """

        import xml.etree.ElementTree as ET

        tree = ET.parse(path)

        return tree.getroot()

    # ---------------------------------------------------------

    def open_zip(
        self,
        path: str | Path
    ) -> zipfile.ZipFile:
        """
        Open ZIP archive.
        """

        return zipfile.ZipFile(
            path,
            "r"
        )

    # ---------------------------------------------------------

    def zip_members(
        self,
        path: str | Path
    ) -> list[str]:
        """
        List archive content.
        """

        with zipfile.ZipFile(path) as archive:

            return archive.namelist()

    # ---------------------------------------------------------

    def extract_zip(
        self,
        archive_path: str | Path,
        destination: str | Path
    ) -> list[Path]:
        """
        Extract ZIP archive.
        """

        destination = Path(destination)

        destination.mkdir(
            parents=True,
            exist_ok=True
        )

        extracted = []

        with zipfile.ZipFile(
            archive_path,
            "r"
        ) as archive:

            archive.extractall(destination)

            for member in archive.namelist():

                extracted.append(

                    destination / member

                )

        return extracted

    # ---------------------------------------------------------

    def detect(
        self,
        path: str | Path
    ) -> str:
        """
        Detect dataset type.
        """

        ext = self.extension(path)

        mapping = {

            ".csv": "csv",

            ".xlsx": "excel",

            ".xls": "excel",

            ".json": "json",

            ".xml": "xml",

            ".zip": "zip",

            ".db": "sqlite",

            ".sqlite": "sqlite",

            ".sql": "sql"

        }

        return mapping.get(

            ext,

            "unknown"

        )

    # ---------------------------------------------------------

    def load(
        self,
        path: str | Path,
        **kwargs
    ):
        """
        Universal loader.
        """

        kind = self.detect(path)

        if kind == "csv":

            return self.load_csv(path)

        if kind == "json":

            return self.load_json(path)

        if kind == "excel":

            return self.load_excel(path)

        if kind == "xml":

            return self.load_xml(path)

        if kind == "zip":

            return self.open_zip(path)

        if kind == "sqlite":

            query = kwargs.get(

                "query",

                "SELECT * FROM sqlite_master"

            )

            return self.load_sql(

                path,

                query

            )

        raise ValueError(

            f"Unsupported dataset: {path}"

        )

    # ---------------------------------------------------------

    def preview(
        self,
        records: Iterable,
        limit: int = 5
    ) -> list:
        """
        Preview first rows.
        """

        result = []

        for index, item in enumerate(records):

            if index >= limit:

                break

            result.append(item)

        return result

        # ---------------------------------------------------------

        def statistics(
                self,
                records: list[dict]
        ) -> dict:
            """
            Dataset statistics.
            """

            if not records:
                return {

                    "rows": 0,

                    "columns": 0,

                    "fields": []

                }

            return {

                "rows": len(records),

                "columns": len(records[0]),

                "fields": list(

                    records[0].keys()

                )

            }

        # ---------------------------------------------------------

        def find_files(
                self,
                directory: str | Path,
                extension: str
        ) -> list[Path]:
            """
            Find files recursively.
            """

            directory = Path(directory)

            extension = extension.lower()

            return sorted(

                directory.rglob(

                    f"*{extension}"

                )

            )

        # ---------------------------------------------------------

        def safe_load(
                self,
                path: str | Path,
                **kwargs
        ):
            """
            Safe loading.
            """

            try:

                return self.load(

                    path,

                    **kwargs

                )

            except Exception as exc:

                print(

                    f"[DatasetLoader] {exc}"

                )

                return None

        # ---------------------------------------------------------

        def describe(
                self,
                path: str | Path
        ) -> dict:
            """
            Dataset description.
            """

            path = Path(path)

            return {

                "name": path.name,

                "suffix": path.suffix,

                "size": path.stat().st_size,

                "exists": path.exists(),

                "type": self.detect(path)

            }

        # ---------------------------------------------------------

        def __repr__(self):

            return (

                "<DatasetLoader>"

            )

    # ============================================================
    # GLOBAL SINGLETON
    # ============================================================

    dataset_loader = DatasetLoader()
