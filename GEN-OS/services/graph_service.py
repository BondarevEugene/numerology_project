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


from services.knowledge_graph_service import (
    knowledge_graph_service
)


class GraphService:

    """
    Runtime API
    над Knowledge Graph.
    """

    def nodes(self):

        return knowledge_graph_service.graph()["nodes"]

    def edges(self):

        return knowledge_graph_service.graph()["edges"]

    def neighbors(
        self,
        uid
    ):

        return knowledge_graph_service.neighbors(uid)

    def statistics(self):

        return knowledge_graph_service.statistics()


graph_service = GraphService()

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
