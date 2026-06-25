"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

GEN-OS Workspace Service

FILE:workspace_service.py

BUILD:0034

AUTHOR:
OpenAI + Yevhenii Bondariev

DESCRIPTION
-----------

Единый сервис управления Workspace.

Не зависит от Flask.
Не зависит от HTML.
Не зависит от SQLAlchemy.
Является прослойкой между
Kernel и GUI.

Функции

• регистрация Workspace
• открытие Workspace
• закрытие Workspace
• переключение
• текущий Workspace
• список Workspace
• история переходов

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional

from kernel.workspaces import WORKSPACES
from kernel.event_bus import event_bus


@dataclass
class WorkspaceSession:
    id: str
    title: str
    icon: str
    template: str
    javascript: str
    opened: bool = False


class WorkspaceService:

    def __init__(self):
        self._registry: Dict[str, WorkspaceSession] = {}
        self._history: List[str] = []
        self._current: Optional[WorkspaceSession] = None
        self._load_registry()

    def _load_registry(self):
        for workspace in WORKSPACES.values():
            self._registry[
                workspace.id
            ] = WorkspaceSession(
                id=workspace.id,
                title=workspace.title,
                icon=workspace.icon,
                template=workspace.template,
                javascript=workspace.javascript
            )

    def list(self):
        return list(
            self._registry.values()
        )

    def current(self):
        return self._current

    def history(self):
        return self._history

    def exists(
            self,
            workspace_id: str
    ):
        return workspace_id in self._registry

    def open(
            self,
            workspace_id: str
    ):
        if workspace_id not in self._registry:
            return None
        if self._current:
            self._current.opened = False

        workspace = self._registry[
            workspace_id
        ]
        workspace.opened = True
        self._current = workspace
        self._history.append(
            workspace.id
        )
        event_bus.publish(
            "workspace.changed",
            workspace
        )
        return workspace

    def close(self):
        if self._current is None:
            return
        self._current.opened = False
        event_bus.publish(
            "workspace.closed",
            self._current
        )
        self._current = None

    def reload(self):
        self._registry.clear()
        self._load_registry()

    def statistics(self):
        return {
            "registered":
                len(self._registry),
            "opened":
                self._current.id
                if self._current
                else None,
            "history":
                len(self._history)
        }


workspace_service = WorkspaceService()