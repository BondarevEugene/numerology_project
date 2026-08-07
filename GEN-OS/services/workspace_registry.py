from config.workspaces import WORKSPACES


class WorkspaceRegistry:

    @staticmethod
    def get(name):

        return WORKSPACES.get(
            name,
            WORKSPACES["dashboard"]
        )

    @staticmethod
    def all():

        return WORKSPACES
