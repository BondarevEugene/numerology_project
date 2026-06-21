class RelationQuery:

    def __init__(self, registry):
        self.registry = registry

    def outgoing(self, node):
        return [
            r for r in self.registry.all()
            if r.source == node
        ]

    def incoming(self, node):
        return [
            r for r in self.registry.all()
            if r.target == node
        ]

    def by_type(self, relation_type):
        return [
            r for r in self.registry.all()
            if r.relation_type == relation_type
        ]
