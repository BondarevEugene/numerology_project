"""
GENESIS HR®

Graph Validator
"""

class GraphValidator:

    @staticmethod

    def validate(graph):

        ids=set()

        for node in graph.nodes.values():

            if node.id in ids:

                raise Exception(

                    f"Duplicate node {node.id}"

                )

            ids.add(node.id)

        return True