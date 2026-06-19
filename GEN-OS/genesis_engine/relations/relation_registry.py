"""
═══════════════════════════════════════════════════════════════════════
GENESIS KNOWLEDGE ENGINE
ODULE    Relation Registry
MODULE ID    GKH-REL-003
VERSION    1.0.0 Alpha
LAYER    Knowledge Graph
DESCRIPTION
Stores every relation inside Genesis.
Provides fast graph lookup.

Supports:
• outgoing edges
• incoming edges
• neighbours
• relation filtering
• graph statistics
═══════════════════════════════════════════════════════════════════════
"""

from collections import defaultdict
from .relation import Relation


class RelationRegistry:
    def __init__(self):
        self._relations = []
        self._outgoing = defaultdict(list)
        self._incoming = defaultdict(list)

    # ==========================================================
    # CRUD
    # ==========================================================
    def add(
            self,
            relation: Relation
    ):
        self._relations.append(
            relation
        )
        self._outgoing[
            relation.source_uuid
        ].append(relation)
        self._incoming[
            relation.target_uuid
        ].append(relation)

    def remove(self, relation_uuid):
        self._relations = [
            r
            for r in self._relations
            if r.uuid != relation_uuid
        ]

    # ==========================================================
    # GRAPH
    # ==========================================================

    def outgoing(
            self,
            entity
    ):
        return self._outgoing.get(
            entity.uuid,
            []
        )

    def incoming(
            self,
            entity
    ):
        return self._incoming.get(
            entity.uuid,
            []
        )

    def neighbours(
            self,
            entity
    ):
        nodes = []
        for relation in self.outgoing(entity):
            nodes.append(
                relation.target_uuid
            )
        return nodes

    # ==========================================================
    # FILTER
    # ==========================================================

    def relations_of_type(
            self,
            relation_type
    ):
        return [
            r
            for r in self._relations
            if r.relation_type == relation_type
        ]

    # ==========================================================
    # STATISTICS
    # ==========================================================

    def count(self):
        return len(
            self._relations
        )

    def statistics(self):
        return {
            "relations": len(
                self._relations
            ),
            "outgoing_nodes": len(
                self._outgoing
            ),
            "incoming_nodes": len(
                self._incoming
            )
        }
    # ==========================================================
    # MAGIC
    # ==========================================================

    def __len__(self):
        return len(
            self._relations
        )

    def __iter__(self):
        return iter(
            self._relations
        )
