"""
═══════════════════════════════════════════════════════════════════════════════

 GENESIS HR® // GEN-OS

 MODULE:
 Knowledge Graph Builder

 FILE:
 knowledge_graph_service.py

 BUILD:
 0106

 DESCRIPTION
 -----------------------------------------------------------------------------

 Строитель Knowledge Graph платформы.

 Responsibilities

    • Построение графа из Registry
    • Создание узлов
    • Создание связей
    • Индексация
    • Подготовка графа
      для Prediction Engine

 IMPORTANT

 Не занимается:

    ✘ Import
    ✘ Validation
    ✘ Recommendation
    ✘ Prediction

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from collections import defaultdict

from registry.knowledge_registry import KnowledgeRegistry

from models.knowledge_node import KnowledgeNode
from models.knowledge_edge import KnowledgeEdge


class KnowledgeGraphService:

    """
    Builder Knowledge Graph.
    """

    def __init__(self):

        self.registry = None

        self.nodes = {}

        self.edges = []

        self.adjacency = defaultdict(set)

    # =======================================================================
    # REGISTRY
    # =======================================================================

    def attach_registry(
        self,
        registry: KnowledgeRegistry
    ):

        self.registry = registry

    # =======================================================================
    # BUILD
    # =======================================================================

    def build_from_registry(self):

        """
        Полная перестройка Graph.
        """

        if self.registry is None:

            raise RuntimeError(
                "Registry is not attached."
            )

        self.nodes.clear()

        self.edges.clear()

        self.adjacency.clear()

        entities = self.registry.all()

        #
        # Nodes
        #

        for entity in entities:

            node = KnowledgeNode(

                uid=entity.uid,

                entity_type=entity.entity_type,

                title=entity.name,

                description=entity.description,

                metadata=entity.metadata

            )

            self.nodes[node.uid] = node

        #
        # Relations
        #
        # Пока строим связи
        # только по metadata["relations"]
        #

        for entity in entities:

            relations = entity.metadata.get(
                "relations",
                []
            )

            for relation in relations:

                target_uid = relation.get(
                    "target"
                )

                relation_type = relation.get(
                    "type",
                    "RELATED_TO"
                )

                if target_uid not in self.nodes:

                    continue

                edge = KnowledgeEdge(

                    source=entity.uid,

                    target=target_uid,

                    relation_type=relation_type

                )

                self.edges.append(edge)

                self.adjacency[
                    entity.uid
                ].add(
                    target_uid
                )

    # =======================================================================
    # QUERY
    # =======================================================================

    def neighbors(
        self,
        uid
    ):

        return [

            self.nodes[x]

            for x

            in self.adjacency.get(
                uid,
                set()
            )

        ]

    def node(
        self,
        uid
    ):

        return self.nodes.get(uid)

    # =======================================================================
    # EXPORT
    # =======================================================================

    def graph(self):

        return {

            "nodes":

                list(self.nodes.values()),

            "edges":

                self.edges

        }

    # =======================================================================
    # STATISTICS
    # =======================================================================

    def statistics(self):

        return {

            "nodes": len(self.nodes),

            "edges": len(self.edges)

        }


knowledge_graph_service = KnowledgeGraphService()