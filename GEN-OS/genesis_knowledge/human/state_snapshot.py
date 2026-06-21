"""
GENESIS HR®

State Snapshot
"""

from copy import deepcopy


class StateSnapshot:
    @staticmethod
    def capture(
        registry
    ):
        return deepcopy(
            registry.variables
        )