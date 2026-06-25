"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Statistics Service

BUILD:0141
═══════════════════════════════════════════════════════════════════════
"""

from services.entity_service import entity_service
from services.relation_service import relation_service


class StatisticsService:

    def overview(self):

        return {

            "entities":
                entity_service.count(),

            "relations":
                relation_service.count()

        }


statistics_service = (
    StatisticsService()
)