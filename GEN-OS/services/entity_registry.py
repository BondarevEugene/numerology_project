"""
═══════════════════════════════════════════════════════════════════════

GENESIS®

Entity Registry

BUILD 0104

═══════════════════════════════════════════════════════════════════════
"""

from models.entity import Entity
from models.relation import Relation


class EntityRegistry:

    def __init__(self):

        self.entities = {}

        self.relations = {}

    def register(self, entity: Entity):

        self.entities[entity.id] = entity

        return entity

    def register_relation(self, relation: Relation):

        self.relations[relation.id] = relation

        return relation

    def get(self, entity_id):

        return self.entities.get(entity_id)

    def all(self):

        return list(self.entities.values())

    def all_relations(self):

        return list(self.relations.values())

    def clear(self):

        self.entities.clear()

        self.relations.clear()


registry = EntityRegistry()