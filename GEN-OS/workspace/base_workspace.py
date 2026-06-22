"""
═══════════════════════════════════════════════════════════════════════

GEN-OS®
Genesys Operating System
Base Workspace
BUILD-0032

───────────────────────────────────────────────────────────────────────
Назначение

Базовый класс любого рабочего пространства GEN-OS.
Все Workspace наследуются только от него.
Жизненный цикл:

load()
render()
refresh()
unload()
═══════════════════════════════════════════════════════════════════════
"""

from abc import ABC
from abc import abstractmethod


class BaseWorkspace(ABC):

    def __init__(
        self,
        workspace_id: str,
        title: str,
        icon: str
    ):
        self.workspace_id = workspace_id
        self.title = title
        self.icon = icon
        self.loaded = False

    def load(self):
        self.loaded = True

    def unload(self):
        self.loaded = False

    def refresh(self):
        pass

    @abstractmethod
    def render(self):
        pass

    def status(self):
        return {
            "id": self.workspace_id,
            "title": self.title,
            "loaded": self.loaded
        }
