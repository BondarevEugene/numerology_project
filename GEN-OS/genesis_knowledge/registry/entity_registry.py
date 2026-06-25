"""
════════════════════════════════════════════════════════════════════

GENESIS HR®

Knowledge Core

Module:
Entity Registry

File:
entity_registry.py

Purpose:
Central in-memory registry of all Genesis entities.

════════════════════════════════════════════════════════════════════
"""

from typing import Dict
from typing import List
from typing import Optional

from .entity import Entity
from .entity_validator import EntityValidator


class EntityRegistry:

    def __init__(self, storage=None):
        self.storage = storage
        self._entities = {}

    @property
    def count(self) -> int:
        return len(self._entities)

    def clear(self) -> None:
        self._entities.clear()

    def exists(
            self,
            entity_id: str
    ) -> bool:
        return entity_id in self._entities

    def add(
            self,
            entity: Entity
    ) -> None:
        errors = EntityValidator.validate(entity)
        if errors:
            raise ValueError(
                "\n".join(errors)
            )
        if entity.id in self._entities:
            raise ValueError(
                f"Entity '{entity.id}' already exists."
            )
        self._entities[entity.id] = entity

    def update(
            self,
            entity: Entity
    ) -> None:
        if entity.id not in self._entities:
            raise KeyError(
                entity.id
            )
        errors = EntityValidator.validate(entity)
        if errors:
            raise ValueError(
                "\n".join(errors)
            )

        entity.touch()
        self._entities[entity.id] = entity

    def remove(
            self,
            entity_id: str
    ) -> None:
        self._entities.pop(
            entity_id,
            None
        )

    def get(
            self,
            entity_id: str
    ) -> Optional[Entity]:
        return self._entities.get(
            entity_id
        )

    def all(self) -> List[Entity]:
        return list(
            self._entities.values()
        )

    def find_by_title(
            self,
            title: str
    ) -> Optional[Entity]:
        title = title.strip().lower()
        for entity in self._entities.values():
            if entity.title.lower() == title:
                return entity
        return None

    def search(
            self,
            text: str
    ) -> List[Entity]:
        text = text.lower()
        result = []
        for entity in self._entities.values():
            if text in entity.title.lower():
                result.append(entity)
                continue
            for alias in entity.aliases:
                if text in alias.lower():
                    result.append(entity)
                    break
        return result

    def filter_by_type(
            self,
            entity_type
    ) -> List[Entity]:
        return [
            entity
            for entity in self._entities.values()
            if entity.type == entity_type
        ]

    def statistics(self) -> dict:
        stat = {
            "entities": self.count,
            "types": {}
        }
        for entity in self._entities.values():
            key = entity.type.value
            stat["types"][key] = (
                    stat["types"].get(
                        key,
                        0
                    ) + 1
            )
        return stat

    def __len__(self):
        return self.count

    def __iter__(self):
        return iter(
            self._entities.values()
        )

    def __contains__(
            self,
            entity_id
    ):
        return entity_id in self._entities

    def save_all(self):
        if self.storage is None:
            return
        for entity in self._entities.values():
            self.storage.save(entity)

    def load_all(self, entity_type):
        if self.storage is None:
            return
        entities = self.storage.list(entity_type)
        for entity in entities:
            self._entities[entity.id] = entity