"""
===============================================================================
 GENESIS HR®
 GEN-OS
 FILE ---- providers/onet_provider.py
 BUILD ----- 0.2.1
 DESCRIPTION ----------- O*NET Database Provider.
 Supports
    • O*NET 30+
    • TXT datasets
    • Streaming readers
    • Validation
===============================================================================
"""

from __future__ import annotations

import csv
import json
import logging

from pathlib import Path
from typing import Iterator

from providers.base_provider import ResourceProvider
from services.archive_service import ArchiveService

LOGGER = logging.getLogger("GEN-OS.ONET")


class ONETProvider(ResourceProvider):
    """
    O*NET occupational database provider.
    """
    DATASET_NAME = "onet"
    REQUIRED_FILES = (
        "Occupation Data.txt",
        "Skills.txt",
        "Knowledge.txt",
        "Abilities.txt",
        "Task Statements.txt",
    )

    def __init__(self, dataset_root: Path) -> None:
        super().__init__(dataset_root)

    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        return self.DATASET_NAME

    # ------------------------------------------------------------------

    @property
    def version(self) -> str:
        manifest = self.root / "manifest.json"
        if not manifest.exists():
            return "unknown"
        data = json.loads(
            manifest.read_text(
                encoding="utf-8"
            )
        )
        return data.get("version", "unknown")

    # ------------------------------------------------------------------

    def discover(self) -> bool:
        return ArchiveService.exists(self.root)

    # ------------------------------------------------------------------

    def install(self) -> None:
        ArchiveService.install(self.root)

    # ------------------------------------------------------------------

    def validate(self) -> bool:
        return ArchiveService.require(self.root, *self.REQUIRED_FILES)

    # ------------------------------------------------------------------

    def metadata(self) -> dict:
        metadata = ArchiveService.summary(self.root)
        metadata["provider"] = self.name
        metadata["version"] = self.version
        return metadata

    # ------------------------------------------------------------------

    def txt_file(self, filename: str) -> Path:
        return self.file(filename)

    # ------------------------------------------------------------------

    def reader(self, filename: str) -> Iterator[dict]:
        """
        Stream TAB-separated O*NET files.
        """

        with self.txt_file(filename).open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(
                stream,
                delimiter="\t"
            )
            yield from reader
    # ------------------------------------------------------------------

    def occupations(self) -> Iterator[dict]:
        """
        Occupation Data.txt
        """
        yield from self.reader(
            "Occupation Data.txt"
        )

    # ------------------------------------------------------------------

    def skills(self) -> Iterator[dict]:
        """
        Skills.txt
        """
        yield from self.reader(
            "Skills.txt"
        )

    # ------------------------------------------------------------------

    def knowledge(self) -> Iterator[dict]:
        """
        Knowledge.txt
        """
        yield from self.reader(
            "Knowledge.txt"
        )

    # ------------------------------------------------------------------

    def abilities(self) -> Iterator[dict]:
        """
        Abilities.txt
        """
        yield from self.reader(
            "Abilities.txt"
        )

    # ------------------------------------------------------------------

    def task_statements(self) -> Iterator[dict]:
        """
        Task Statements.txt
        """
        yield from self.reader(
            "Task Statements.txt"
        )

    # ------------------------------------------------------------------

    def load(self) -> dict:
        """
        Load complete O*NET dataset.
        """
        LOGGER.info(
            "Loading O*NET dataset..."
        )

        return {
            "occupations": list(
                self.occupations()
            ),
            "skills": list(
                self.skills()
            ),
            "knowledge": list(
                self.knowledge()
            ),
            "abilities": list(
                self.abilities()
            ),
            "tasks": list(
                self.task_statements()
            )
        }

    # ------------------------------------------------------------------

    def count(self, iterator: Iterator[dict]) -> int:
        return sum(1 for _ in iterator)

    # ------------------------------------------------------------------

    def statistics(self) -> dict:
        return {
            **self.info(),
            "occupations":
                self.count(
                    self.occupations()
                ),
            "skills":
                self.count(
                    self.skills()
                ),
            "knowledge":
                self.count(
                    self.knowledge()
                ),
            "abilities":
                self.count(
                    self.abilities()
                ),
            "tasks":
                self.count(
                    self.task_statements()
                )

        }    # ------------------------------------------------------------------

    def occupation_rows(self) -> Iterator[dict]:
        """
        Repository alias.
        """
        yield from self.occupations()

    # ------------------------------------------------------------------

    def skill_rows(self) -> Iterator[dict]:
        """
        Repository alias.
        """
        yield from self.skills()

    # ------------------------------------------------------------------

    def knowledge_rows(self) -> Iterator[dict]:
        """
        Repository alias.
        """
        yield from self.knowledge()

    # ------------------------------------------------------------------

    def ability_rows(self) -> Iterator[dict]:
        """
        Repository alias.
        """
        yield from self.abilities()

    # ------------------------------------------------------------------

    def task_rows(self) -> Iterator[dict]:
        """
        Repository alias.
        """
        yield from self.task_statements()

    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """
        Complete initialization.
        """

        LOGGER.info(
            "Initializing O*NET provider..."
        )
        if not self.discover():
            raise FileNotFoundError(
                "O*NET dataset not found."
            )
        self.install()
        if not self.validate():
            raise RuntimeError(
                "O*NET validation failed."
            )
        LOGGER.info(
            "O*NET provider READY."
        )

    # ------------------------------------------------------------------

    def dataset_summary(self) -> dict:
        """
        Lightweight dataset summary.
        """
        stats = self.statistics()
        return {
            "provider": self.name,
            "version": self.version,
            "entities": (
                stats["occupations"] +
                stats["skills"] +
                stats["knowledge"] +
                stats["abilities"] +
                stats["tasks"]
            ),
            "statistics": stats
        }

    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            "<ONETProvider "
            f"version='{self.version}'>"
        )

# ==============================================================================
# FACTORY
# ==============================================================================


def create_onet_provider(
    dataset_root: Path
) -> ONETProvider:
    """
    Factory helper.
    """
    return ONETProvider(dataset_root)
