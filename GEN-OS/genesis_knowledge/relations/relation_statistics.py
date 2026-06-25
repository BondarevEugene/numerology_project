from collections import Counter


class RelationStatistics:

    @staticmethod
    def summary(registry):

        counter=Counter()

        for relation in registry.all():

            counter[relation.relation_type]+=1

        return dict(counter)