"""
═══════════════════════════════════════════════════════════════════════
MODULE ID:    GKH-PIPE-004
NAME:    Entity Importer
DESCRIPTION
Imports validated entities
into Genesis Registry.
═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass


@dataclass
class ImportStatistics:
    imported: int = 0
    updated: int = 0
    skipped: int = 0
    invalid: int = 0


class EntityImporter:

    def __init__(self, registry, validator):
        self.registry = registry
        self.validator = validator

    def execute(self, context):
        stats = ImportStatistics()
        for entity in context.entities:
            if not self.validator.validate(entity):
                stats.invalid += 1
                continue
            if self.registry.exists(entity.uuid):
                self.registry.update(entity)
                stats.updated += 1
            else:
                self.registry.add(entity)
                stats.imported += 1
        context.statistics["import"] = stats
