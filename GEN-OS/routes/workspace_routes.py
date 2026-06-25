"""
═══════════════════════════════════════════════════════════════════════

GEN-OS®
Workspace Routes
BUILD-0016

Описание
Единая точка входа для всех Workspace платформы.
Shell никогда не знает где лежит HTML.
Shell просто делает:
GET /workspace/import
а этот файл сам находит нужный шаблон.

═══════════════════════════════════════════════════════════════════════
"""

from flask import Blueprint
from flask import render_template
from flask import abort

from kernel.workspaces import WORKSPACES


workspace_bp = Blueprint(
    "workspace",
    __name__
)


@workspace_bp.route(
    "/workspace/<workspace_id>"
)
def workspace_loader(
    workspace_id
):
    workspace = WORKSPACES.get(
        workspace_id
    )
    if workspace is None:
        abort(404)
    return render_template(
        workspace.template,
        workspace=workspace
    )


@workspace_bp.route(
    "/api/workspaces"
)
def workspace_registry():
    return {
        item.id:{
            "title":item.title,
            "subtitle":item.subtitle,
            "icon":item.icon,
            "enabled":item.enabled
        }
        for item in WORKSPACES.values()
    }