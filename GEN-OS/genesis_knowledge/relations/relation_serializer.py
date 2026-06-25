"""
GENESIS HR®

Relation Serializer
"""

from dataclasses import asdict


class RelationSerializer:

    @staticmethod
    def serialize(

        relation

    ):

        return asdict(

            relation

        )