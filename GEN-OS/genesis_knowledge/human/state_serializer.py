"""
GENESIS HR®

State Serializer
"""

from dataclasses import asdict


class StateSerializer:

    @staticmethod
    def serialize(variable):
        return asdict(variable)
