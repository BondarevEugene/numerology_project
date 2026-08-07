"""
═══════════════════════════════════════════════════════════════════════

GENESIS HR®

Knowledge Repository

BUILD 0400

═══════════════════════════════════════════════════════════════════════
"""

from repositories.base_repository import BaseRepository


class KnowledgeRepository(BaseRepository):

    def nodes(self):
        return self.all()

    def edges(self):
        return []

    def graph(self):

        return {

            "nodes": self.nodes(),

            "edges": self.edges()

        }

    def summary(self):

        return {

            "nodes": len(self.nodes()),

            "edges": len(self.edges())

        }