"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS Graph Service

BUILD:0035

DESCRIPTION
Построение Knowledge Graph.
Используется:
Explorer
Graph Workspace
Simulation
AI

═══════════════════════════════════════════════════════════════════════
"""

from services.entity_service import entity_service
from services.relation_service import relation_service


class GraphService:

    def nodes(self):
        return entity_service.all()

    def edges(self):
        return relation_service.all()

    def statistics(self):
        return {
            "nodes": entity_service.count(),
            "edges": relation_service.count()
        }

"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS
Graph Service
BUILD:0068
DESCRIPTION
Высокоуровневая работа
с графом знаний.

═══════════════════════════════════════════════════════════════════════
"""

from services.relation_service import relation_service


class GraphService:

    def neighbors(
        self,
        entity_id
    ):
        result = []
        for relation in relation_service.all():
            if relation.source == entity_id:
                result.append(
                    relation.target
                )

        return result

    def outgoing(
        self,
        entity_id
    ):

        result = []
        for relation in relation_service.all():
            if relation.source == entity_id:
                result.append(
                    relation
                )
        return result

    def incoming(
        self,
        entity_id
    ):
        result = []
        for relation in relation_service.all():
            if relation.target == entity_id:
                result.append(
                    relation
                )
        return result


graph_service = GraphService()