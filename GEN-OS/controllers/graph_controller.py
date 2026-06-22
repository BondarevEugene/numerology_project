"""
═══════════════════════════════════════════════════════════════════════

GEN-OS®
Genesys Operating System
Graph Controller
BUILD-0032

───────────────────────────────────────────────────────────────────────

Назначение

Управляет Graph Workspace.

Отвечает за:

• построение графа знаний
• загрузку сущностей
• построение связей
• поиск соседних узлов
• обновление графа
• уведомление интерфейса

ВНИМАНИЕ

Контроллер ничего не знает
о Flask,
HTML,
SQLAlchemy.

Он управляет исключительно
логикой Graph Workspace.

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class GraphState:
    loaded: bool = False
    nodes: int = 0
    edges: int = 0
    selected_node: Optional[str] = None
    selected_relation: Optional[str] = None
    dirty: bool = False


class GraphController:

    def __init__(self):
        self.state = GraphState()

    def load(self):
        self.state.loaded = True

    def unload(self):
        self.state = GraphState()

    def refresh(self):
        self.state.dirty = False

    def add_node(
        self,
        entity: Any
    ):
        self.state.nodes += 1
        self.state.dirty = True

    def add_relation(
        self,
        relation: Any
    ):
        self.state.edges += 1
        self.state.dirty = True

    def select_node(
        self,
        entity_id: str
    ):
        self.state.selected_node = entity_id

    def select_relation(
        self,
        relation_id: str
    ):
        self.state.selected_relation = relation_id

    def statistics(self):
        return {
            "nodes": self.state.nodes,
            "edges": self.state.edges,
            "loaded": self.state.loaded,
            "dirty": self.state.dirty

        }

    def get_state(self):
        return self.state