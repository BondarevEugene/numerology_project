"""
═══════════════════════════════════════════════════════════════════════
GENESIS KNOWLEDGE ENGINE

MODULE
    Entity Registry

MODULE ID
    GKH-REG-002

VERSION
    2.0.0 Alpha

LAYER
    Registry

DESCRIPTION

Central in-memory registry of every
Knowledge Entity inside Genesis.

The Registry acts as the single source
of truth during runtime.

Responsibilities

✓ Register entities
✓ Search entities
✓ Update entities
✓ Remove entities
✓ Build indexes
✓ Statistics

This module DOES NOT

✗ Import data
✗ Validate data
✗ Build graph relations
✗ Execute AI

═══════════════════════════════════════════════════════════════════════
"""

from collections import defaultdict
from typing import Dict, List, Optional

from .entity import Entity


class EntityRegistry:

    def __init__(self):

        # =====================================================
        # PRIMARY STORAGE
        # =====================================================

        self._uuid_index: Dict[str, Entity] = {}

        # =====================================================
        # SECONDARY INDEXES
        # =====================================================

        self._code_index: Dict[str, Entity] = {}
        self._title_index: Dict[str, Entity] = {}
        self._type_index = defaultdict(list)
        self._category_index = defaultdict(list)

    # ==========================================================
    # CRUD
    # ==========================================================

    def add(self, entity: Entity):
        self._uuid_index[entity.uuid] = entity
        self._code_index[entity.code] = entity
        self._title_index[
            entity.title.lower()
        ] = entity
        self._type_index[
            entity.type.value
        ].append(entity)

        self._category_index[
            entity.category
        ].append(entity)

    def update(self, entity: Entity):
        self.remove(entity.uuid)
        self.add(entity)

    def remove(self, uuid: str):
        entity = self._uuid_index.get(uuid)
        if entity is None:
            return

        self._uuid_index.pop(uuid)
        self._code_index.pop(
            entity.code,
            None
        )
        self._title_index.pop(
            entity.title.lower(),
            None
        )
        if entity in self._type_index[
            entity.type.value
        ]:
            self._type_index[
                entity.type.value
            ].remove(entity)

        if entity in self._category_index[
            entity.category
        ]:
            self._category_index[
                entity.category
            ].remove(entity)

    # ==========================================================
    # LOOKUP
    # ==========================================================

    def get(self, uuid):
        return self._uuid_index.get(uuid)

    def exists(self, uuid):
        return uuid in self._uuid_index

    def by_code(self, code):
        return self._code_index.get(code)

    def by_title(self, title):
        return self._title_index.get(
            title.lower()
        )

    def by_type(self, entity_type):
        return list(
            self._type_index.get(
                entity_type,
                []
            )
        )

    def by_category(self, category):
        return list(
            self._category_index.get(
                category,
                []
            )
        )

    def all(self):
        return list(
            self._uuid_index.values()
        )

    # ==========================================================
    # STATISTICS
    # ==========================================================

    def statistics(self):
        return {
            "entities": len(
                self._uuid_index
            ),
            "entity_types": {
                key: len(value)
                for key, value
                in self._type_index.items()
            },
            "categories": {
                key: len(value)
                for key, value
                in self._category_index.items()
            }
        }

    # ==========================================================
    # UTILITIES
    # ==========================================================

    def clear(self):
        self.__init__()

    def __len__(self):
        return len(
            self._uuid_index
        )

    def __iter__(self):
        return iter(
            self._uuid_index.values()
        )

    def __contains__(self, uuid):
        return uuid in self._uuid_index