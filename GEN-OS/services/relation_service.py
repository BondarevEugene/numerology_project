"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS
Relation Service

BUILD:0035

DESCRIPTION
Работает со всеми отношениями Knowledge Graph.

═══════════════════════════════════════════════════════════════════════
"""


class RelationService:

    def __init__(self):
        self.registry = None

    def attach(self, registry):
        self.registry = registry

    def all(self):
        if self.registry is None:
            return []
        return self.registry.all()

    def count(self):
        return len(self.all())

    def by_type(self, relation_type):
        result = []
        for relation in self.all():
            if getattr(
                    relation,
                    "relation_type",
                    ""
            ) == relation_type:
                result.append(relation)
        return result

    def statistics(self):
        return {
            "relations": self.count()
        }


relation_service = RelationService()
