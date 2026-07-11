"""
===============================================================================

 GENESIS HR® GEN-OS
 FILE ---- services/knowledge_graph_service.py
 BUILD ----- 0.2.1
 DESCRIPTION
  -----------
 Enterprise Knowledge Graph Engine.
 Stores every domain object.
 Profession
 Skill
 Competency
 Course
 Vacancy
 Human
 KnowledgeNode
===============================================================================
"""

from __future__ import annotations

from collections import defaultdict

from typing import Dict
from typing import Iterable
from typing import Iterator

from models.knowledge_edge import KnowledgeEdge

import logging


LOGGER = logging.getLogger("GEN-OS.Graph")


class KnowledgeGraphService:
    """
    Enterprise in-memory graph.
    O(1)
        node lookup
    O(1)
        adjacency lookup
    """

    def __init__(self):
        self.clear()

    # ------------------------------------------------------------

    def clear(self):
        self._nodes: Dict[str, object] = {}
        self._edges: list[
            KnowledgeEdge
        ] = []
        self._adjacency = defaultdict(list)
        self._reverse = defaultdict(list)

    # ------------------------------------------------------------

    @property
    def nodes(self):
        return self._nodes

    # ------------------------------------------------------------

    @property
    def edges(self):
        return self._edges

    # ------------------------------------------------------------

    def add_node(self,node):
        self._nodes[node.id] = node

    # ------------------------------------------------------------

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    # ------------------------------------------------------------

    def node(self, node_id: str):
        return self._nodes.get(node_id)

    # ------------------------------------------------------------

    def has_node(self, node_id: str) -> bool:
        return node_id in self._nodes

    # ------------------------------------------------------------
    # EDGE MANAGEMENT
    # ------------------------------------------------------------

    def add_edge(self, edge: KnowledgeEdge) -> None:
        """
        Register graph edge.
        """
        self._edges.append(edge)
        self._adjacency[edge.source].append(edge)
        self._reverse[edge.target].append(edge)

    # ------------------------------------------------------------

    def add_edges(self, edges: Iterable[KnowledgeEdge]) -> None:
        """
        Register multiple edges.
        """
        for edge in edges:
            self.add_edge(edge)

    # ------------------------------------------------------------

    def neighbours(self, node_id: str) -> list:
        """
        Return neighbouring nodes.
        """
        result = []
        for edge in self._adjacency.get(node_id, []):
            node = self.node(edge.target)
            if node is not None:
                result.append(node)
        return result

    # ------------------------------------------------------------

    def parents(self, node_id: str) -> list:
        """
        Return parent nodes.
        """
        result = []
        for edge in self._reverse.get(node_id,[]):
            node = self.node(edge.source)
            if node is not None:
                result.append(node)
        return result

    # ------------------------------------------------------------

    def outgoing_edges(self, node_id: str) -> list[KnowledgeEdge]:
        """
        Return outgoing edges.
        """
        return list(self._adjacency.get(node_id, []))

    # ------------------------------------------------------------

    def incoming_edges(self, node_id: str) -> list[KnowledgeEdge]:
        """
        Return incoming edges.
        """
        return list(
            self._reverse.get(
                node_id,
                []
            )

        )

    # ------------------------------------------------------------

    def edge_count(self) -> int:

        return len(self._edges)

    # ------------------------------------------------------------

    def node_count(self) -> int:

        return len(self._nodes)

    # ------------------------------------------------------------

    def has_edge(
        self,
        source: str,
        target: str,
        relation: str | None = None
    ) -> bool:
        """
        Check edge existence.
        """

        for edge in self._adjacency.get(
            source,
            []
        ):

            if edge.target != target:
                continue

            if relation is None:
                return True

            if edge.relation == relation:
                return True

        return False

    # ------------------------------------------------------------

    def remove_edge(
        self,
        source: str,
        target: str
    ) -> bool:
        """
        Remove graph edge.
        """

        removed = False

        self._edges = [

            edge

            for edge in self._edges

            if not (

                edge.source == source

                and

                edge.target == target

            )

        ]

        if source in self._adjacency:

            remaining = []

            for edge in self._adjacency[source]:

                if edge.target == target:

                    removed = True

                    continue

                remaining.append(edge)

            self._adjacency[source] = remaining

        if target in self._reverse:

            self._reverse[target] = [

                edge

                for edge in self._reverse[target]

                if edge.source != source

            ]

        return removed
    # ------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------

    def find_by_type(
        self,
        class_name: str
    ) -> list:
        """
        Return every node of given class.
        """

        return [

            node

            for node in self._nodes.values()

            if node.__class__.__name__ == class_name

        ]

    # ------------------------------------------------------------

    def find_by_name(
        self,
        text: str
    ) -> list:
        """
        Case-insensitive search.
        """

        text = text.lower()

        result = []

        for node in self._nodes.values():

            name = getattr(
                node,
                "name",
                ""
            )

            if text in name.lower():

                result.append(node)

        return result

    # ------------------------------------------------------------

    def nodes_of(
        self,
        model
    ) -> list:
        """
        Return nodes of given model class.
        """

        return [

            node

            for node in self._nodes.values()

            if isinstance(node, model)

        ]

    # ------------------------------------------------------------

    def relation_edges(
        self,
        relation: str
    ) -> list[KnowledgeEdge]:
        """
        Return edges by relation type.
        """

        return [

            edge

            for edge in self._edges

            if edge.relation == relation

        ]

    # ------------------------------------------------------------

    def statistics(self) -> dict:
        """
        Graph statistics.
        """

        classes = {}

        for node in self._nodes.values():

            name = node.__class__.__name__

            classes.setdefault(
                name,
                0
            )

            classes[name] += 1

        relations = {}

        for edge in self._edges:

            relations.setdefault(
                edge.relation,
                0
            )

            relations[edge.relation] += 1

        return {

            "nodes":
                self.node_count(),

            "edges":
                self.edge_count(),

            "classes":
                classes,

            "relations":
                relations

        }

    # ------------------------------------------------------------
    # EXPORT
    # ------------------------------------------------------------

    def export_json(self) -> dict:
        """
        Export graph.

        Ready for REST API.
        """

        return {

            "nodes": [

                node.to_dict()

                if hasattr(
                    node,
                    "to_dict"
                )

                else vars(node)

                for node in self._nodes.values()

            ],

            "edges": [

                {

                    "source":
                        edge.source,

                    "target":
                        edge.target,

                    "relation":
                        edge.relation,

                    "weight":
                        edge.weight,

                    "bidirectional":
                        edge.bidirectional

                }

                for edge in self._edges

            ]

        }

    # ------------------------------------------------------------

    def cytoscape(self) -> dict:
        """
        Export graph for Cytoscape.js.
        """

        nodes = []

        edges = []

        for node in self._nodes.values():

            nodes.append({

                "data": {

                    "id": node.id,

                    "label": getattr(
                        node,
                        "name",
                        node.id
                    ),

                    "type": node.__class__.__name__

                }

            })

        for edge in self._edges:

            edges.append({

                "data": {

                    "source": edge.source,

                    "target": edge.target,

                    "label": edge.relation,

                    "weight": edge.weight

                }

            })

        return {

            "nodes": nodes,

            "edges": edges

        }

        # ------------------------------------------------------------
        # GRAPH ALGORITHMS
        # ------------------------------------------------------------

        def connected_nodes(
                self,
                node_id: str
        ) -> list:
            """
            Return all directly connected nodes.
            """

            result = []

            result.extend(
                self.neighbours(node_id)
            )

            result.extend(
                self.parents(node_id)
            )

            unique = {}

            for node in result:
                unique[node.id] = node

            return list(unique.values())

        # ------------------------------------------------------------

        def remove_node(
                self,
                node_id: str
        ) -> bool:
            """
            Remove node and every connected edge.
            """

            if node_id not in self._nodes:
                return False

            del self._nodes[node_id]

            self._edges = [

                edge

                for edge in self._edges

                if edge.source != node_id

                   and edge.target != node_id

            ]

            self._adjacency.pop(
                node_id,
                None
            )

            self._reverse.pop(
                node_id,
                None
            )

            for source in self._adjacency:
                self._adjacency[source] = [

                    edge

                    for edge in self._adjacency[source]

                    if edge.target != node_id

                ]

            for target in self._reverse:
                self._reverse[target] = [

                    edge

                    for edge in self._reverse[target]

                    if edge.source != node_id

                ]

            return True

        # ------------------------------------------------------------

        def merge(
                self,
                other: "KnowledgeGraphService"
        ) -> None:
            """
            Merge another graph.
            """

            self.add_nodes(
                other.nodes.values()
            )

            self.add_edges(
                other.edges
            )

        # ------------------------------------------------------------

        def shortest_path(
                self,
                source: str,
                target: str
        ) -> list[str]:
            """
            Breadth First Search.

            Returns node ids.
            """

            from collections import deque

            queue = deque()

            queue.append(
                (source, [source])
            )

            visited = {

                source

            }

            while queue:

                current, path = queue.popleft()

                if current == target:
                    return path

                for edge in self.outgoing_edges(
                        current
                ):

                    if edge.target in visited:
                        continue

                    visited.add(
                        edge.target
                    )

                    queue.append(

                        (

                            edge.target,

                            path + [edge.target]

                        )

                    )

            return []

        # ------------------------------------------------------------

        def subgraph(
                self,
                root: str,
                depth: int = 2
        ) -> dict:
            """
            Build neighbourhood graph.
            """

            visited = set()

            queue = [

                (root, 0)

            ]

            nodes = []

            edges = []

            while queue:

                node_id, level = queue.pop(0)

                if node_id in visited:
                    continue

                visited.add(
                    node_id
                )

                node = self.node(node_id)

                if node is not None:
                    nodes.append(node)

                if level >= depth:
                    continue

                for edge in self.outgoing_edges(
                        node_id
                ):
                    edges.append(edge)

                    queue.append(

                        (

                            edge.target,

                            level + 1

                        )

                    )

            return {

                "nodes": nodes,

                "edges": edges

            }

        # ------------------------------------------------------------

        def __len__(self):

            return len(
                self._nodes
            )

        # ------------------------------------------------------------

        def __iter__(self):

            return iter(
                self._nodes.values()
            )

        # ------------------------------------------------------------

        def __contains__(
                self,
                node_id: str
        ):

            return node_id in self._nodes

        # ------------------------------------------------------------

        def __repr__(self):

            return (

                "<KnowledgeGraph "

                f"nodes={self.node_count()} "

                f"edges={self.edge_count()}>"

            )

    # ============================================================
    # GLOBAL GRAPH
    # ============================================================

    knowledge_graph = KnowledgeGraphService()
