"""
═══════════════════════════════════════════════════════════════

Genesis Workspace Manager

BUILD 0511

═══════════════════════════════════════════════════════════════
"""

from kernel.workspace_registry import workspace_registry
from kernel.workspace_renderer import workspace_renderer


class WorkspaceManager:

    def __init__(self):

        self.registry = workspace_registry
        self.renderer = workspace_renderer

    # --------------------------------------------------

    def register(self, workspace):

        workspace.boot()

        self.registry.register(workspace)

        return workspace

    # --------------------------------------------------

    def get(self, workspace_id):

        return self.registry.get(workspace_id)

    # --------------------------------------------------

    def all(self):

        return self.registry.all()

    # --------------------------------------------------

    def menu(self):

        return self.registry.menu()

    # --------------------------------------------------

    def render(self, workspace_id):

        workspace = self.get(workspace_id)

        if workspace is None:
            raise KeyError(workspace_id)

        return self.renderer.render(workspace)


workspace_manager = WorkspaceManager()