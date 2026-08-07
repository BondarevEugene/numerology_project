"""
====================================================================

GENESIS HR®
O*NET Dataset Parser
BUILD 0303
DESCRIPTION
-----------

Converts raw O*NET datasets into
GEN-OS canonical format.

Input:
    SQL
    CSV
    XLSX

Output:
    profession_id
    profession_name
    skill
    importance
    level
    technology

====================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from services.dataset_loader import dataset_loader


class ONetParser:
    """
    Canonical O*NET parser.
    """
    def __init__(self):
        self._aliases = {
            "occupation": [
                "occupation",
                "occupation_title",
                "title",
                "name"
            ],
            "occupation_id": [
                "occupation_id",
                "onet_soc_code",
                "soc_code",
                "id",
                "code"
            ],
            "skill": [
                "skill",
                "element_name",
                "element",
                "commodity_title",
                "technology",
                "software"
            ],
            "importance": [
                "importance",
                "im"
            ],
            "level": [
                "level",
                "lv"
            ]
        }

    # ------------------------------------------------------------

    def value(
        self,
        row: dict,
        field: str,
        default=""
    ):
        aliases = self._aliases.get(
            field,
            []
        )
        for alias in aliases:
            if alias in row:
                value = row[alias]
                if value is None:
                    continue
                value = str(value).strip()
                if value:
                    return value
        return default

    # ------------------------------------------------------------

    def normalize(
        self,
        row: dict
    ) -> dict:
        return {
            "occupation_id":
                self.value(
                    row,
                    "occupation_id"
                ),
            "occupation":
                self.value(
                    row,
                    "occupation"
                ),
            "skill":
                self.value(
                    row,
                    "skill"
                ),
            "importance":
                self.value(
                    row,
                    "importance",
                    1
                ),
            "level":
                self.value(
                    row,
                    "level",
                    1
                )
        }

    # ------------------------------------------------------------
    # FILE PARSING
    # ------------------------------------------------------------

    def parse_records(
        self,
        records: Iterable[dict]
    ) -> list[dict]:
        """
        Normalize every record.
        """
        normalized = []
        for row in records:
            normalized.append(
                self.normalize(row)
            )
        return normalized

    # ------------------------------------------------------------

    def parse_csv(
        self,
        path: str | Path
    ) -> list[dict]:
        records = dataset_loader.load_csv(path)
        return self.parse_records(records)

    # ------------------------------------------------------------

    def parse_excel(
        self,
        path: str | Path
    ) -> list[dict]:
        records = dataset_loader.load_excel(path)
        return self.parse_records(records)

    # ------------------------------------------------------------

    def parse_json(
        self,
        path: str | Path
    ) -> list[dict]:
        records = dataset_loader.load_json(path)
        return self.parse_records(records)

    # ------------------------------------------------------------

    def parse_xml(
        self,
        path: str | Path
    ) -> list[dict]:
        """
        Generic XML parser.

        Later can be specialized
        for ESCO XML.
        """
        root = dataset_loader.load_xml(path)
        rows = []

        for child in root:
            row = {}
            for item in child:
                row[item.tag] = item.text
            rows.append(row)

        return self.parse_records(rows)

    # ------------------------------------------------------------

    def parse_file(
        self,
        path: str | Path
    ) -> list[dict]:
        kind = dataset_loader.detect(path)

        if kind == "csv":
            return self.parse_csv(path)

        if kind == "excel":
            return self.parse_excel(path)

        if kind == "json":
            return self.parse_json(path)

        if kind == "xml":
            return self.parse_xml(path)

        raise ValueError(
            f"Unsupported dataset type: {kind}"
        )

    # ------------------------------------------------------------
    # DIRECTORY PARSING
    # ------------------------------------------------------------

    def parse_directory(
        self,
        directory: str | Path
    ) -> dict:
        """
        Scan directory and parse every supported file.
        """
        directory = Path(directory)
        datasets = {}
        supported = {
            ".csv",
            ".xlsx",
            ".xls",
            ".xml",
            ".json"
        }

        for file in sorted(directory.rglob("*")):
            if file.suffix.lower() not in supported:
                continue

            try:
                datasets[file.stem] = self.parse_file(file)
            except Exception as exc:
                print(
                    f"[ONetParser] "
                    f"{file.name}: {exc}"
                )

        return datasets

    # ------------------------------------------------------------
    # ZIP SUPPORT
    # ------------------------------------------------------------

    def parse_archive(
        self,
        archive: str | Path,
        destination: str | Path
    ) -> dict:
        """
        Extract archive and parse
        every supported dataset.
        """
        dataset_loader.extract_zip(
            archive,
            destination
        )
        return self.parse_directory(destination)

    # ------------------------------------------------------------
    # O*NET DETECTION
    # ------------------------------------------------------------

    def detect_dataset_type(
        self,
        filename: str
    ) -> str:
        name = filename.lower()

        if "occupation" in name:
            return "professions"
        if "software" in name:
            return "software"
        if "essential" in name:
            return "essential"
        if "transferable" in name:
            return "transferable"
        if "technology" in name:
            return "technology"
        if "skill" in name:
            return "skills"
        if "task" in name:
            return "tasks"
        if "ability" in name:
            return "abilities"

        return "unknown"

    # ------------------------------------------------------------

    def classify(
        self,
        datasets: dict
    ) -> dict:
        """
        Convert parsed files into
        canonical O*NET groups.
        """
        result = {
            "professions": [],
            "software": [],
            "essential": [],
            "transferable": [],
            "skills": [],
            "tasks": [],
            "abilities": []
        }

        for filename, rows in datasets.items():
            dataset_type = self.detect_dataset_type(filename)
            if dataset_type == "unknown":
                continue

            result.setdefault(
                dataset_type,
                []
            )
            result[dataset_type].extend(rows)

        return result

    # ------------------------------------------------------------

    def summary(
        self,
        datasets: dict
    ) -> dict:
        """
        Dataset statistics.
        """
        stats = {}
        for name, rows in datasets.items():
            stats[name] = {
                "rows": len(rows)
            }
        return stats

    # ------------------------------------------------------------
    # VALIDATION (ВЫРОВНЕН СКОУП МЕТОДА К КЛАССУ ONetParser)
    # ------------------------------------------------------------

    def validate(
        self,
        datasets: dict
    ) -> dict:
        """
        Validate normalized datasets.
        Returns: {"valid": bool, "errors": [], "warnings": []}
        """
        report = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        for dataset_name, rows in datasets.items():
            if not rows:
                report["warnings"].append(
                    f"{dataset_name}: empty"
                )
                continue

            for index, row in enumerate(rows):
                if not row.get("occupation_id"):
                    report["errors"].append(
                        f"{dataset_name}[{index}] missing occupation_id"
                    )
                    report["valid"] = False

                if dataset_name != "professions":
                    if not row.get("skill"):
                        report["errors"].append(
                            f"{dataset_name}[{index}] missing skill"
                        )
                        report["valid"] = False

        return report

    # ------------------------------------------------------------

    def load(
        self,
        source: str
    ) -> dict:
        """
        Universal O*NET loader.

        Supports:
            folder
            zip
            csv
            excel
            json
            xml
        """
        source = Path(source)

        if source.is_dir():
            parsed = self.parse_directory(source)
        elif source.suffix.lower() == ".zip":
            parsed = self.parse_archive(
                source,
                source.parent / "_extract"
            )
        else:
            parsed = {
                source.stem: self.parse_file(source)
            }

        datasets = self.classify(parsed)
        validation = self.validate(datasets)

        return {
            "datasets": datasets,
            "statistics": self.summary(datasets),
            "validation": validation
        }

    # ------------------------------------------------------------

    def __repr__(self):
        return "<ONetParser>"


# ============================================================
# GLOBAL SINGLETON (ВЫНЕСЕН ИЗ СКОУПА КЛАССА В МОДУЛЬ)
# ============================================================

onet_parser = ONetParser()

# ==============================================================
# END OF FILE // OMNIFACTORY LABS COGNITIVE REPOSITORY SPEC
# ==============================================================
