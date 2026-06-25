"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS
Search Service
BUILD:0034

DESCRIPTION
-----------
Единый поисковый движок платформы.
Работает поверх KnowledgeService.
Используется:

• Explorer
• Human Workspace
• Graph
• AI
• Prediction

═══════════════════════════════════════════════════════════════════════
"""

from services.knowledge_service import knowledge_service


class SearchService:

    def search(
        self,
        text,
        entity_type=None
    ):
        entities = knowledge_service.search(
            text
        )

        if entity_type is None:
            return entities
        result = []
        for entity in entities:
            if getattr(
                entity,
                "entity_type",
                ""

            ) == entity_type:
                result.append(
                    entity
                )
        return result

    def first(
        self,
        text
    ):
        result = self.search(
            text
        )
        if result:
            return result[0]
        return None


search_service = SearchService()