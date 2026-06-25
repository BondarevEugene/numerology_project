"""
═══════════════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS
Entity Service
BUILD:0066
AUTHOR
OpenAI + Yevhenii Bondariev

DESCRIPTION
------------

Базовый сервис работы со всеми сущностями платформы.
Любая сущность GEN-OS проходит через EntityService.
Поддерживаемые типы:

• Human
• Profession
• Competency
• Book
• Habit
• Hobby
• Sport
• Course
• Protocol
• Environment
• Tool
• Technology
• Company
• University

═══════════════════════════════════════════════════════════════════════════════
"""

from collections import defaultdict


class EntityService:

    def __init__(self):
        self.registry = None

    def attach(
        self,
        registry
    ):
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
        return self.registry.find(
            entity_id
        )

    def search(
        self,
        text
    ):
        text = text.lower()
        result = []
        for entity in self.all():
            title = getattr(
                entity,
                "title",
                ""
            )
            if text in title.lower():
                result.append(
                    entity
                )
        return result

    def by_type(
        self,
        entity_type
    ):

        result = []
        for entity in self.all():
            if getattr(
                entity,
                "entity_type",
                ""
            ) == entity_type:
                result.append(
                    entity
                )
        return result

    def statistics(self):
        stats = defaultdict(int)
        for entity in self.all():
            entity_type = getattr(
                entity,
                "entity_type",
                "Unknown"
            )
            stats[
                entity_type
            ] += 1
        return dict(stats)


entity_service = EntityService()