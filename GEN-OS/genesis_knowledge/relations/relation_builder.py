from .relation import Relation


class RelationBuilder:

    @staticmethod
    def create(source,target,relation_type,weight=100):

        return Relation(
            source=source,
            target=target,
            relation_type=relation_type,
            weight=weight
        )