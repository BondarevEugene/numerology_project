"""
═══════════════════════════════════════════════════════════════
GENESIS HR®

Knowledge Graph
═══════════════════════════════════════════════════════════════
"""

class KnowledgeGraph:

    def __init__(self):

        self.nodes={}

        self.edges=[]

    def add_node(self,node):

        self.nodes[node.id]=node

    def add_edge(self,edge):

        self.edges.append(edge)

    def get_node(self,node_id):

        return self.nodes.get(node_id)

    def node_count(self):

        return len(self.nodes)

    def edge_count(self):

        return len(self.edges)