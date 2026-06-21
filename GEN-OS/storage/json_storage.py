"""
==========================================================
GENESIS HR®
JSON Storage
Version:1.0

Description: Файловое хранилище Registry.
==========================================================
"""

import json
from pathlib import Path

from .storage import Storage


class JsonStorage(Storage):

    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(self, entity):
        folder = self.root / entity.entity_type.value
        folder.mkdir(
            parents=True,
            exist_ok=True
        )
        filename = folder / f"{entity.slug}.json"
        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                entity.to_dict(),
                f,
                ensure_ascii=False,
                indent=4
            )

    def load(self, entity_id):
        raise NotImplementedError

    def delete(self, entity_id):
        raise NotImplementedError

    def exists(self, entity_id):
        raise NotImplementedError

    def list(self, entity_type):
        folder = self.root / entity_type.value
        if not folder.exists():
            return []
        return list(folder.glob("*.json"))

    def statistics(self):
        result = {}
        for folder in self.root.iterdir():
            if folder.is_dir():
                result[folder.name] = len(
                    list(folder.glob("*.json"))
                )
        return result
