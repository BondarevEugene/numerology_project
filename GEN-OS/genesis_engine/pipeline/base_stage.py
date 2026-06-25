"""
═══════════════════════════════════════════════════════════════════════
MODULE ID:     GKH-PIPE-002
NAME:    Base Pipeline Stage
DESCRIPTION
Every Pipeline Stage
inherits this class.
═══════════════════════════════════════════════════════════════════════
"""

from abc import ABC
from abc import abstractmethod


class BaseStage(ABC):

    @abstractmethod
    def execute(self, context):

        pass
