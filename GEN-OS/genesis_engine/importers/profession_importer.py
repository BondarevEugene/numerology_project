"""
═══════════════════════════════════════════════════════════════════════

GENESIS KNOWLEDGE ENGINE
MODULE    Profession Importer
MODULE ID    GKH-IMPORT-001
VERSION    1.0.0 Alpha
LAYER    Import Engine

DESCRIPTION
Imports professions from any supported
provider into Genesis Registry.

Responsibilities
✓ Load dataset
✓ Parse records
✓ Create Entities
✓ Register Entities
✓ Return Registry

Pipeline

Provider
      ↓
Parser
      ↓
EntityFactory
      ↓
EntityRegistry
═══════════════════════════════════════════════════════════════════════
"""

from pathlib import Path

from ..providers.json_provider import JsonProvider
from ..parsers.profession_parser import ProfessionParser
from ..registry.entity_registry import EntityRegistry


class ProfessionImporter:
    NAME = "Profession Importer"
    VERSION = "1.0.0"

    def __init__(self):
        self.registry = EntityRegistry()

    # ==========================================================
    # IMPORT
    # ==========================================================

    def run(self, filepath):
        filepath = Path(filepath)
        print()
        print("═══════════════════════════════════════")
        print("🚀 GENESIS IMPORT ENGINE")
        print("═══════════════════════════════════════")
        print()
        print("STEP 1")
        print("Loading dataset...")
        provider = JsonProvider(filepath)
        dataset = provider.load()
        print()
        print("STEP 2")
        print("Parsing entities...")
        entities = ProfessionParser.parse_many(
            dataset
        )
        print()
        print("STEP 3")
        print("Registering entities...")
        for entity in entities:
            self.registry.add(entity)

        print()
        print("═══════════════════════════════════════")
        print("IMPORT COMPLETED")
        print("═══════════════════════════════════════")
        print()
        print(f"Imported : {len(entities)}")
        print(f"Registry : {len(self.registry)}")
        print()
        return self.registry

    from ..storage.json_storage import JsonStorage
    storage = JsonStorage(
        "registry/entities.json"
    )
    storage.save(
        self.registry
    )

    # ==========================================================
    # SHORTCUT
    # ==========================================================

    @classmethod
    def import_json(cls, filepath):
        importer = cls()
        return importer.run(filepath)