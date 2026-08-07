"""
Workspace Registry
Хранит зарегистрированные Workspace.
"""


class WorkspaceRegistry:

    def __init__(self):
        self._workspaces = {}

    # -----------------------------------------------------

    def register(self, workspace):
        self._workspaces[
            workspace.id
        ] = workspace
        return workspace

    # -----------------------------------------------------

    def unregister(self, workspace_id):
        self._workspaces.pop(
            workspace_id,
            None
        )

    # -----------------------------------------------------

    def get(self, workspace_id):
        return self._workspaces.get(
            workspace_id
        )

    # -----------------------------------------------------

    def exists(self, workspace_id):
        return workspace_id in self._workspaces

    # -----------------------------------------------------

    def all(self):
        return list(
            self._workspaces.values()
        )

    # -----------------------------------------------------

    def menu(self):
        return [
            workspace
            for workspace
            in self.all()
            if workspace.menu
        ]

    # -----------------------------------------------------

    def __len__(self):
        return len(
            self._workspaces
        )


workspace_registry = WorkspaceRegistry()
