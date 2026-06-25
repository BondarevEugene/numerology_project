"""
GENESIS HR®

Graph Query
"""


class GraphQuery:

    def __init__(self, graph):
        self.graph = graph

    def node(self, node_id):
        return self.graph.get_node(node_id)

    def nodes(self):
        return list(

            self.graph.nodes.values()

        )

    def edges(self):
        return self.graph.edges
