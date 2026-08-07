"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   GENESIS HR®                                                                ║
║──────────────────────────────────────────────────────────────────────────────║
║ MODULE      : Knowledge Service                                              ║
║ FILE        : services/knowledge_service.py                                  ║
║ LAYER       : Business Logic                                                 ║
║ BUILD       : 0500                                                           ║
║ STATUS      : ACTIVE                                                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

from services.base_service import BaseService


class KnowledgeService(BaseService):

    def __init__(self):

        super().__init__()

        self.name = "Knowledge"

        self.registry = None

        self.boot()

    # ==========================================================
    # REGISTRY
    # ==========================================================

    def attach(self, registry):

        self.registry = registry

    def ready(self):

        return self.registry is not None

    # ==========================================================
    # DATA
    # ==========================================================

    def all(self):

        if not self.ready():

            return []

        return self.registry.all()

    def count(self):

        return len(self.all())

    def get(self, node_id):
        if not self.ready():
            return None
        return self.registry.find(entity_id)

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search(self, query):
        if not self.ready():
            return []
        if not query:
            return []
        query = query.lower()
        result = []
        for entity in self.all():
            title = str(
                getattr(
                    entity,
                    "title",
                    ""
                )
            ).lower()
            name = str(
                getattr(
                    entity,
                    "name",
                    ""
                )
            ).lower()
            description = str(
                getattr(
                    entity,
                    "description",
                    ""
                )
            ).lower()
            if (
                query in title
                or
                query in name
                or
                query in description
            ):
                result.append(entity)
        return result

    # ==========================================================
    # FILTER
    # ==========================================================

    def by_type(self, entity_type):
        if not self.ready():
            return []
        result = []
        for entity in self.all():
            if getattr(
                entity,
                "entity_type",
                ""
            ) == entity_type:
                result.append(entity)
        return result

    # ==========================================================
    # GRAPH
    # ==========================================================

    def nodes(self):
        return self.all()

    def edges(self):
        return []

    def graph(self):
        return {
            "nodes": self.nodes(),
            "edges": self.edges()
        }

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    def dashboard(self):
        return [
            {
                "title": "Knowledge",
                "value": self.count(),
                "subtitle": "Entities",
                "icon": "📚"
            },
            {
                "title": "Graph",
                "value": len(self.edges()),
                "subtitle": "Relations",
                "icon": "🕸"
            }
        ]

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary(self):
        return {
            "loaded": self.ready(),
            "entities": self.count(),
            "relations": len(self.edges())
        }

    # ==========================================================
    # WORKSPACE
    # ==========================================================

    def workspace(self):
        return {
            "summary": self.summary(),
            "dashboard": self.dashboard(),
            "nodes": self.nodes(),
            "edges": self.edges()
        }

    # ==========================================================
    # STATISTICS
    # ==========================================================

    def statistics(self):
        return {
            "loaded": self.ready(),
            "entities": self.count(),
            "nodes": len(self.nodes()),
            "edges": len(self.edges())
        }

    # ==========================================================
    # HEALTH
    # ==========================================================

    def health(self):
        return {
            "service": self.name,
            "ready": self.ready(),
            "entities": self.count()
        }

knowledge_service = KnowledgeService()
