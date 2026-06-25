"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

GEN-OS Workspace Runtime

FILE: workspace_runtime.py

BUILD: 0036

AUTHOR:
OpenAI + Yevhenii Bondariev

DESCRIPTION
-----------
Runtime отвечает за запуск Workspace.
Он соединяет:
Kernel
↓
WorkspaceService
↓
Controller
↓
Template
↓
Javascript

Runtime ничего не знает
о Flask,
HTML,
SQLAlchemy.

═══════════════════════════════════════════════════════════════════════
"""

from services.workspace_service import workspace_service


class WorkspaceRuntime:

    def __init__(self):
        self.active = None

    def boot(self):
        if workspace_service.current() is None:
            workspaces = workspace_service.list()
            if workspaces:
                workspace_service.open(
                    workspaces[0].id
                )
        self.active = workspace_service.current()
        return self.active

    def switch(self, workspace_id):
        self.active = workspace_service.open(
            workspace_id
        )
        return self.active

    def current(self):
        return self.active

    def template(self):
        if self.active is None:
            return None
        return self.active.template

    def javascript(self):
        if self.active is None:
            return None
        return self.active.javascript

    def context(self):
        return {

            "workspace":
                self.current(),

            "workspaces":
                workspace_service.list(),

            "template":
                self.template(),

            "javascript":
                self.javascript()

        }


workspace_runtime = WorkspaceRuntime()
