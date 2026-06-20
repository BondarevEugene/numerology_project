"""
==========================================================
GENESIS HR®
Knowledge Graph Engine
==========================================================
"""


class GraphEngine:

    def __init__(
            self,
            entity_registry,
            relation_registry
    ):
        self.entities = entity_registry
        self.relations = relation_registry

    def neighbours(
            self,
            entity_id
    ):
        return self.relations.by_source(entity_id)

    def statistics(self):
        return {
            "entities": self.entities.count,
            "relations": len(self.relations.all())
        }
