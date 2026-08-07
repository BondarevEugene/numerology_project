"""
Workspace Loader
Автоматическая регистрация Workspace.
"""

from kernel.workspace_registry import (
    workspace_registry
)


class WorkspaceLoader:

    def register (self, workspace):
        workspace.boot()
        workspace_registry.register(
            workspace
        )
        return workspace

    # -------------------------------------------------

    def load(self, workspaces):
        for workspace in workspaces:
            self.register(
                workspace
            )


workspace_loader = WorkspaceLoader()