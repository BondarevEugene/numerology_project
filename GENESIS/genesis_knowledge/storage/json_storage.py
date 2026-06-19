"""
═══════════════════════════════════════════════════════════════════════

GENESIS KNOWLEDGE ENGINE

MODULE    JSON Storage

MODULE ID    GKH-STORAGE-001

VERSION    1.0.0 Alpha

LAYER    Storage

DESCRIPTION
Persistent storage for Genesis Registry.

Responsible for

✓ Save Registry
✓ Load Registry
✓ Backup Registry
✓ Export Registry

Does NOT

✗ Parse data
✗ Create entities
✗ Validate entities
═══════════════════════════════════════════════════════════════════════
"""

import json
from pathlib import Path

from ..registry.entity import Entity
from ..registry.entity_factory import EntityFactory
from ..schema.knowledge_schema import (
    EntityType,
    EntityStatus,
    SourceType
)


class JsonStorage:
    NAME = "Genesis JSON Storage"
    VERSION = "1.0.0"

    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, registry):
        data = []
        for entity in registry.all():
            data.append(
                entity.to_dict()
            )
        with open(
                self.filepath,
                "w",
                encoding="utf-8"
        ) as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )
        print()
        print("════════════════════════════")
        print("💾 Registry Saved")
        print()
        print(self.filepath)
        print()
        print(f"Objects : {len(data)}")
        print()
        print("════════════════════════════")

    # =====================================================
    # LOAD
    # =====================================================

    def load(self):
        if not self.filepath.exists():
            return []
        with open(
                self.filepath,
                "r",
                encoding="utf-8"
        ) as f:
            raw = json.load(f)
        entities = []
        for item in raw:
            entity = Entity(
                uuid=item["uuid"],
                type=EntityType(
                    item["type"]
                ),
                code=item["code"],
                slug=item["slug"],
                title=item["title"],
                title_ru=item.get(
                    "title_ru",
                    ""
                ),
                title_ua=item.get(
                    "title_ua",
                    ""
                ),
                aliases=item.get(
                    "aliases",
                    []
                ),
                description=item.get(
                    "description",
                    ""
                ),
                short_description=item.get(
                    "short_description",
                    ""
                ),
                category=item.get(
                    "category",
                    ""
                ),
                subcategory=item.get(
                    "subcategory",
                    ""
                ),
                tags=item.get(
                    "tags",
                    []
                ),
                source=item.get(
                    "source",
                    ""
                ),
                status=item.get(
                    "status",
                    "draft"
                ),
                language=item.get(
                    "language",
                    "en"
                ),
                confidence=item.get(
                    "confidence",
                    1.0
                ),
                attributes=item.get(
                    "attributes",
                    {}
                ),
                metadata=item.get(
                    "metadata",
                    {}
                ),
                passport=item.get(
                    "passport",
                    {}
                ),
                version=item.get(
                    "version",
                    "1.0"
                )
            )

            entities.append(entity)

        print()
        print("════════════════════════════")
        print("📂 Registry Loaded")
        print()
        print(f"Objects : {len(entities)}")
        print()
        print("════════════════════════════")
        return entities
