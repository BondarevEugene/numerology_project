"""
═══════════════════════════════════════════════════════════════════════

GENESIS KNOWLEDGE ENGINE
MODULE    Graph Pathfinder

MODULE ID    GKH-GRAPH-002

VERSION    1.0.0 Alpha

LAYER    Knowledge Graph

DESCRIPTION
Performs intelligent traversal
through Genesis Knowledge Graph.
The Pathfinder is responsible for

✓ Graph Traversal
✓ Recommendation Chains
✓ Development Paths
✓ Career Paths
✓ Dependency Search

This module DOES NOT

✗ Create Entities
✗ Create Relations
✗ Import Data
═══════════════════════════════════════════════════════════════════════
"""

from collections import deque


class GraphPathFinder:
    def __init__(
            self,
            graph
    ):
        self.graph = graph

    # ==========================================================
    # BREADTH FIRST SEARCH
    # ==========================================================

    def shortest_path(
            self,
            start,
            target
    ):
        visited = set()
        queue = deque()
        queue.append(
            (start.uuid, [])
        )
        while queue:
            current_uuid, path = queue.popleft()
            if current_uuid in visited:
                continue
            visited.add(current_uuid)
            entity = self.graph.entity(
                current_uuid
            )
            if entity is None:
                continue
            path = path + [entity]
            if current_uuid == target.uuid:
                return path
            for relation in self.graph.outgoing(entity):
                queue.append(
                    (
                        relation.target_uuid,
                        path
                    )
                )
        return []

    # ==========================================================
    # REACHABLE
    # ==========================================================
    def reachable(
            self,
            entity,
            depth=3
    ):
        result = []
        visited = set()
        queue = deque()
        queue.append(
            (
                entity,
                0
            )
        )
        while queue:
            current, level = queue.popleft()
            if current.uuid in visited:
                continue
            visited.add(current.uuid)
            result.append(current)
            if level >= depth:
                continue
            for relation in self.graph.outgoing(current):
                target = self.graph.entity(
                    relation.target_uuid
                )
                if target:
                    queue.append(
                        (
                            target,
                            level + 1
                        )
                    )
        return result

    # ==========================================================
    # RECOMMENDATION TREE
    # ==========================================================

    def recommendation_tree(
            self,
            entity,
            depth=4
    ):
        tree = {}
        self._build_tree(
            entity,
            tree,
            depth
        )
        return tree

    def _build_tree(
            self,
            entity,
            node,
            depth
    ):
        if depth <= 0:
            return
        children = []
        for relation in self.graph.outgoing(entity):
            target = self.graph.entity(
                relation.target_uuid
            )
            if target is None:
                continue
            child = {
                "relation": relation.relation_type,
                "entity": target,
                "children": []
            }
            self._build_tree(
                target,
                child["children"],
                depth - 1
            )
            children.append(child)
        node["entity"] = entity
        node["children"] = children

    # ==========================================================
    # TRACE
    # ==========================================================

    def explain(
            self,
            entity,
            relation_type=None
    ):
        explanation = []
        for relation in self.graph.outgoing(entity):
            if relation_type:
                if relation.relation_type != relation_type:
                    continue
            target = self.graph.entity(
                relation.target_uuid
            )
            if target:
                explanation.append(
                    {
                        "from": entity.title,
                        "relation": relation.relation_type,
                        "to": target.title
                    }
                )
        return explanation
