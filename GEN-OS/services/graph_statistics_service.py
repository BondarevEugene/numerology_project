"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Graph Statistics Service

BUILD:0143
═══════════════════════════════════════════════════════════════════════
"""

from services.graph_service import (
    graph_service
)


class GraphStatisticsService:

    def summary(
        self,
        entity_id
    ):

        return {

            "incoming":
                len(
                    graph_service
                    .incoming(
                        entity_id
                    )
                ),

            "outgoing":
                len(
                    graph_service
                    .outgoing(
                        entity_id
                    )
                )

        }


graph_statistics_service = (
    GraphStatisticsService()
)