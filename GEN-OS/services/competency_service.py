"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS
Competency Service
BUILD:0046
DESCRIPTION

Работает с единым реестром компетенций.
Используется:

• Human Workspace
• Career Engine
• Recommendation Engine
• Development Engine
• AI Matching
• Knowledge Registry

═══════════════════════════════════════════════════════════════════════
"""

from collections import defaultdict


class CompetencyService:

    def __init__(self):
        self.registry = None

    def attach(self, registry):
        self.registry = registry

    def all(self):
        if self.registry is None:
            return []
        return self.registry.all()

    def count(self):
        return len(
            self.all()
        )

    def find(
        self,
        entity_id
    ):
        if self.registry is None:
            return None
        return self.registry.find(entity_id)

    def search(self, text):
        result = []
        text = text.lower()
        for competency in self.all():
            title = getattr(competency, "title", "")
            if text in title.lower():
                result.append(competency)
        return result

    def by_category(self, category):
        result = []
        for competency in self.all():
            if getattr(
                competency,
                "category",
                ""
            ) == category:
                result.append(competency)
        return result

    def categories(self):
        data = defaultdict(int)
        for competency in self.all():
            category = getattr(
                competency,
                "category",
                "General"
            )
            data[category] += 1
        return dict(data)

    def top_categories(self):
        items = list(
            self.categories().items()
        )
        items.sort(
            key=lambda x: x[1],
            reverse=True
        )
        return items

    def statistics(self):
        return {
            "count": self.count(),
            "categories": self.categories(),
            "top_categories": self.top_categories()
        }


competency_service = CompetencyService()