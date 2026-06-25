"""
GENESIS HR®

Graph Builder
"""

from .graph import KnowledgeGraph


class GraphBuilder:

    def __init__(self):

        self.graph=KnowledgeGraph()

    def add_node(self,node):

        self.graph.add_node(node)

        return self

    def add_edge(self,edge):

        self.graph.add_edge(edge)

        return self

    def build(self):

        return self.graph