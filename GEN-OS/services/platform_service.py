"""
GENESIS HR®
Platform Service
"""

from kernel.platform import platform


class PlatformService:

    def statistics(self):
        return platform.statistics()

    def context(self):
        return platform.context()


platform_service = PlatformService()
