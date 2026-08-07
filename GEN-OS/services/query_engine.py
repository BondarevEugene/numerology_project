"""
GENESIS®

Query Engine
"""

class QueryEngine:

    def __init__(self, registry):

        self.registry = registry

    def find(self, **filters):

        entities = self.registry.all()

        result = []

        for entity in entities:

            ok = True

            for key, value in filters.items():

                if getattr(entity, key, None) != value:

                    ok = False

                    break

            if ok:

                result.append(entity)

        return result

    def first(self, **filters):

        data = self.find(**filters)

        if data:

            return data[0]

        return None