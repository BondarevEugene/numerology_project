"""
═══════════════════════════════════════════════════════════════════════

GENESIS KNOWLEDGE ENGINE

MODULE
    Profession Parser

MODULE ID
    GKH-PARSER-001

VERSION
    1.0.0 Alpha

LAYER
    Parsers

DESCRIPTION

Transforms raw Profession data
(JSON / CSV / Excel / API)
into Genesis Entity objects.

Parser responsibilities

✓ Normalize fields
✓ Fill defaults
✓ Call EntityFactory

Parser DOES NOT

✗ Read files
✗ Save Registry
✗ Create relations

Pipeline

JSON Provider
        ↓
Profession Parser
        ↓
Entity Factory
        ↓
Entity
        ↓
Registry

═══════════════════════════════════════════════════════════════════════
"""

from ..registry.entity_factory import EntityFactory
from ..schema.knowledge_schema import (
    SourceType,
    EntityStatus
)


class ProfessionParser:
    NAME = "Profession Parser"
    VERSION = "1.0.0"

    # ==========================================================
    # PARSE ONE
    # ==========================================================

    @staticmethod
    def parse(item: dict):
        return EntityFactory.profession(
            title=item.get(
                "title",
                ""
            ),
            title_ru=item.get(
                "title_ru",
                ""
            ),
            title_ua=item.get(
                "title_ua",
                ""
            ),
            description=item.get(
                "description",
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
            aliases=item.get(
                "aliases",
                []
            ),
            attributes={
                "salary":
                    item.get("salary"),
                "education":
                    item.get("education"),
                "future_demand":
                    item.get("future_demand"),
                "automation_risk":
                    item.get("automation_risk"),
                "remote":
                    item.get("remote"),
                "keywords":
                    item.get("keywords", [])
            },

            metadata=item.get(
                "metadata",
                {}
            ),

            passport={
                "provider":
                    "json",
                "provider_version":
                    "1.0",
                "external_id":
                    item.get(
                        "id"
                    )
            },

            source=SourceType.JSON,
            status=EntityStatus.IMPORTED
        )

    # ==========================================================
    # PARSE MANY
    # ==========================================================

    @classmethod
    def parse_many(cls, dataset):
        entities = []
        for row in dataset:
            entity = cls.parse(row)
            entities.append(entity)
        print()
        print("═══════════════════════════════")
        print("🧠 Profession Parser")
        print()
        print(f"Entities created : {len(entities)}")
        print()
        print("═══════════════════════════════")
        return entities
