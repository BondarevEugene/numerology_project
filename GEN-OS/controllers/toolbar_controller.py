"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Toolbar Controller

BUILD-0031

Author:
OpenAI + Yevhenii Bondariev

Description:
Управляет верхней панелью GENOS.

Отвечает за:

• переключение Workspace
• быстрый поиск
• текущего пользователя
• уведомления
• состояние ядра
• действия Toolbar

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ToolbarAction:
    id: str
    title: str
    icon: str
    enabled: bool = True
    visible: bool = True


@dataclass
class ToolbarState:
    workspace: str = "Knowledge"
    search: str = ""
    username: str = "Administrator"
    notifications: int = 0
    kernel_state: str = "READY"
    actions: List[ToolbarAction] = field(default_factory=list)


class ToolbarController:

    def __init__(self):
        self.state = ToolbarState()
        self._build_default_actions()

    def _build_default_actions(self):
        self.state.actions = [
            ToolbarAction(
                id="new",
                title="New",
                icon="📄"
            ),
            ToolbarAction(
                id="save",
                title="Save",
                icon="💾"
            ),
            ToolbarAction(
                id="import",
                title="Import",
                icon="📥"
            ),
            ToolbarAction(
                id="export",
                title="Export",
                icon="📤"
            ),
            ToolbarAction(
                id="refresh",
                title="Refresh",
                icon="🔄"
            ),
            ToolbarAction(
                id="settings",
                title="Settings",
                icon="⚙"
            )
        ]

    def set_workspace(
            self,
            workspace: str
    ):
        self.state.workspace = workspace

    def set_search(
            self,
            value: str
    ):
        self.state.search = value

    def set_kernel_state(
            self,
            state: str
    ):

        self.state.kernel_state = state

    def set_notifications(
            self,
            count: int
    ):
        self.state.notifications = count

    def set_user(
            self,
            username: str
    ):
        self.state.username = username

    def add_action(
            self,
            action: ToolbarAction
    ):
        self.state.actions.append(action)

    def remove_action(
            self,
            action_id: str
    ):
        self.state.actions = [
            action
            for action
            in self.state.actions
            if action.id != action_id
        ]

    def get_action(
            self,
            action_id: str
    ) -> Optional[ToolbarAction]:
        for action in self.state.actions:
            if action.id == action_id:
                return action
        return None

    def enable(
            self,
            action_id: str
    ):
        action = self.get_action(action_id)
        if action:
            action.enabled = True

    def disable(
            self,
            action_id: str
    ):
        action = self.get_action(action_id)
        if action:
            action.enabled = False

    def hide(
            self,
            action_id: str
    ):
        action = self.get_action(action_id)
        if action:
            action.visible = False

    def show(
            self,
            action_id: str
    ):
        action = self.get_action(action_id)
        if action:
            action.visible = True

    def context(self):
        return {
            "toolbar": self.state
        }


toolbar = ToolbarController()
