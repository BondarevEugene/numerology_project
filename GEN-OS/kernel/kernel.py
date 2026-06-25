"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS

FILE:kernel.py

BUILD:0101

DESCRIPTION
Главное ядро платформы.
Содержит ссылки на все основные подсистемы.
═══════════════════════════════════════════════════════════════════════
"""

from kernel.manifest import PLATFORM
from kernel.modules import MODULES

from kernel.workspaces import WORKSPACES

from services.workspace_service import workspace_service

from kernel.shell_context import shell_context


class GenesisKernel:
    VERSION = PLATFORM["version"]
    PLATFORM = PLATFORM["name"]
    BUILD = PLATFORM["build"]

    def __init__(self):
        self.manifest = PLATFORM
        self.modules = MODULES
        self.workspaces = WORKSPACES
        self.workspace_service = workspace_service
        self.shell = shell_context

    def statistics(self):
        return {"modules": len(self.modules), "workspaces": len(self.workspaces)
                }


kernel = GenesisKernel()
