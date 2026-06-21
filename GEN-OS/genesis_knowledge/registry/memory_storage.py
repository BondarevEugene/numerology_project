"""
==========================================================
GENESIS HR®
Memory Storage
Version:
1.0

Description:
Временное хранилище.
Используется для тестов и AI Simulation.
==========================================================
"""

from .storage import Storage


class MemoryStorage(Storage):

    def __init__(self):
        self.entities = {}

    def save(self, entity):
        self.entities[entity.id] = entity

    def load(self, entity_id):
        return self.entities.get(entity_id)

    def delete(self, entity_id):
        if entity_id in self.entities:
            del self.entities[entity_id]

    def exists(self, entity_id):
        return entity_id in self.entities

    def list(self, entity_type):
        return [
            entity
            for entity in self.entities.values()
            if entity.entity_type == entity_type
        ]

    def statistics(self):
        return {
            "entities": len(self.entities)
        }
