from kernel.workspace_registry import workspace_registry

from workspaces.human import HumanWorkspace


def register_workspaces():

    ws = HumanWorkspace()

    workspace_registry.register(ws)

    print("REGISTER:", ws.id)

    print("TOTAL:", len(workspace_registry))

    return workspace_registry