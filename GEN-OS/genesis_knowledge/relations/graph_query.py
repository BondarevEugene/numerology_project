"""
==========================================================
GENESIS HR®
Graph Query Engine
==========================================================
"""


class GraphQuery:

    def __init__(self, graph):
        self.graph = graph

    def outgoing(self, entity):
        return self.graph.neighbours(entity)

    def recommendations(self, entity):
        result = []
        for relation in self.graph.neighbours(entity):
            if relation.weight >= 70:
                result.append(relation)
        return result
