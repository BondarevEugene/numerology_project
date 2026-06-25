"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS Application
BUILD:0103
Главная точка управления платформой.
═══════════════════════════════════════════════════════════════════════
"""

from kernel.platform import platform


class Application:

    def __init__(self):
        self.platform = platform

    def boot(self):
        self.platform.boot()

    def context(self):
        return self.platform.context()

    def statistics(self):
        return self.platform.statistics()


application = Application()