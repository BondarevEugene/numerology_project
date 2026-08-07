"""
GENESIS®

Graph Engine
"""

class GraphEngine:

    def __init__(self, registry):

        self.registry = registry

    def neighbours(self, entity_id):

        result = []

        for relation in self.registry.all_relations():

            if relation.source == entity_id:

                node = self.registry.get(relation.target)

                if node:

                    result.append(node)

        return result

    def parents(self, entity_id):

        result = []

        for relation in self.registry.all_relations():

            if relation.target == entity_id:

                node = self.registry.get(relation.source)

                if node:

                    result.append(node)

        return result

    def connected(self, entity_id):

        ids = set()

        for relation in self.registry.all_relations():

            if relation.source == entity_id:

                ids.add(relation.target)

            if relation.target == entity_id:

                ids.add(relation.source)

        return [
            self.registry.get(x)

            for x in ids

            if self.registry.get(x)
        ]