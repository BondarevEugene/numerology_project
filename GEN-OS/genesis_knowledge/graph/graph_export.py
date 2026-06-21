"""
GENESIS HR®

Graph Export
"""

import json


class GraphExporter:

    @staticmethod

    def export(graph):

        return json.dumps(

            {

                "nodes":

                list(graph.nodes.keys()),

                "edges":[

                    edge.__dict__

                    for edge

                    in graph.edges

                ]

            },

            indent=4

        )