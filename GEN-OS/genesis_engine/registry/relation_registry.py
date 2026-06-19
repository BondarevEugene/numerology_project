from .relation import Relation


class RelationRegistry:

    def __init__(self):

        self.relations = []

    def add(self, relation: Relation):

        self.relations.append(
            relation
        )

    def count(self):

        return len(
            self.relations
        )

    def all(self):

        return self.relations