class RelationGraph:

    def __init__(self,registry):
        self.registry=registry

    def neighbors(self,node):
        result=[]
        for relation in self.registry.all():
            if relation.source==node:
                result.append(relation.target)
        return result
