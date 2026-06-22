"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

StatusBar Controller

BUILD-0031

Author:
OpenAI + Yevhenii Bondariev

Description:
Управляет нижней строкой состояния GENOS.

Показывает:

• текущий Workspace
• выбранную сущность
• количество объектов Registry
• состояние Import
• состояние AI
• состояние Graph
• системное время
• версию платформы

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class StatusBarState:
    workspace: str = "Knowledge"
    entity: str = "-"
    registry_objects: int = 0
    graph_nodes: int = 0
    graph_edges: int = 0
    import_jobs: int = 0
    ai_state: str = "Idle"
    kernel_state: str = "READY"
    version: str = "GENOS BUILD-0031"
    last_update: str = ""


class StatusBarController:
    def __init__(self):
        self.state = StatusBarState()
        self.refresh()

    def refresh(self):
        self.state.last_update = datetime.now().strftime("%H:%M:%S")

    def set_workspace(
            self,
            workspace: str
    ):
        self.state.workspace = workspace
        self.refresh()

    def set_entity(
            self,
            entity: str
    ):
        self.state.entity = entity
        self.refresh()

    def set_registry_size(
            self,
            count: int
    ):
        self.state.registry_objects = count
        self.refresh()

    def set_graph(
            self,
            nodes: int,
            edges: int
    ):
        self.state.graph_nodes = nodes
        self.state.graph_edges = edges
        self.refresh()

    def set_import_jobs(
            self,
            count: int
    ):
        self.state.import_jobs = count
        self.refresh()

    def set_ai_state(
            self,
            state: str
    ):
        self.state.ai_state = state
        self.refresh()

    def set_kernel_state(
            self,
            state: str
    ):
        self.state.kernel_state = state
        self.refresh()

    def snapshot(self):
        return self.state

    def context(self):
        return {
            "statusbar": self.state
        }


statusbar = StatusBarController()
