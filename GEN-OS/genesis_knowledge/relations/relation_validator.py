"""
GENESIS HR®

Relation Validator
"""

from .relation import Relation


class RelationValidator:

    @staticmethod
    def validate(

        relation: Relation

    ):

        if not relation.source:

            raise ValueError("Relation source is empty.")

        if not relation.target:

            raise ValueError("Relation target is empty.")

        if not relation.relation_type:

            raise ValueError("Relation type is empty.")

        return True