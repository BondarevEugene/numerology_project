"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Search Controller

BUILD:0140
═══════════════════════════════════════════════════════════════════════
"""

from services.search_service import (
    search_service
)


class SearchController:

    def search(
        self,
        query
    ):

        return search_service.search(
            query
        )


search_controller = SearchController()