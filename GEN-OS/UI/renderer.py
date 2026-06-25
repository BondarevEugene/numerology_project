"""
══════════════════════════════════════════════════════════════════════
GENESIS HR®
Workspace Renderer

Build:
0002

══════════════════════════════════════════════════════════════════════
"""

from flask import render_template

class WorkspaceRenderer:

    @staticmethod
    def render(workspace, **context):
        return render_template(
            "workspace/page.html",
            workspace=workspace,
            **context
        )