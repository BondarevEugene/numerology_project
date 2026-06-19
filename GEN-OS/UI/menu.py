"""
GENOS Menu Builder
"""

from .layout import WORKSPACE


class MenuBuilder:
    @staticmethod
    def sidebar():
        return sorted(
            WORKSPACE,
            key=lambda x: x.order
        )