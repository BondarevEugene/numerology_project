"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

GEN-OS

Profession Service

BUILD:0045

DESCRIPTION

Работа со всеми профессиями платформы.

Используется:

• Human Workspace
• Career Engine
• Import Station
• Recommendation Engine
• AI Matching
• Prediction

═══════════════════════════════════════════════════════════════════════
"""

from typing import List


class ProfessionService:

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

    def by_category(
        self,
        category
    ):

        result = []

        for profession in self.all():

            if getattr(
                profession,
                "category",
                None
            ) == category:

                result.append(
                    profession
                )

        return result

    def search(
        self,
        text
    ):

        result = []

        text = text.lower()

        for profession in self.all():

            if text in profession.title.lower():

                result.append(
                    profession
                )

        return result

    def statistics(self):

        categories = {}

        for profession in self.all():

            category = getattr(
                profession,
                "category",
                "Unknown"
            )

            categories[
                category
            ] = categories.get(
                category,
                0
            ) + 1

        return {

            "count": self.count(),

            "categories": categories

        }


profession_service = ProfessionService()