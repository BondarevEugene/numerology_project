"""
═══════════════════════════════════════════════════════════════════════

GENESIS HR®

GEN-OS Platform

FILE:
kernel/platform.py

BUILD:
0102

DESCRIPTION

Главный объект платформы.

Platform соединяет все подсистемы GEN-OS,
но не содержит бизнес-логики.

═══════════════════════════════════════════════════════════════════════
"""

from kernel.manifest import PLATFORM
from kernel.modules import MODULES
from kernel.workspaces import WORKSPACES

from kernel.shell_context import shell_context

from services.workspace_service import workspace_service
from kernel.workspace_runtime import workspace_runtime


class Platform:

    def __init__(self):
        self.manifest = PLATFORM
        self.modules = MODULES
        self.workspaces = WORKSPACES
        self.workspace_service = workspace_service
        self.runtime = workspace_runtime
        self.shell = shell_context

    def boot(self):
        self.runtime.boot()
        return self

    def context(self):
        return self.shell.build()

    def statistics(self):
        return {
            "modules": len(self.modules),
            "workspaces": len(self.workspaces),
            "current_workspace":
                self.runtime.current().id
                if self.runtime.current()
                else None
        }


platform = Platform()
