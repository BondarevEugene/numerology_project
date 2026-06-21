"""
GENESIS HR®

Graph Search
"""

class GraphSearch:

    def __init__(self,graph):

        self.graph=graph

    def by_type(

        self,

        entity_type

    ):

        return [

            n

            for n

            in self.graph.nodes.values()

            if n.entity_type==entity_type

        ]