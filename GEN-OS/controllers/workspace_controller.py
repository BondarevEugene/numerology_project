"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS

Workspace Controller

BUILD-0034
Author:
OpenAI + Yevhenii Bondariev

Description
-----------
Главный контроллер интерфейса.
Не содержит бизнес-логики.
Работает исключительно
через WorkspaceService.

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from typing import Optional

from controllers.console_controller import console
from controllers.statusbar_controller import statusbar
from controllers.toolbar_controller import toolbar

from services.workspace_service import workspace_service


@dataclass
class WorkspaceState:
    current_workspace: str = "human"
    title: str = "Digital Twin"
    selected_entity: Optional[str] = None
    loaded: bool = False


class WorkspaceController:

    def __init__(self):
        self.state = WorkspaceState()

    def boot(self):
        workspace = workspace_service.current()
        if workspace:
            self.state.current_workspace = workspace.id
            self.state.title = workspace.title
        self.state.loaded = True

        console.success(
            "Workspace",
            "Workspace Controller initialized."
        )

        return self.context()

    def open(self, workspace_id: str):
        workspace = workspace_service.open(workspace_id)
        if workspace is None:
            return
        self.state.current_workspace = workspace.id
        self.state.title = workspace.title
        toolbar.set_workspace(workspace.title)
        statusbar.set_workspace(workspace.title)

    def select_entity(self, entity_id: str):
        self.state.selected_entity = entity_id

    def context(self):
        return {
            "workspace": self.state,
            "workspaces": workspace_service.list()
        }


workspace = WorkspaceController()

"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Workspace Controller

BUILD:0106

═══════════════════════════════════════════════════════════════════════
"""

from services.workspace_service import (
    workspace_service
)


class WorkspaceController:

    def current(self):
        return workspace_service.current()

    def open(
            self,
            workspace_id
    ):
        return workspace_service.open(
            workspace_id
        )

    def close(self):
        return workspace_service.close()

    def list(self):
        return workspace_service.list()

    def statistics(self):
        return workspace_service.statistics()


workspace_controller = WorkspaceController()
