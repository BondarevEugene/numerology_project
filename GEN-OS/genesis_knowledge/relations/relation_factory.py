"""
==========================================================
GENESIS HR®
Relation Factory
==========================================================
"""

from .relation import Relation


class RelationFactory:

    @staticmethod
    def create(
            source,
            relation,
            target,
            weight=100,
            description=""
    ):
        return Relation(
            source=source,
            target=target,
            relation=relation,
            weight=weight,
            description=description
        )
