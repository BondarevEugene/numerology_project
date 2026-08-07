"""
Genesis Workspace Renderer
"""

from flask import render_template


class WorkspaceRenderer:

    def render(self, workspace):
        return render_template(
            workspace.template(),
            workspace=workspace,
            **workspace.build_context()
        )


workspace_renderer = WorkspaceRenderer()
