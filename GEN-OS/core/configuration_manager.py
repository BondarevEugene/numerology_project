"""
═══════════════════════════════════════════════════════════════════════════════

 GENESIS HR® // OMNIFACTORY EVO
 GEN-OS Platform
 FILE:    configuration_manager.py
 BUILD:     0402
 DESCRIPTION
 Unified configuration loader for every GEN-OS subsystem.
 No module should access JSON files directly.

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any


class ConfigurationManager:

    def __init__(self, config_root: Path):
        self.config_root = config_root
        self._cache: dict[str, Any] = {}

    # ----------------------------------------------------------

    def load(self, relative_path: str):
        path = self.config_root / relative_path
        if relative_path in self._cache:
            return self._cache[relative_path]
        with open(path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        self._cache[relative_path] = data
        return data

    # ----------------------------------------------------------

    def save(self, relative_path: str, data):
        path = self.config_root / relative_path
        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        with open(
            path,
            "w",
            encoding="utf-8"
        ) as fp:
            json.dump(
                data,
                fp,
                indent=4,
                ensure_ascii=False
            )
        self._cache[relative_path] = data

    # ----------------------------------------------------------

    def clear_cache(self):
        self._cache.clear()
