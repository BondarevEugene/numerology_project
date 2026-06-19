"""
═══════════════════════════════════════════════════════════════════════

GENESIS KNOWLEDGE ENGINE

MODULE    JSON Provider

MODULE ID    GKH-PROVIDER-002

VERSION    1.0.0 Alpha

LAYER    Providers

DESCRIPTION
Reads JSON datasets and returns raw objects.
This provider knows NOTHING about:
    • Entity
    • Registry
    • Parser
It simply loads JSON.

Example

professions.json
books.json
habits.json
competencies.json
═══════════════════════════════════════════════════════════════════════
"""

import json
from pathlib import Path

from .base_provider import BaseProvider


class JsonProvider(BaseProvider):
    NAME = "JSON Provider"
    VERSION = "1.0.0"

    def __init__(self, filepath):
        self.filepath = Path(filepath)

    # ==========================================================
    # LOAD
    # ==========================================================

    def load(self):
        if not self.filepath.exists():
            raise FileNotFoundError(
                f"Dataset not found:\n"
                f"{self.filepath}"
            )
        with open(
                self.filepath,
                "r",
                encoding="utf-8"
        ) as file:
            data = json.load(file)
        print()
        print("══════════════════════════════")
        print("📦 JSON Provider")
        print()
        print(f"File : {self.filepath}")
        print(f"Objects : {len(data)}")
        print()
        print("══════════════════════════════")
        return data

    # ==========================================================
    # INFO
    # ==========================================================

    def exists(self):
        return self.filepath.exists()

    def __repr__(self):
        return (
            f"<JsonProvider "
            f"{self.filepath}>"

        )
