"""
═══════════════════════════════════════════════════════════════════════

GENESIS HR®
GEN-OS
FILE:kernel/shell_context.py

BUILD:0101

DESCRIPTION
Формирует единый Context для Shell.
Никакой HTML.
Никакого Flask.
Только подготовка данных.

═══════════════════════════════════════════════════════════════════════
"""

from services.workspace_service import workspace_service
from kernel.workspace_runtime import workspace_runtime


class ShellContext:
    def build(self):
        return {
            "workspace":
                workspace_runtime.current(),
            "workspaces":
                workspace_service.list(),
            "template":
                workspace_runtime.template(),
            "javascript":
                workspace_runtime.javascript(),
            "tree": [],
            "entity_count": 0,
            "relation_count": 0,
            "console": [],
            "kernel_status": "ONLINE"

        }


shell_context = ShellContext()
