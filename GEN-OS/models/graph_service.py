"""
═══════════════════════════════════════════════════════════════════════

Knowledge Graph Service

═══════════════════════════════════════════════════════════════════════
"""

from models.knowledge_edge import KnowledgeEdge


class GraphService:

    def __init__(self):

        self.nodes = {}

        self.edges = []

    def add_node(self, node):

        self.nodes[node.id] = node

    def add_edge(self, edge: KnowledgeEdge):

        self.edges.append(edge)

    def get_node(self, node_id):

        return self.nodes.get(node_id)

    def neighbours(self, node_id):

        result = []

        for edge in self.edges:

            if edge.source == node_id:

                result.append(self.get_node(edge.target))

        return result

    def clear(self):

        self.nodes.clear()

        self.edges.clear()