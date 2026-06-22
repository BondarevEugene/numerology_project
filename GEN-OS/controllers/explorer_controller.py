"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Explorer Controller

BUILD-0031

Author:
OpenAI + Yevhenii Bondariev

Description:
Контроллер левой панели навигации.
Explorer отображает Registry в виде дерева.
Никакой бизнес-логики не содержит.

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import List, Optional

from controllers.console_controller import console


@dataclass
class ExplorerNode:
    id: str
    title: str
    icon: str = "📄"
    type: str = "entity"
    expanded: bool = True
    selected: bool = False
    children: List["ExplorerNode"] = field(default_factory=list)


class ExplorerController:
    def __init__(self):
        self.root_nodes = []
        self.selected = None

    def clear(self):
        self.root_nodes = []

    def load_registry(self, registry):
        self.clear()
        groups = {}
        for entity in registry.all():
            entity_type = getattr(
                entity,
                "entity_type",
                "other"
            )
            if entity_type not in groups:
                groups[entity_type] = ExplorerNode(
                    id=entity_type,
                    title=entity_type.title(),
                    icon="📂",
                    type="group"
                )
            groups[entity_type].children.append(
                ExplorerNode(
                    id=str(entity.id),
                    title=getattr(
                        entity,
                        "title",
                        "Unnamed"
                    ),
                    icon="📄",
                    type=entity_type
                )
            )
        self.root_nodes = list(groups.values())
        console.success(
            "Explorer",
            f"{len(self.root_nodes)} groups loaded."
        )

    def select(
        self,
        node_id: str
    ):
        self.selected = node_id
        for group in self.root_nodes:
            for node in group.children:
                node.selected = (
                    node.id == node_id
                )
        console.info(
            "Explorer",
            f"Selected node {node_id}"
        )
    def search(
        self,
        text: str
    ):
        text = text.lower()
        result = []
        for group in self.root_nodes:
            for node in group.children:
                if text in node.title.lower():
                    result.append(node)
        return result

    def context(self):
        return {
            "tree": self.root_nodes,
            "selected": self.selected
        }


explorer = ExplorerController()