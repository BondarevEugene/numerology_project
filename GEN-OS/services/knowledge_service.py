"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

GEN-OS

Knowledge Service

FILE: knowledge_service.py

BUILD: 0034

AUTHOR: OpenAI + Yevhenii Bondariev

DESCRIPTION
-----------
Центральный сервис доступа ко всем знаниям платформы.
Не знает ничего о GUI.
Используется:

• Explorer
• Inspector
• Graph
• Human Workspace
• Career Engine
• AI
• Recommendation
• Prediction

═══════════════════════════════════════════════════════════════════════
"""

from typing import List
from typing import Optional


class KnowledgeService:

    def __init__(self):
        self.registry = None

    def attach(self, registry):
        self.registry = registry

    def loaded(self):
        return self.registry is not None

    def all(self):
        if not self.loaded():
            return []
        return self.registry.all()

    def count(self):
        return len(self.all())

    def find(self, entity_id):
        if not self.loaded():
            return None

        return self.registry.find(entity_id)

    def search(self, text):
        if not self.loaded():
            return []

        text = text.lower()
        result = []
        for entity in self.registry.all():
            title = str(
                getattr(
                    entity,
                    "title",
                    ""
                )
            ).lower()

            if text in title:
                result.append(entity)
        return result

    def by_type(self, entity_type):
        if not self.loaded():
            return []
        result = []
        for entity in self.registry.all():
            if getattr(
                entity,
                "entity_type",
                ""
            ) == entity_type:
                result.append(entity)
        return result

    def statistics(self):
        return {
            "loaded": self.loaded(),
            "entities": self.count()
        }


knowledge_service = KnowledgeService()