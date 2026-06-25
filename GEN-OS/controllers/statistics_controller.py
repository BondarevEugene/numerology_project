"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Statistics Controller

BUILD:0142
═══════════════════════════════════════════════════════════════════════
"""

from services.statistics_service import (
    statistics_service
)


class StatisticsController:

    def overview(self):

        return (
            statistics_service
            .overview()
        )


statistics_controller = (
    StatisticsController()
)