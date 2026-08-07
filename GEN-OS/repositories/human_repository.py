"""
═══════════════════════════════════════════════════════════════════════

GENESIS HR®

Human Repository

BUILD 0400

═══════════════════════════════════════════════════════════════════════
"""

from repositories.base_repository import BaseRepository


class HumanRepository(BaseRepository):

    def profile(self):
        return None

    def dashboard(self):
        return []

    def competencies(self):
        return []

    def professions(self):
        return []

    def risks(self):
        return []

    def roadmap(self):
        return []