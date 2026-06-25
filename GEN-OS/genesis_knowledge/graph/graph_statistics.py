"""
GENESIS HR®

Graph Statistics
"""

class GraphStatistics:

    def __init__(self,graph):

        self.graph=graph

    def summary(self):

        return{

            "nodes":

            self.graph.node_count(),

            "edges":

            self.graph.edge_count()

        }