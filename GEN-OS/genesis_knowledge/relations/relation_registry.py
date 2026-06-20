"""
==========================================================
GENESIS HR®
Relation Registry
==========================================================
"""

from collections import defaultdict


class RelationRegistry:

    def __init__(self):
        self._relations = []
        self._index = defaultdict(list)

    def add(self, relation):
        self._relations.append(relation)
        self._index[relation.source].append(relation)

    def all(self):
        return self._relations

    def by_source(self, entity):
        return self._index.get(entity, [])

    def statistics(self):
        return {
            "relations": len(self._relations),
            "nodes": len(self._index)
        }
