"""
===============================================================================
 GENESIS HR®
 GEN-OS
 FILE  providers/esco_provider.py
 ----
 BUILD  0.2.1
 -----
 DESCRIPTION  ESCO Dataset Provider.
 -----------
 Supports:
    • ESCO Dataset v1.2.1+
    • CSV datasets
    • Manifest generation
    • Validation
    • Loading
===============================================================================
"""

from __future__ import annotations

import csv
import logging

from pathlib import Path
from typing import Iterator

from providers.base_provider import ResourceProvider
from services.archive_service import ArchiveService

LOGGER = logging.getLogger("GEN-OS.ESCO")


class ESCOProvider(ResourceProvider):
    """
    European Skills, Competences,
    Qualifications and Occupations Provider.
    """

    DATASET_NAME = "esco"
    REQUIRED_FILES = (
        "occupations_en.csv",
        "skills_en.csv",
        "occupationSkillRelations_en.csv",
    )

    def __init__(
            self,
            dataset_root: Path
    ) -> None:
        super().__init__(dataset_root)

    # -----------------------------------------------------------------

    @property
    def name(self) -> str:
        return self.DATASET_NAME

    # -----------------------------------------------------------------

    @property
    def version(self) -> str:
        manifest = self.root / "manifest.json"
        if not manifest.exists():
            return "unknown"
        import json
        data = json.loads(
            manifest.read_text(
                encoding="utf-8"
            )
        )
        return data.get(
            "version",
            "unknown"
        )

    # -----------------------------------------------------------------

    def discover(self) -> bool:
        """
        Dataset exists?
        """
        return ArchiveService.exists(
            self.root
        )

    # -----------------------------------------------------------------

    def install(self) -> None:
        """
        Install ESCO dataset.
        """
        ArchiveService.install(
            self.root
        )

    # -----------------------------------------------------------------

    def validate(self) -> bool:
        """
        Validate ESCO structure.
        """
        return ArchiveService.require(
            self.root,
            *self.REQUIRED_FILES
        )

    # -----------------------------------------------------------------

    def metadata(self) -> dict:
        data = ArchiveService.summary(self.root)
        data["provider"] = self.name
        data["version"] = self.version
        return data

    # -----------------------------------------------------------------

    def load(self) -> dict:
        """
        Load complete ESCO dataset.

        Returns
        -------
        dict
        """
        return {
            "occupations": self.occupations(),
            "skills": self.skills(),
            "relations": self.relations()
        }

    # -----------------------------------------------------------------

    def statistics(self) -> dict:
        return {**self.info(), "occupations": self.count_occupations(), "skills": self.count_skills(),
                "relations": self.count_relations()}

    # -----------------------------------------------------------------

    def csv_file(
            self,
            filename: str
    ) -> Path:
        """
        Locate CSV inside extracted dataset.
        """
        return self.file(filename)

    # -----------------------------------------------------------------

    def csv_reader(
            self,
            filename: str
    ) -> Iterator[dict]:
        """
        Streaming CSV reader.
        """
        with self.csv_file(
                filename
        ).open(
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as stream:
            reader = csv.DictReader(
                stream
            )
            for row in reader:
                yield row

    # -----------------------------------------------------------------

    def occupations(
            self
    ) -> Iterator[dict]:
        """
        Occupation iterator.
        """
        yield from self.csv_reader(
            "occupations_en.csv"
        )

    # -----------------------------------------------------------------

    def skills(
            self
    ) -> Iterator[dict]:
        """
        Skills iterator.
        """
        yield from self.csv_reader("skills_en.csv")

    # -----------------------------------------------------------------

    def relations(
            self
    ) -> Iterator[dict]:
        """
        Occupation-Skill iterator.
        """
        yield from self.csv_reader(
            "occupationSkillRelations_en.csv"
        )

    # -----------------------------------------------------------------

    def count_occupations(
            self
    ) -> int:
        return sum(1 for _ in self.occupations())

    # -----------------------------------------------------------------

    def count_skills(
            self
    ) -> int:
        return sum(1 for _ in self.skills())

    # -----------------------------------------------------------------

    def count_relations(self) -> int:
        return sum(1 for _ in self.relations())

    # -----------------------------------------------------------------

    def profession_rows(self):
        """
        Alias for occupation records.
        Used by ProfessionRepository.
        """

        yield from self.occupations()

    # -----------------------------------------------------------------

    def skill_rows(self):
        """
        Alias for skill records.
        Used by SkillRepository.
        """

        yield from self.skills()

    # -----------------------------------------------------------------

    def relation_rows(self):
        """
        Alias for relation records.

        Used by GraphBuilder.
        """

        yield from self.relations()

    # -----------------------------------------------------------------

    def healthcheck(self) -> dict:
        """
        Provider diagnostic.
        """

        return {
            "provider": self.name,
            "version": self.version,
            "available": self.discover(),
            "valid": self.validate(),
            "statistics": self.statistics()
        }

    # -----------------------------------------------------------------

    def initialize(self) -> None:
        """
        Complete provider initialization.
        """

        LOGGER.info(
            "Initializing ESCO provider..."
        )

        if not self.discover():
            raise FileNotFoundError(

                "ESCO dataset not found."

            )

        self.install()

        if not self.validate():
            raise RuntimeError(

                "ESCO validation failed."

            )

        LOGGER.info(
            "ESCO provider READY."
        )

    # -----------------------------------------------------------------

    def __repr__(self) -> str:
        return ("<ESCOProvider " f"version='{self.version}'>"
                )
