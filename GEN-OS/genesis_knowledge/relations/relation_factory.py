"""
GENESIS HR®

Relation Factory
"""

from .relation import Relation


class RelationFactory:

    @staticmethod
    def create(

        source,

        target,

        relation_type,

        weight=1.0,

        confidence=1.0,

        metadata=None

    ):

        return Relation(

            source=source,

            target=target,

            relation_type=relation_type,

            weight=weight,

            confidence=confidence,

            metadata=metadata or {}

        )