"""
═══════════════════════════════════════════════════════════════════════
GENESIS KNOWLEDGE ENGINE

MODULE    Graph Engine
MODULE ID    GKH-GRAPH-001

VERSION    1.0.0 Alpha

LAYER    Knowledge Graph

DESCRIPTION
Central Knowledge Graph Engine.
The Graph is the heart of Genesis.
Every AI recommendation,
prediction,
career path,
development protocol
and evolution strategy
starts here.

The Graph DOES NOT know
what a Profession is.

It only knows

    Entity

    Relation

and how to navigate
between them.
═══════════════════════════════════════════════════════════════════════
"""

from collections import defaultdict


class GraphEngine:
    def __init__(
            self,
            registry,
            relations
    ):
        self.registry = registry
        self.relations = relations

    # ==========================================================
    # BASIC LOOKUP
    # ==========================================================

    def entity(self, uuid):
        return self.registry.get(uuid)

    # ==========================================================
    # OUTGOING
    # ==========================================================

    def outgoing(
            self,
            entity
    ):
        return self.relations.outgoing(
            entity
        )

    # ==========================================================
    # INCOMING
    # ==========================================================

    def incoming(
            self,
            entity
    ):
        return self.relations.incoming(
            entity
        )

    # ==========================================================
    # RELATED ENTITIES
    # ==========================================================

    def related(
            self,
            entity
    ):
        result = []
        for relation in self.outgoing(entity):
            target = self.registry.get(
                relation.target_uuid
            )
            if target:
                result.append(target)
        return result

    # ==========================================================
    # FILTER BY RELATION
    # ==========================================================
    def related_by(
            self,
            entity,
            relation_type
    ):
        result = []
        for relation in self.outgoing(entity):
            if relation.relation_type != relation_type:
                continue
            target = self.registry.get(
                relation.target_uuid
            )
            if target:
                result.append(target)
        return result

    # ==========================================================
    # HIGH LEVEL API
    # ==========================================================

    def requires(self, entity):
        return self.related_by(
            entity,
            "requires"
        )

    def develops(self, entity):
        return self.related_by(
            entity,
            "develops"
        )

    def books(self, entity):
        return self.related_by(
            entity,
            "recommended_book"
        )

    def habits(self, entity):
        return self.related_by(
            entity,
            "recommended_habit"
        )

    def sports(self, entity):
        return self.related_by(
            entity,
            "recommended_sport"
        )

    def protocols(self, entity):
        return self.related_by(
            entity,
            "recommended_protocol"
        )

    # ==========================================================
    # GRAPH INFO
    # ==========================================================

    def statistics(self):
        return {
            "entities":
                len(self.registry),
            "relations":
                len(self.relations)
        }
