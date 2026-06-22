"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Workspace Controller
BUILD-0024
Назначение
-----------
Главный контроллер рабочей области.
Не содержит бизнес-логики.
Связывает:

• Kernel
• Registry
• Explorer
• Inspector
• Toolbar
• Console
Является точкой входа GUI.
═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from typing import Optional

from UI.layout import WORKSPACE
from dataclasses import dataclass
from typing import Dict
from controllers.console_controller import console
from controllers.statusbar_controller import statusbar
from controllers.toolbar_controller import toolbar


@dataclass
class WorkspaceState:
    current_workspace: str = "human"
    selected_entity: Optional[str] = None
    loaded: bool = False
    title: str = "Genesis Workspace"


class WorkspaceController:

    def __init__(self):
        self.state = WorkspaceState()
        self.modules = WORKSPACE
        self.context: Dict[str, Any] = {}

    def boot(self):
        self.state.loaded = True
        self.context = {
            "workspace": self.state,
            "modules": self.modules
        }
        return self.context

    def switch_workspace(self, workspace: str):
        self.state.current_workspace = workspace

    def select_entity(self, entity_id: str):
        self.state.selected_entity = entity_id

    def title(self):
        return self.state.title

    def render_context(self):
        return {
            "workspace": self.state,
            "modules": self.modules,
            "selected": self.state.selected_entity
        }

    @dataclass
    class Workspace:

        id: str
        title: str
        icon: str
        opened: bool = False

    class WorkspaceController:

        def __init__(self):
            self.workspaces: Dict[str, Workspace] = {}
            self.current = None
            self.register_defaults()

        def register_defaults(self):

            self.register(
                Workspace(
                    id="knowledge",
                    title="Knowledge",
                    icon="📚"
                )
            )

            self.register(
                Workspace(
                    id="human",
                    title="Human",
                    icon="👤"
                )
            )
            self.register(
                Workspace(
                    id="career",
                    title="Career",
                    icon="💼"
                )
            )
            self.register(
                Workspace(
                    id="prediction",
                    title="Prediction",
                    icon="📈"
                )
            )
            self.register(
                Workspace(
                    id="graph",
                    title="Graph",
                    icon="🕸"
                )
            )
            self.register(
                Workspace(
                    id="import",
                    title="Import",
                    icon="📥"
                )
            )

        def register(
                self,
                workspace: Workspace
        ):
            self.workspaces[workspace.id] = workspace

        def open(
                self,
                workspace_id: str
        ):
            if workspace_id not in self.workspaces:
                console.error(
                    "Workspace",
                    f"{workspace_id} not registered."
                )
                return
            for workspace in self.workspaces.values():
                workspace.opened = False
            current = self.workspaces[workspace_id]
            current.opened = True
            self.current = current
            toolbar.set_workspace(
                current.title
            )
            statusbar.set_workspace(
                current.title
            )
            console.success(
                "Workspace",
                f"{current.title} opened."
            )

        def current_workspace(self):
            return self.current

        def list(self):
            return list(
                self.workspaces.values()
            )

        def context(self):
            return {
                "workspace": self.current,
                "workspaces": self.list()
            }

    workspace = WorkspaceController()
