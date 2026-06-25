"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Knowledge Controller
BUILD-0031
Author:
OpenAI + Yevhenii Bondariev
Description:
Главный контроллер Knowledge Workspace.

Отвечает за:
• загрузку Registry
• выбор сущности
• поиск
• фильтрацию
• передачу объекта Inspector
• обновление Explorer
• публикацию событий

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from typing import List, Optional

from controllers.console_controller import console
from controllers.statusbar_controller import statusbar
from controllers.inspector_controller import InspectorController


@dataclass
class KnowledgeState:
    entity_type: str = "profession"
    selected_id: Optional[str] = None
    search: str = ""
    total_entities: int = 0


class KnowledgeController:

    def __init__(self):
        self.state = KnowledgeState()
        self.registry = None
        self.inspector = InspectorController()
        self.entities = []

    def attach_registry(
            self,
            registry
    ):

        self.registry = registry
        self.reload()

    def reload(self):
        if self.registry is None:
            self.entities = []
            self.state.total_entities = 0

            return

        self.entities = self.registry.all()
        self.state.total_entities = len(
            self.entities
        )
        statusbar.set_registry_size(
            self.state.total_entities
        )

        console.success(
            "Knowledge",
            f"{self.state.total_entities} entities loaded."
        )

    def search(
            self,
            text: str
    ):
        self.state.search = text.lower()

        if not self.registry:
            return []
        result = []
        for entity in self.entities:
            title = str(
                getattr(
                    entity,
                    "title",
                    ""

                )
            ).lower()
            if self.state.search in title:
                result.append(
                    entity
                )
        return result

    def select(
            self,
            entity
    ):

        self.state.selected_id = getattr(
            entity,
            "id",
            None
        )

        statusbar.set_entity(
            getattr(
                entity,
                "title",
                "-"
            )
        )

        self.inspector.load_entity(
            entity
        )
        console.info(
            "Knowledge",
            f"Selected: {getattr(entity, 'title', '')}"
        )

    def current(self):
        return self.state

    def context(self):
        return {
            "knowledge": self.state,
            "entities": self.entities,
            "inspector": self.inspector.context()
        }


knowledge = KnowledgeController()

"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Knowledge Controller

BUILD:0102

═══════════════════════════════════════════════════════════════════════
"""

from flask import render_template

from services.entity_service import entity_service
from services.relation_service import relation_service


class KnowledgeController:

    def workspace(self):
        return render_template(
            "workspaces/knowledge_workspace.html",
            entities=entity_service.count(),
            relations=relation_service.count()
        )

    def statistics(self):

        return {
            "entities":
                entity_service.count(),
            "relations":
                relation_service.count()
        }


knowledge_controller = KnowledgeController()